#!/usr/bin/env python3
"""
fm_index.py
FM index를 계산하는 파이썬 프로그램

FM index는 Burrows-Wheeler Transform (BWT)과 suffix array를 기반으로 한 
압축된 full-text 인덱스 구조입니다.
"""

import sys
import argparse
from collections import defaultdict


class FMIndex:
    """
    FM Index를 구현하는 클래스
    """
    
    def __init__(self, text):
        """
        FM Index 객체를 초기화합니다.
        
        Args:
            text (str): 인덱싱할 텍스트
        """
        self.original_text = text
        self.text = text + '$'  # 종료 문자 추가
        self.suffix_array = []
        self.bwt = ""
        self.first_column = ""
        self.last_column = ""
        self.count_table = {}
        self.occurrence_table = {}
        
        # FM Index 구축
        self.build_fm_index()
    
    
    def build_suffix_array(self):
        """
        Suffix Array를 구축합니다.
        """
        print("Building Suffix Array...")
        
        # 모든 suffix와 그 시작 위치를 생성
        suffixes = []
        for i in range(len(self.text)):
            suffixes.append((self.text[i:], i))
        
        # 사전식 순서로 정렬
        suffixes.sort(key=lambda x: x[0])
        
        # suffix array는 정렬된 suffix들의 시작 위치
        self.suffix_array = [suffix[1] for suffix in suffixes]
        
        print(f"Suffix Array: {self.suffix_array}")
    
    
    def build_bwt(self):
        """
        Burrows-Wheeler Transform을 구축합니다.
        """
        print("\nBuilding Burrows-Wheeler Transform...")
        
        # BWT는 각 suffix의 마지막 문자 (즉, 원래 위치에서 한 칸 앞의 문자)
        bwt_chars = []
        for pos in self.suffix_array:
            if pos == 0:
                # 첫 번째 위치면 마지막 문자
                bwt_chars.append(self.text[-1])
            else:
                # 그 외에는 한 칸 앞의 문자
                bwt_chars.append(self.text[pos - 1])
        
        self.bwt = ''.join(bwt_chars)
        self.last_column = self.bwt  # BWT = Last column
        
        # First column은 BWT를 정렬한 것
        self.first_column = ''.join(sorted(self.bwt))
        
        print(f"BWT (Last Column): {self.bwt}")
        print(f"First Column: {self.first_column}")
    
    
    def build_count_table(self):
        """
        Count table을 구축합니다. (각 문자가 first column에서 시작하는 위치)
        """
        print("\nBuilding Count Table...")
        
        self.count_table = {}
        char_counts = defaultdict(int)
        
        # 각 문자의 first column에서의 시작 위치 계산
        for i, char in enumerate(self.first_column):
            if char not in self.count_table:
                self.count_table[char] = i
        
        print(f"Count Table: {self.count_table}")
    
    
    def build_occurrence_table(self):
        """
        Occurrence table을 구축합니다. (각 위치에서 각 문자의 누적 개수)
        """
        print("\nBuilding Occurrence Table...")
        
        # 문자별 누적 개수 테이블
        chars = sorted(set(self.text))
        self.occurrence_table = {char: [0] * (len(self.bwt) + 1) for char in chars}
        
        # 각 위치에서의 누적 개수 계산
        for i, char in enumerate(self.bwt):
            # 이전 위치의 개수를 복사
            for c in chars:
                self.occurrence_table[c][i + 1] = self.occurrence_table[c][i]
            
            # 현재 문자의 개수 증가
            self.occurrence_table[char][i + 1] += 1
        
        print("Occurrence Table:")
        for char in sorted(chars):
            print(f"  {char}: {self.occurrence_table[char]}")
    
    
    def build_fm_index(self):
        """
        전체 FM Index를 구축합니다.
        """
        print(f"Building FM Index for text: '{self.original_text}'")
        print(f"Text with end marker: '{self.text}'")
        print("=" * 60)
        
        self.build_suffix_array()
        self.build_bwt()
        self.build_count_table()
        self.build_occurrence_table()
        
        print("\n" + "=" * 60)
        print("FM Index construction completed!")
    
    
    def search(self, pattern):
        """
        FM Index를 사용하여 패턴을 검색합니다.
        
        Args:
            pattern (str): 검색할 패턴
        
        Returns:
            list: 패턴이 발견된 위치들의 리스트
        """
        print(f"\nSearching for pattern: '{pattern}'")
        
        if not pattern:
            return []
        
        # Backward search 알고리즘
        top = 0
        bottom = len(self.bwt) - 1
        
        # 패턴을 뒤에서부터 검색
        for i in range(len(pattern) - 1, -1, -1):
            char = pattern[i]
            
            if char not in self.count_table:
                print(f"Character '{char}' not found in text")
                return []
            
            # LF mapping을 사용하여 범위 업데이트
            top = self.count_table[char] + self.occurrence_table[char][top]
            bottom = self.count_table[char] + self.occurrence_table[char][bottom + 1] - 1
            
            print(f"After processing '{char}': top={top}, bottom={bottom}")
            
            if top > bottom:
                print(f"Pattern '{pattern}' not found")
                return []
        
        # 발견된 위치들을 suffix array에서 추출
        positions = []
        for i in range(top, bottom + 1):
            positions.append(self.suffix_array[i])
        
        positions.sort()
        print(f"Pattern '{pattern}' found at positions: {positions}")
        return positions
    
    
    def print_detailed_structure(self):
        """
        FM Index의 상세한 구조를 출력합니다.
        """
        print("\n" + "=" * 80)
        print("DETAILED FM INDEX STRUCTURE")
        print("=" * 80)
        
        print("\n1. Suffix Array and Suffixes:")
        print("Index | SA[i] | Suffix")
        print("-" * 30)
        for i, pos in enumerate(self.suffix_array):
            suffix = self.text[pos:] if pos < len(self.text) else "$"
            print(f"{i:5d} | {pos:5d} | {suffix}")
        
        print("\n2. BWT Construction:")
        print("Index | SA[i] | BWT[i] | First[i]")
        print("-" * 40)
        for i, pos in enumerate(self.suffix_array):
            bwt_char = self.bwt[i]
            first_char = self.first_column[i]
            print(f"{i:5d} | {pos:5d} | {bwt_char:6s} | {first_char}")
        
        print(f"\n3. Summary:")
        print(f"Original text: '{self.original_text}'")
        print(f"Text with $: '{self.text}'")
        print(f"BWT: '{self.bwt}'")
        print(f"First column: '{self.first_column}'")
        print(f"Suffix Array: {self.suffix_array}")


def main():
    """
    메인 함수: command-line arguments를 처리하고 FM Index를 구축합니다.
    """
    parser = argparse.ArgumentParser(
        description="FM Index 계산 프로그램",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python3 fm_index.py "banana"
  python3 fm_index.py "ATCGATCG" --search "ATG"
  python3 fm_index.py "hello world" --detailed
  python3 fm_index.py "ACGTACGT" --search "CG" --detailed
        """
    )
    
    parser.add_argument("text", help="FM Index를 구축할 문자열")
    parser.add_argument("-s", "--search", help="검색할 패턴")
    parser.add_argument("-d", "--detailed", action="store_true",
                       help="상세한 구조 정보 출력")
    
    # 인수가 없으면 도움말 출력
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # FM Index 구축
    fm_index = FMIndex(args.text)
    
    # 상세 정보 출력
    if args.detailed:
        fm_index.print_detailed_structure()
    
    # 패턴 검색
    if args.search:
        positions = fm_index.search(args.search)
        
        if positions:
            print(f"\n🎯 Success! Pattern '{args.search}' found at {len(positions)} location(s):")
            for pos in positions:
                # 컨텍스트와 함께 출력
                start = max(0, pos - 5)
                end = min(len(args.text), pos + len(args.search) + 5)
                context = args.text[start:end]
                
                # 패턴 부분 강조
                pattern_start = pos - start
                pattern_end = pattern_start + len(args.search)
                highlighted = (context[:pattern_start] + 
                             f"[{context[pattern_start:pattern_end]}]" + 
                             context[pattern_end:])
                
                print(f"  Position {pos}: ...{highlighted}...")
        else:
            print(f"\n❌ Pattern '{args.search}' not found in text")
    
    print(f"\n✅ FM Index construction completed for text: '{args.text}'")


if __name__ == "__main__":
    main()
