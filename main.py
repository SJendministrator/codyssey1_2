# main.py
import json
import os
import random
from datetime import datetime
from quiz import Quiz

STATE_FILE = "state.json"

# 기본 퀴즈 데이터 (state.json이 없거나 손상되었을 때 자동 복구용)
DEFAULT_QUIZZES = [
    {
        "question": "파이썬에서 리스트의 맨 뒤에 새로운 요소를 추가할 때 사용하는 메서드는?",
        "options": ["add()", "append()", "insert()", "push()"],
        "answer": 2,
        "category": "프로그래밍",
        "hint": "a로 시작하는 6글자 단어입니다."
    },
    {
        "question": "다음 중 파이썬의 불변(Immutable) 시퀀스 자료형은?",
        "options": ["list", "dict", "set", "tuple"],
        "answer": 4,
        "category": "프로그래밍",
        "hint": "소괄호()를 사용하여 선언합니다."
    },
    {
        "question": "Git에서 현재 작업 상태와 커밋되지 않은 변경사항을 확인하는 명령어는?",
        "options": ["git log", "git status", "git diff", "git check"],
        "answer": 2,
        "category": "Git",
        "hint": "상태를 뜻하는 영어 단어입니다."
    },
    {
        "question": "프로세스 실행 중 무한 루프나 강제 종료 명령(Ctrl+C)이 발생시킬 수 있는 예외는?",
        "options": ["ValueError", "KeyError", "KeyboardInterrupt", "TypeError"],
        "answer": 3,
        "category": "프로그래밍",
        "hint": "키보드 중단이라는 뜻을 가집니다."
    },
    {
        "question": "JSON 형식에서 데이터를 주고받을 때 기본이 되는 구조는?",
        "options": ["Key-Value 쌍", "Array 단독", "Binary 데이터", "XML 태그"],
        "answer": 1,
        "category": "컴퓨터공학",
        "hint": "파이썬의 dict(딕셔너리)와 유사합니다."
    }
]

class QuizGame:
    def __init__(self, state_file=STATE_FILE):
        self.state_file = state_file
        self.quizzes = []
        self.best_score = 0.0
        self.history = []
        self.load_state()

    def safe_input(self, prompt=""):
        """Ctrl+C 또는 EOF 발생 시 비정상 종료되지 않고 안전하게 처리하는 입력 함수"""
        try:
            return input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n[알림] 입력이 중단되었습니다. 안전하게 메인 메뉴로 돌아가거나 종료합니다.")
            return None

    def load_state(self):
        """state.json 파일 읽기 (없거나 손상 시 기본 데이터로 복구)"""
        if not os.path.exists(self.state_file):
            print(f"[알림] {self.state_file} 파일이 없어 기본 퀴즈 데이터로 생성합니다.")
            self.reset_to_default()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = float(data.get("best_score", 0.0))
                self.history = data.get("history", [])
                
                if not self.quizzes:
                    print("[알림] 퀴즈 데이터가 비어있어 기본 퀴즈로 복구합니다.")
                    self.reset_to_default()
        except Exception as e:
            print(f"[경고] 파일이 손상되었거나 읽기 오류가 발생했습니다 ({e}). 기본 데이터로 복구합니다.")
            self.reset_to_default()

    def reset_to_default(self):
        """기본 퀴즈 데이터로 초기화 및 저장"""
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = 0.0
        self.history = []
        self.save_state()

    def save_state(self):
        """state.json에 UTF-8로 저장"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[오류] 파일 저장 실패: {e}")

    def show_menu(self):
        print("\n" + "=" * 40)
        print(" Science & Engineering Quiz Game")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 목록 보기")
        print("3. 새 퀴즈 추가하기")
        print("4. 퀴즈 삭제하기")
        print("5. 점수 및 히스토리 확인")
        print("6. 게임 종료")
        print("=" * 40)

    def play_quiz(self):
        if not self.quizzes:
            print("\n[알림] 출제할 퀴즈가 없습니다.")
            return

        name_input = self.safe_input("\n플레이어 이름을 입력하세요: ")
        if name_input is None: return
        player_name = name_input if name_input else "익명"

        total_avail = len(self.quizzes)
        print(f"현재 등록된 총 퀴즈 수: {total_avail}개")

        while True:
            cnt_str = self.safe_input(f"풀 문제 수를 입력하세요 (1~{total_avail}): ")
            if cnt_str is None: return
            try:
                quiz_count = int(cnt_str)
                if 1 <= quiz_count <= total_avail:
                    break
                print(f"[오류] 1에서 {total_avail} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("[오류] 올바른 숫자를 입력해주세요.")

        selected_quizzes = random.sample(self.quizzes, quiz_count)
        earned_score = 0.0

        print(f"\n--- {player_name} 님의 퀴즈 시작 (총 {quiz_count}문항) ---")

        for idx, quiz in enumerate(selected_quizzes, 1):
            quiz.display(idx)
            hint_used = False

            while True:
                u_input = self.safe_input("\n답 선택 (1-4, 'h': 힌트): ")
                if u_input is None: return
                u_input = u_input.lower()

                if u_input == 'h':
                    if not hint_used:
                        print(f"💡 [힌트]: {quiz.hint}")
                        print("※ 힌트 사용 시 정답 점수는 0.5점만 인정됩니다.")
                        hint_used = True
                    else:
                        print("💡 [힌트]: 이미 힌트를 확인하셨습니다.")
                    continue

                try:
                    choice = int(u_input)
                    if 1 <= choice <= len(quiz.options):
                        break
                    print("[오류] 선택지 범위(1~4) 내의 숫자를 입력하세요.")
                except ValueError:
                    print("[오류] 숫자(1~4) 또는 'h'를 입력하세요.")

            if quiz.is_correct(choice):
                pts = 0.5 if hint_used else 1.0
                earned_score += pts
                print(f">> 정답입니다! (+{pts}점)")
            else:
                correct_opt = quiz.options[quiz.answer - 1]
                print(f">> 틀렸습니다. (정답: {quiz.answer}번 - {correct_opt})")

        final_pct = round((earned_score / quiz_count) * 100, 1)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "-" * 40)
        print(f"퀴즈 완료! 점수: {final_pct}점 (획득: {earned_score}/{quiz_count}점)")
        
        # 최고 점수 갱신 확인
        if final_pct > self.best_score:
            print(f"🎉 최고 점수 갱신! (이전 최고 점수: {self.best_score}점 -> 신기록: {final_pct}점)")
            self.best_score = final_pct
        else:
            print(f"현재 최고 점수: {self.best_score}점")
        print("-" * 40)

        record = {
            "datetime": now_str,
            "name": player_name,
            "score": final_pct,
            "earned_points": earned_score,
            "total_count": quiz_count
        }
        self.history.append(record)
        self.save_state()

    def list_quizzes(self):
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 전체 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"{idx:03d}. [{quiz.category}] {quiz.question}")

    def add_quiz(self):
        print("\n--- 새 퀴즈 추가 ---")
        category = self.safe_input("분야 입력: ")
        if category is None: return
        question = self.safe_input("질문 입력: ")
        if question is None: return

        options = []
        for i in range(1, 5):
            opt = self.safe_input(f"보기 {i}: ")
            if opt is None: return
            options.append(opt)

        while True:
            ans_str = self.safe_input("정답 번호 (1-4): ")
            if ans_str is None: return
            try:
                answer = int(ans_str)
                if 1 <= answer <= 4:
                    break
                print("[오류] 1~4 사이 숫자를 입력하세요.")
            except ValueError:
                print("[오류] 숫자를 입력하세요.")

        hint = self.safe_input("힌트 입력 (선택, 엔터 시 생략): ")
        if hint is None: return

        new_quiz = Quiz(question, options, answer, category or "일반", hint or "힌트가 없습니다.")
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n[성공] 새 퀴즈가 저장되었습니다!")

    def delete_quiz(self):
        if not self.quizzes:
            print("\n[알림] 삭제할 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        while True:
            del_str = self.safe_input("\n삭제할 퀴즈 번호 입력 (취소: 0): ")
            if del_str is None: return
            try:
                del_idx = int(del_str)
                if del_idx == 0:
                    print("삭제를 취소합니다.")
                    return
                if 1 <= del_idx <= len(self.quizzes):
                    target = self.quizzes.pop(del_idx - 1)
                    self.save_state()
                    print(f"\n[성공] '{target.question}' 퀴즈가 삭제되었습니다.")
                    break
                print("[오류] 올바른 문제 번호를 입력하세요.")
            except ValueError:
                print("[오류] 숫자를 입력하세요.")

    def show_history(self):
        print(f"\n🏆 현재 최고 점수: {self.best_score}점")
        if not self.history:
            print("[알림] 아직 플레이 기록이 없습니다.")
            return

        print("\n--- 전체 게임 히스토리 ---")
        for idx, rec in enumerate(self.history, 1):
            dt = rec.get("datetime", "-")
            name = rec.get("name", "익명")
            score = rec.get("score", 0)
            print(f"{idx:02d}. [{dt}] {name} - {score}점")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = self.safe_input("메뉴 선택 (1-6): ")
                if choice is None or choice == '6':
                    print("\n게임을 안전하게 종료합니다. 이용해 주셔서 감사합니다.")
                    break
                elif choice == '1':
                    self.play_quiz()
                elif choice == '2':
                    self.list_quizzes()
                elif choice == '3':
                    self.add_quiz()
                elif choice == '4':
                    self.delete_quiz()
                elif choice == '5':
                    self.show_history()
                else:
                    print("\n[오류] 1~6 사이의 번호를 입력해주세요.")
        except Exception as e:
            print(f"\n[예외 발생] 예상치 못한 오류가 발생하여 데이터를 안전하게 저장 후 종료합니다: {e}")
            self.save_state()

if __name__ == "__main__":
    game = QuizGame()
    game.run()