# main.py
from quiz import Quiz, DEFAULT_QUIZZES

def show_menu():
    """메인 메뉴 옵션을 화면에 출력"""
    print("\n" + "=" * 40)
    print(" Science & Engineering Quiz Game")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 목록 보기")
    print("3. 새 퀴즈 추가하기")
    print("4. 점수 및 기록 보기")
    print("5. 게임 종료")
    print("=" * 40)

def play_quiz(quizzes):
    """등록된 퀴즈를 순서대로 진행하고 정답률 및 점수를 계산"""
    if not quizzes:
        print("\n[경고] 등록된 퀴즈가 없습니다.")
        return

    print("\n--- 퀴즈 풀기 시작 ---")
    score = 0
    total = len(quizzes)

    for idx, quiz in enumerate(quizzes, 1):
        quiz.display(idx)
        
        # 사용자가 올바른 범위의 숫자만 입력하도록 예외 처리 루프
        while True:
            try:
                user_input = input("\n답을 선택하세요 (1-4): ").strip()
                choice = int(user_input)
                if 1 <= choice <= len(quiz.options):
                    break
                else:
                    print("[오류] 선택지 범위 안의 숫자를 입력해 주세요.")
            except ValueError:
                print("[오류] 숫자만 입력할 수 있습니다.")

        # 정답 여부 판별
        if quiz.is_correct(choice):
            print(">> 정답입니다!")
            score += 1
        else:
            correct_option = quiz.options[quiz.answer - 1]
            print(f">> 틀렸습니다. (정답: {quiz.answer}번 - {correct_option})")

    # 최종 결과 요약 출력
    print("\n" + "-" * 40)
    print(f"퀴즈 종료! 최종 점수: {score} / {total}점 ({int(score/total*100)}점)")
    print("-" * 40)

def list_quizzes(quizzes):
    """현재 시스템에 등록되어 있는 모든 퀴즈 목록을 출력"""
    if not quizzes:
        print("\n[경고] 등록된 퀴즈가 없습니다.")
        return

    print("\n--- 전체 퀴즈 목록 ---")
    for idx, quiz in enumerate(quizzes, 1):
        print(f"{idx}. [{quiz.category}] {quiz.question} (정답: {quiz.answer}번)")

def add_quiz(quizzes):
    """사용자로부터 분야, 질문, 보기, 정답을 입력받아 새로운 Quiz 객체 추가"""
    print("\n--- 새 퀴즈 추가 ---")
    category = input("분야를 입력하세요 (예: 컴퓨터공학): ").strip()
    question = input("질문을 입력하세요: ").strip()
    
    # 4개의 선택지 입력 받기
    options = []
    for i in range(1, 5):
        opt = input(f"보기 {i}: ").strip()
        options.append(opt)
    
    # 정답 번호 입력 및 예외 처리
    while True:
        try:
            answer = int(input("정답 번호를 입력하세요 (1-4): ").strip())
            if 1 <= answer <= 4:
                break
            else:
                print("[오류] 1에서 4 사이의 숫자를 입력해야 합니다.")
        except ValueError:
            print("[오류] 숫자만 입력해 주세요.")

    # 입력받은 정보로 new_quiz 객체 생성 후 목록에 추가
    new_quiz = Quiz(question, options, answer, category)
    quizzes.append(new_quiz)
    print("\n[성공] 새 퀴즈가 성공적으로 추가되었습니다!")

def main():
    """프로그램 시작점: 초기 데이터 로드 및 메뉴 분기 처리"""
    quizzes = DEFAULT_QUIZZES.copy()

    while True:
        show_menu()
        choice = input("원하는 메뉴 번호를 입력하세요 (1-5): ").strip()
        
        if choice == '1':
            play_quiz(quizzes)
        elif choice == '2':
            list_quizzes(quizzes)
        elif choice == '3':
            add_quiz(quizzes)
        elif choice == '4':
            print("\n[!] 점수 및 기록 보기 기능 준비 중...")
        elif choice == '5':
            print("\n게임을 종료합니다. 이용해 주셔서 감사합니다.")
            break
        else:
            print("\n[오류] 잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    main()