#!/usr/bin/env python3
"""
Edit Distance Calculator (Substitution Only)
길이가 같은 두 문자열 간의 edit distance를 계산합니다.
indel(insertion/deletion)은 고려하지 않고 substitution만 계산합니다.
"""

import sys
import argparse


def calculate_edit_distance(str1, str2):
    """
    길이가 같은 두 문자열 간의 edit distance를 계산합니다.
    indel을 고려하지 않고 substitution만 계산합니다.
    
    Args:
        str1 (str): 첫 번째 문자열
        str2 (str): 두 번째 문자열
    
    Returns:
        int: edit distance (다른 위치의 개수)
    
    Raises:
        ValueError: 두 문자열의 길이가 다른 경우
    """
    if len(str1) != len(str2):
        raise ValueError(f"문자열 길이가 다릅니다: {len(str1)} != {len(str2)}")
    
    # 각 위치에서 문자가 다른 경우의 수를 세기
    distance = 0
    differences = []
    
    for i, (char1, char2) in enumerate(zip(str1, str2)):
        if char1 != char2:
            distance += 1
            differences.append(f"위치 {i}: '{char1}' -> '{char2}'")
    
    return distance, differences


def main():
    """메인 함수: command-line arguments를 처리하고 edit distance를 계산합니다."""
    
    parser = argparse.ArgumentParser(
        description="길이가 같은 두 문자열 간의 edit distance를 계산합니다 (substitution only).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python3 edit_distance.py ATCG ATGG
  python3 edit_distance.py "hello world" "hello earth"
        """
    )
    
    parser.add_argument("string1", help="첫 번째 문자열")
    parser.add_argument("string2", help="두 번째 문자열")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="자세한 정보 출력 (차이점 위치 표시)")
    
    # 인수가 없으면 도움말 출력
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    try:
        # Edit distance 계산
        distance, differences = calculate_edit_distance(args.string1, args.string2)
        
        # 결과 출력
        print(f"문자열 1: {args.string1}")
        print(f"문자열 2: {args.string2}")
        print(f"길이: {len(args.string1)}")
        print(f"Edit Distance: {distance}")
        
        if args.verbose and differences:
            print(f"\n차이점 ({len(differences)}개):")
            for diff in differences:
                print(f"  {diff}")
        elif differences:
            print(f"차이점: {len(differences)}개")
        
        # 유사도 계산 및 출력
        if len(args.string1) > 0:
            similarity = (len(args.string1) - distance) / len(args.string1) * 100
            print(f"유사도: {similarity:.1f}%")
        
    except ValueError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
