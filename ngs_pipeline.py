#!/usr/bin/env python3
"""
NGS Data Processing Pipeline
============================

주어진 디렉토리의 모든 FASTQ 파일에 대해 다음을 자동으로 수행하는 파이프라인:
1. FastQC - 품질 분석
2. CutAdapt - Illumina Universal Adapter 제거  
3. BWA-mem2 - Alignment 및 markdup, BAI 인덱싱

Usage:
    python3 ngs_pipeline.py [options]
    
Example:
    python3 ngs_pipeline.py --input-dir /path/to/fastq --reference /path/to/bwa-index --output-dir /path/to/output
"""

import argparse
import os
import sys
import subprocess
import glob
import logging
from pathlib import Path
import time

class NGSPipeline:
    """NGS 데이터 처리 파이프라인 클래스"""
    
    def __init__(self, input_dir, reference_prefix, output_dir, threads=4):
        self.input_dir = Path(input_dir)
        self.reference_prefix = reference_prefix
        self.output_dir = Path(output_dir)
        self.threads = threads
        
        # Illumina Universal Adapter 시퀀스 (homework2.sh에서 참조)
        self.adapter_r1 = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA"
        self.adapter_r2 = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT"
        
        # 출력 디렉토리 설정
        self.fastqc_dir = self.output_dir / "fastqc_results"
        self.trimmed_dir = self.output_dir / "trimmed"
        self.aligned_dir = self.output_dir / "aligned"
        
        # 로깅 설정
        self.setup_logging()
        
    def setup_logging(self):
        """로깅 설정"""
        # 출력 디렉토리 먼저 생성
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'pipeline.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_directories(self):
        """필요한 디렉토리 생성"""
        self.logger.info("=== 디렉토리 구조 생성 ===")
        directories = [self.output_dir, self.fastqc_dir, self.trimmed_dir, self.aligned_dir]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"디렉토리 생성: {directory}")
            
    def find_fastq_pairs(self):
        """FASTQ 파일 쌍 찾기"""
        self.logger.info("=== FASTQ 파일 쌍 검색 ===")
        
        # 패턴 매칭으로 R1, R2 파일 찾기
        r1_pattern = str(self.input_dir / "*_1.fastq.gz")
        r2_pattern = str(self.input_dir / "*_2.fastq.gz")
        
        r1_files = sorted(glob.glob(r1_pattern))
        r2_files = sorted(glob.glob(r2_pattern))
        
        self.logger.info(f"발견된 R1 파일: {len(r1_files)}개")
        self.logger.info(f"발견된 R2 파일: {len(r2_files)}개")
        
        if not r1_files or not r2_files:
            raise FileNotFoundError("FASTQ 파일을 찾을 수 없습니다.")
            
        if len(r1_files) != len(r2_files):
            raise ValueError("R1과 R2 파일 개수가 일치하지 않습니다.")
            
        # 파일 쌍 매칭
        pairs = []
        for r1_file in r1_files:
            # _1.fastq.gz를 _2.fastq.gz로 바꿔서 대응하는 R2 파일 찾기
            r2_file = r1_file.replace("_1.fastq.gz", "_2.fastq.gz")
            if r2_file in r2_files:
                pairs.append((r1_file, r2_file))
                self.logger.info(f"파일 쌍: {os.path.basename(r1_file)} & {os.path.basename(r2_file)}")
            else:
                self.logger.warning(f"대응하는 R2 파일을 찾을 수 없습니다: {r1_file}")
                
        if not pairs:
            raise FileNotFoundError("매칭되는 FASTQ 파일 쌍을 찾을 수 없습니다.")
            
        return pairs
        
    def run_command(self, command, description):
        """시스템 명령어 실행"""
        self.logger.info(f"{description}")
        self.logger.info(f"실행 명령어: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                self.logger.debug(f"STDOUT: {result.stdout}")
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"명령어 실행 실패: {e}")
            self.logger.error(f"STDERR: {e.stderr}")
            raise
            
    def run_fastqc(self, fastq_files):
        """FastQC 품질 분석 실행"""
        self.logger.info("=== FastQC 품질 분석 시작 ===")
        
        for fastq_file in fastq_files:
            if os.path.exists(fastq_file):
                command = [
                    "fastqc",
                    "--outdir", str(self.fastqc_dir),
                    "--threads", str(self.threads),
                    fastq_file
                ]
                
                self.run_command(
                    command,
                    f"FastQC 실행: {os.path.basename(fastq_file)}"
                )
            else:
                self.logger.warning(f"파일을 찾을 수 없습니다: {fastq_file}")
                
        self.logger.info(f"FastQC 분석 완료. 결과: {self.fastqc_dir}")
        
    def run_cutadapt(self, r1_file, r2_file):
        """CutAdapt를 이용한 어댑터 제거"""
        self.logger.info("=== CutAdapt Adapter Trimming 시작 ===")
        
        # 출력 파일명 생성
        r1_basename = os.path.basename(r1_file).replace(".fastq.gz", "")
        r2_basename = os.path.basename(r2_file).replace(".fastq.gz", "")
        
        r1_output = self.trimmed_dir / f"{r1_basename}_trimmed.fastq.gz"
        r2_output = self.trimmed_dir / f"{r2_basename}_trimmed.fastq.gz"
        
        self.logger.info(f"처리 중: {os.path.basename(r1_file)} & {os.path.basename(r2_file)}")
        self.logger.info(f"출력: {r1_output.name} & {r2_output.name}")
        
        # CutAdapt 명령어 (homework2.sh 참조)
        command = [
            "cutadapt",
            "-a", self.adapter_r1,  # R1 어댑터
            "-A", self.adapter_r2,  # R2 어댑터
            "--minimum-length", "20",
            "--cores", str(self.threads),
            "--output", str(r1_output),
            "--paired-output", str(r2_output),
            r1_file,
            r2_file
        ]
        
        self.run_command(command, f"CutAdapt 실행: 어댑터 제거")
        
        return str(r1_output), str(r2_output)
        
    def run_bwa_mem2(self, r1_trimmed, r2_trimmed, sample_name):
        """BWA-mem2를 이용한 alignment 및 후처리"""
        self.logger.info("=== BWA-mem2 Alignment 시작 ===")
        
        # 출력 파일명
        sam_file = self.aligned_dir / f"{sample_name}.sam"
        bam_file = self.aligned_dir / f"{sample_name}.bam"
        sorted_bam = self.aligned_dir / f"{sample_name}.sorted.bam"
        markdup_bam = self.aligned_dir / f"{sample_name}.sorted.markdup.bam"
        bai_file = self.aligned_dir / f"{sample_name}.sorted.markdup.bam.bai"
        
        # 1. BWA-mem2 alignment
        self.logger.info("1단계: BWA-mem2 alignment")
        bwa_command = [
            "bwa-mem2", "mem",
            "-t", str(self.threads),
            self.reference_prefix,
            r1_trimmed,
            r2_trimmed
        ]
        
        with open(sam_file, 'w') as sam_output:
            process = subprocess.run(
                bwa_command,
                stdout=sam_output,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            if process.stderr:
                self.logger.info(f"BWA-mem2 정보: {process.stderr}")
                
        self.logger.info(f"Alignment 완료: {sam_file}")
        
        # 2. SAM to BAM 변환
        self.logger.info("2단계: SAM to BAM 변환")
        sam_to_bam_command = [
            "samtools", "view",
            "-@", str(self.threads),
            "-b",
            "-o", str(bam_file),
            str(sam_file)
        ]
        self.run_command(sam_to_bam_command, "SAM to BAM 변환")
        
        # SAM 파일 삭제 (용량 절약)
        os.remove(sam_file)
        self.logger.info("SAM 파일 삭제 완료")
        
        # 3. BAM 파일 정렬 (name-sorted for fixmate)
        self.logger.info("3단계: BAM 파일 이름순 정렬")
        name_sorted_bam = self.aligned_dir / f"{sample_name}.namesorted.bam"
        name_sort_command = [
            "samtools", "sort",
            "-@", str(self.threads),
            "-n",  # name sort
            "-o", str(name_sorted_bam),
            str(bam_file)
        ]
        self.run_command(name_sort_command, "BAM 파일 이름순 정렬")
        
        # 정렬되지 않은 BAM 파일 삭제
        os.remove(bam_file)
        self.logger.info("정렬되지 않은 BAM 파일 삭제 완료")
        
        # 4. Fixmate (mate score 태그 추가)
        self.logger.info("4단계: Fixmate")
        fixmate_bam = self.aligned_dir / f"{sample_name}.fixmate.bam"
        fixmate_command = [
            "samtools", "fixmate",
            "-@", str(self.threads),
            "-m",  # add mate score tags
            str(name_sorted_bam),
            str(fixmate_bam)
        ]
        self.run_command(fixmate_command, "Fixmate 실행")
        
        # name-sorted BAM 파일 삭제
        os.remove(name_sorted_bam)
        self.logger.info("이름순 정렬 BAM 파일 삭제 완료")
        
        # 5. BAM 파일 좌표순 정렬
        self.logger.info("5단계: BAM 파일 좌표순 정렬")
        coord_sort_command = [
            "samtools", "sort",
            "-@", str(self.threads),
            "-o", str(sorted_bam),
            str(fixmate_bam)
        ]
        self.run_command(coord_sort_command, "BAM 파일 좌표순 정렬")
        
        # fixmate BAM 파일 삭제
        os.remove(fixmate_bam)
        self.logger.info("Fixmate BAM 파일 삭제 완료")
        
        # 6. Mark duplicates
        self.logger.info("6단계: Mark Duplicates")
        markdup_command = [
            "samtools", "markdup",
            "-@", str(self.threads),
            str(sorted_bam),
            str(markdup_bam)
        ]
        self.run_command(markdup_command, "Mark Duplicates")
        
        # 7. BAI 인덱스 생성
        self.logger.info("7단계: BAI 인덱스 생성")
        index_command = [
            "samtools", "index",
            str(markdup_bam)
        ]
        self.run_command(index_command, "BAI 인덱스 생성")
        
        self.logger.info(f"최종 출력 파일: {markdup_bam}")
        self.logger.info(f"인덱스 파일: {bai_file}")
        
        return str(markdup_bam)
        
    def get_sample_name(self, r1_file):
        """파일명에서 샘플명 추출"""
        basename = os.path.basename(r1_file)
        # SRR7211645_1.fastq.gz -> SRR7211645
        sample_name = basename.replace("_1.fastq.gz", "")
        return sample_name
        
    def run_pipeline(self):
        """전체 파이프라인 실행"""
        start_time = time.time()
        self.logger.info("=== NGS 데이터 처리 파이프라인 시작 ===")
        
        try:
            # 1. 디렉토리 생성
            self.create_directories()
            
            # 2. FASTQ 파일 쌍 찾기
            fastq_pairs = self.find_fastq_pairs()
            
            # 3. 모든 FASTQ 파일에 대해 FastQC 실행
            all_fastq_files = []
            for r1, r2 in fastq_pairs:
                all_fastq_files.extend([r1, r2])
            self.run_fastqc(all_fastq_files)
            
            # 4. 각 파일 쌍에 대해 처리
            for r1_file, r2_file in fastq_pairs:
                sample_name = self.get_sample_name(r1_file)
                self.logger.info(f"=== 샘플 처리: {sample_name} ===")
                
                # CutAdapt 실행
                r1_trimmed, r2_trimmed = self.run_cutadapt(r1_file, r2_file)
                
                # BWA-mem2 alignment 및 후처리
                final_bam = self.run_bwa_mem2(r1_trimmed, r2_trimmed, sample_name)
                
                self.logger.info(f"샘플 {sample_name} 처리 완료: {final_bam}")
                
            # 5. 결과 요약
            self.print_summary()
            
            elapsed_time = time.time() - start_time
            self.logger.info(f"=== 파이프라인 완료 (소요시간: {elapsed_time:.2f}초) ===")
            
        except Exception as e:
            self.logger.error(f"파이프라인 실행 중 오류 발생: {e}")
            raise
            
    def print_summary(self):
        """결과 요약 출력"""
        self.logger.info("=== 결과 요약 ===")
        
        # FastQC 결과
        fastqc_files = list(self.fastqc_dir.glob("*.html"))
        self.logger.info(f"FastQC 결과 파일 ({len(fastqc_files)}개):")
        for file in fastqc_files:
            self.logger.info(f"  {file}")
            
        # Trimmed FASTQ 파일
        trimmed_files = list(self.trimmed_dir.glob("*.fastq.gz"))
        self.logger.info(f"Trimmed FASTQ 파일 ({len(trimmed_files)}개):")
        for file in trimmed_files:
            self.logger.info(f"  {file}")
            
        # Aligned BAM 파일
        bam_files = list(self.aligned_dir.glob("*.markdup.bam"))
        self.logger.info(f"최종 BAM 파일 ({len(bam_files)}개):")
        for file in bam_files:
            bai_file = Path(str(file) + ".bai")
            index_status = "✓" if bai_file.exists() else "✗"
            self.logger.info(f"  {file} (인덱스: {index_status})")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="NGS 데이터 처리 파이프라인",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  python3 ngs_pipeline.py --input-dir /path/to/fastq --reference /path/to/bwa-index --output-dir /path/to/output
  python3 ngs_pipeline.py  # 기본값 사용
        """
    )
    
    # 기본값 설정
    default_input_dir = "/home/whalstj1/2025-bioinformatics/202255180/week3/homework/task6"
    default_reference = "/home/whalstj1/2025-bioinformatics/202255180/week3/homework/task6/bwa-index/Caenorhabditis_elegans.WBcel235.dna_sm.toplevel.fa.gz"
    default_output_dir = "/home/whalstj1/2025-bioinformatics/202255180/week3/homework/task6/results"
    
    parser.add_argument(
        "--input-dir",
        default=default_input_dir,
        help=f"FASTQ 파일이 위치한 디렉토리 (기본값: {default_input_dir})"
    )
    
    parser.add_argument(
        "--reference",
        default=default_reference,
        help=f"BWA 인덱스 파일 경로 (기본값: {default_reference})"
    )
    
    parser.add_argument(
        "--output-dir",
        default=default_output_dir,
        help=f"결과 출력 디렉토리 (기본값: {default_output_dir})"
    )
    
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="사용할 스레드 수 (기본값: 4)"
    )
    
    args = parser.parse_args()
    
    # 파이프라인 실행
    try:
        pipeline = NGSPipeline(
            input_dir=args.input_dir,
            reference_prefix=args.reference,
            output_dir=args.output_dir,
            threads=args.threads
        )
        
        pipeline.run_pipeline()
        
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()