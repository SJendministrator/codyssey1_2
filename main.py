from storage import StorageManager
from game import QuizGameRunner  # 게임 실행부 모듈화

def main():
    storage = StorageManager()
    quizzes, best_score, history = storage.load_state()
    runner = QuizGameRunner(quizzes, best_score, history, storage)

    while True:
        print("\n" + "=" * 40)
        print(" Science & Engineering Quiz Game")
        print("=" * 40)
        print("1. 퀴즈 풀기\n2. 퀴즈 목록\n3. 퀴즈 추가\n4. 퀴즈 삭제\n5. 기록 확인\n6. 종료")
        print("=" * 40)
        
        choice = runner.safe_input("메뉴 선택 (1-6): ")
        if choice is None or choice == "6":
            print("\n게임을 종료합니다.")
            break
        elif choice == "1":
            runner.play_quiz()
        elif choice == "2":
            runner.list_quizzes()
        elif choice == "3":
            runner.add_quiz()
        elif choice == "4":
            runner.delete_quiz()
        elif choice == "5":
            runner.show_history()

if __name__ == "__main__":
    main()