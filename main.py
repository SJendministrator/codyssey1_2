# main.py
from quiz import DEFAULT_QUIZZES

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

def play_quiz(quizzes):
    """퀴즈 풀기 메인 로직"""
    if not quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다.")
        return

    print("\n🚀 과학·공학 퀴즈를 시작합니다!")
    score = 0
    total = len(quizzes)

    for idx, quiz in enumerate(quizzes, 1):
        quiz.display(idx)
        
        # 사용자 답안 입력 및 예외 처리
        while True:
            try:
                user_input = input("\n답을 선택하세요 (1-4): ").strip()
                choice = int(user_input)
                if 1 <= choice <= len(quiz.options):
                    break
                else:
                    print("⚠️ 선택지 범위 안의 숫자를 입력해 주세요.")
            except ValueError:
                print("⚠️ 숫자만 입력할 수 있습니다.")

        # 정답 확인
        if quiz.is_correct(choice):
            print("✅ 정답입니다!")
            score += 1
        else:
            correct_option = quiz.options[quiz.answer - 1]
            print(f"❌ 틀렸습니다. (정답: {quiz.answer}번 - {correct_option})")

    # 결과 출력
    print("\n" + "-" * 40)
    print(f"🎉 퀴즈 종료! 최종 점수: {score} / {total}점 ({int(score/total*100)}점)")
    print("-" * 40)

def main():
    # 퀴즈 목록 로드 (초기 데이터)
    quizzes = DEFAULT_QUIZZES.copy()

    while True:
        show_menu()
        choice = input("원하는 메뉴 번호를 입력하세요 (1-5): ").strip()
        
        if choice == '1':
            play_quiz(quizzes)
        elif choice == '2':
            print("\n[!] 퀴즈 목록 보기 기능 준비 중...")
        elif choice == '3':
            print("\n[!] 퀴즈 추가 기능 준비 중...")
        elif choice == '4':
            print("\n[!] 점수 및 기록 보기 기능 준비 중...")
        elif choice == '5':
            print("\n👋 게임을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    main()