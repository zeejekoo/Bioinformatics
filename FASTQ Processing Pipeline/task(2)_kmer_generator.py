#!/usr/bin/env python3
"""
K-mer Generator
입력받은 문자열에서 모든 k-mer를 생성하고 출력하는 프로그램입니다.
"""

import sys
import argparse


def generate_kmers(sequence, k):
    """
    주어진 문자열에서 모든 k-mer를 생성합니다.
    
    Args:
        sequence (str): 입력 문자열 (DNA 서열, 단백질 서열, 일반 텍스트 등)
        k (int): k-mer의 길이
    
    Returns:
        list: 모든 k-mer의 리스트
    
    Raises:
        ValueError: k값이 문자열 길이보다 큰 경우
    """
    if k <= 0:
        raise ValueError(f"k값은 양수여야 합니다: {k}")
    
    if k > len(sequence):
        raise ValueError(f"k값({k})이 문자열 길이({len(sequence)})보다 큽니다")
    
    kmers = []
    
    # 슬라이딩 윈도우 방식으로 k-mer 생성
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        kmers.append(kmer)
    
    return kmers


def count_kmers(kmers):
    """
    k-mer의 빈도를 계산합니다.
    
    Args:
        kmers (list): k-mer 리스트
    
    Returns:
        dict: k-mer와 그 빈도수의 딕셔너리
    """
    kmer_counts = {}
    for kmer in kmers:
        kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
    return kmer_counts


def main():
    """메인 함수: command-line arguments를 처리하고 k-mer를 생성합니다."""
    
    parser = argparse.ArgumentParser(
        description="입력받은 문자열에서 모든 k-mer를 생성하고 출력합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python3 kmer_generator.py ATCGATCG 3
  python3 kmer_generator.py "HELLO WORLD" 4 --unique
  python3 kmer_generator.py AGCTTAGC 2 --count
        """
    )
    
    parser.add_argument("sequence", help="입력 문자열 (DNA 서열, 텍스트 등)")
    parser.add_argument("k", type=int, help="k-mer의 길이 (양의 정수)")
    parser.add_argument("--unique", "-u", action="store_true", 
                       help="중복 제거된 고유한 k-mer만 출력")
    parser.add_argument("--count", "-c", action="store_true",
                       help="각 k-mer의 빈도수도 함께 출력")
    parser.add_argument("--sort", "-s", action="store_true",
                       help="k-mer를 알파벳 순으로 정렬하여 출력")
    
    # 인수가 없으면 도움말 출력
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    try:
        # K-mer 생성
        kmers = generate_kmers(args.sequence, args.k)
        
        # 결과 출력
        print(f"입력 문자열: {args.sequence}")
        print(f"문자열 길이: {len(args.sequence)}")
        print(f"k-mer 길이: {args.k}")
        print(f"총 k-mer 개수: {len(kmers)}")
        print("-" * 40)
        
        if args.count:
            # 빈도수와 함께 출력
            kmer_counts = count_kmers(kmers)
            if args.sort:
                sorted_kmers = sorted(kmer_counts.items())
            else:
                sorted_kmers = kmer_counts.items()
            
            print("k-mer (빈도수):")
            for kmer, count in sorted_kmers:
                print(f"  {kmer} ({count})")
            
            print(f"\n고유한 k-mer 개수: {len(kmer_counts)}")
            
        elif args.unique:
            # 중복 제거된 k-mer만 출력
            unique_kmers = list(set(kmers))
            if args.sort:
                unique_kmers.sort()
            
            print("고유한 k-mer들:")
            for i, kmer in enumerate(unique_kmers, 1):
                print(f"  {i:2d}. {kmer}")
            
            print(f"\n고유한 k-mer 개수: {len(unique_kmers)}")
            
        else:
            # 모든 k-mer 순서대로 출력
            if args.sort:
                display_kmers = sorted(kmers)
            else:
                display_kmers = kmers
            
            print("모든 k-mer들:")
            for i, kmer in enumerate(display_kmers, 1):
                print(f"  {i:2d}. {kmer}")
        
        # 위치 정보도 출력 (정렬하지 않은 경우만)
        if not args.sort and not args.unique and not args.count:
            print(f"\n위치별 k-mer:")
            for i, kmer in enumerate(kmers):
                print(f"  위치 {i}: {kmer}")
        
    except ValueError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
