# main.py
import json
import os
import random
from quiz import Quiz

STATE_FILE = "state.json"

class QuizGame:
    """게임 전체의 데이터 관리, 데이터 저장/불러오기, UI 진행을 담당하는 클래스"""
    
    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file
        self.quizzes = []
        self.history = []
        self.load_state()

    def load_state(self):
        """state.json 파일에서 퀴즈 목록과 도전자 기록을 로드 (파일이 없거나 손상 시 예외 처리)"""
        if not os.path.exists(self.state_file):
            print(f"[알림] {self.state_file} 파일이 존재하지 않아 기본 상태로 시작합니다.")
            self.history = []
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.history = data.get("history", [])
        except Exception as e:
            print(f"[경고] {self.state_file} 로드 중 오류 발생 ({e}). 기본 상태로 초기화합니다.")
            self.history = []

    def save_state(self):
        """현재 퀴즈 목록과 도전자 기록을 state.json 파일에 UTF-8 인코딩으로 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "history": self.history
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[오류] 데이터 저장 실패: {e}")

    def show_menu(self):
        """메인 메뉴 출력"""
        print("\n" + "=" * 40)
        print(" Science & Engineering Quiz Game")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 목록 보기")
        print("3. 새 퀴즈 추가하기")
        print("4. 점수 및 기록 보기")
        print("5. 게임 종료")
        print("=" * 40)

    def play_quiz(self):
        """등록된 퀴즈 중 랜덤으로 문제를 출제하고 진행"""
        if not self.quizzes:
            print("\n[경고] 등록된 퀴즈가 없습니다.")
            return

        player_name = input("\n플레이어 이름을 입력해 주세요: ").strip()
        if not player_name:
            player_name = "익명"

        sample_count = min(10, len(self.quizzes))
        selected_quizzes = random.sample(self.quizzes, sample_count)

        print(f"\n--- {player_name} 님의 퀴즈 풀기 (총 {sample_count}문항) ---")
        score = 0

        for idx, quiz in enumerate(selected_quizzes, 1):
            quiz.display(idx)
            
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

            if quiz.is_correct(choice):
                print(">> 정답입니다!")
                score += 1
            else:
                correct_option = quiz.options[quiz.answer - 1]
                print(f">> 틀렸습니다. (정답: {quiz.answer}번 - {correct_option})")

        final_score = int(score / sample_count * 100)
        print("\n" + "-" * 40)
        print(f"퀴즈 종료! 최종 점수: {score} / {sample_count}점 ({final_score}점)")
        print("-" * 40)

        record = {
            "name": player_name,
            "score": final_score,
            "correct_count": score,
            "total_count": sample_count
        }
        self.history.append(record)
        self.save_state()
        print(f"[시스템] 플레이 기록이 {self.state_file}에 저장되었습니다.")

    def list_quizzes(self):
        """등록된 전체 퀴즈 목록 보기"""
        if not self.quizzes:
            print("\n[경고] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 전체 퀴즈 목록 (총 {len(self.quizzes)}문제) ---")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"{idx:03d}. [{quiz.category}] {quiz.question}")

    def add_quiz(self):
        """새 퀴즈 추가 및 state.json 저장"""
        print("\n--- 새 퀴즈 추가 ---")
        category = input("분야를 입력하세요 (예: 컴퓨터공학): ").strip()
        question = input("질문을 입력하세요: ").strip()
        
        options = []
        for i in range(1, 5):
            opt = input(f"보기 {i}: ").strip()
            options.append(opt)
        
        while True:
            try:
                answer = int(input("정답 번호를 입력하세요 (1-4): ").strip())
                if 1 <= answer <= 4:
                    break
                else:
                    print("[오류] 1에서 4 사이의 숫자를 입력해야 합니다.")
            except ValueError:
                print("[오류] 숫자만 입력해 주세요.")

        new_quiz = Quiz(question, options, answer, category)
        self.quizzes.append(new_quiz)
        self.save_state()
        print(f"\n[성공] 새 퀴즈가 성공적으로 추가되었으며 {self.state_file}에 저장되었습니다!")

    def show_history(self):
        """누적 기록 및 점수 보기"""
        if not self.history:
            print("\n[알림] 아직 저장된 점수 기록이 없습니다.")
            return

        print("\n--- 점수 및 누적 기록 ---")
        for idx, rec in enumerate(self.history, 1):
            print(f"{idx}. {rec['name']} - {rec['score']}점 ({rec['correct_count']}/{rec['total_count']} 정답)")

    def run(self):
        """게임 실행 메인 루프"""
        while True:
            self.show_menu()
            choice = input("원하는 메뉴 번호를 입력하세요 (1-5): ").strip()
            
            if choice == '1':
                self.play_quiz()
            elif choice == '2':
                self.list_quizzes()
            elif choice == '3':
                self.add_quiz()
            elif choice == '4':
                self.show_history()
            elif choice == '5':
                print("\n게임을 종료합니다. 이용해 주셔서 감사합니다.")
                break
            else:
                print("\n[오류] 잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()