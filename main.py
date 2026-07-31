# main.py

def show_menu():
    print("\n" + "=" * 40)
    print(" 🔬 Science & Engineering Quiz Game")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 목록 보기")
    print("3. 새 퀴즈 추가하기")
    print("4. 점수 및 기록 보기")
    print("5. 게임 종료")
    print("=" * 40)

def main():
    while True:
        show_menu()
        choice = input("원하는 메뉴 번호를 입력하세요 (1-5): ").strip()
        
        if choice == '1':
            print("\n[!] 퀴즈 풀기 기능 준비 중...")
        elif choice == '2':
            print("\n[!] 퀴즈 목록 보기 기능 준비 중...")
        elif choice == '3':
            print("\n[!] 퀴즈 추가 기능 준비 중...")
        elif choice == '4':
            print("\n[!] 점수 및 기록 보기 기능 준비 중...")
        elif choice == '5':
            print("\n게임을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            print("\n잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    main():