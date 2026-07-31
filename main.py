# main.py
"""
과학/공학 퀴즈 게임 (Science & Engineering Quiz Game)
주요 기능: 퀴즈 출제, 추가, 삭제, 목록 조회, 점수 저장 및 기록 관리
특징: 예외 처리 강화(KeyboardInterrupt, EOFError 대응), JSON 데이터 영속성 유지
"""

import json
import os
import random
from datetime import datetime
from quiz import Quiz

# 데이터 저장 파일 경로 (프로젝트 루트 디렉토리)
STATE_FILE = "state.json"

# 기본 퀴즈 데이터셋 (state.json이 없거나 손상되었을 경우 자동 복구용 표준 데이터)
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
    """게임 전체 로직, CLI 상태 제어 및 데이터 입출력을 담당하는 컨트롤러 클래스"""

    def __init__(self, state_file=STATE_FILE):
        """초기화 메서드: 파일 경로 지정 및 기존 데이터 로드"""
        self.state_file = state_file
        self.quizzes = []
        self.best_score = 0.0
        self.history = []
        self.load_state()

    def safe_input(self, prompt=""):
        """
        사용자 입력을 안전하게 처리하는 래퍼 메서드.
        Ctrl+C(KeyboardInterrupt) 또는 Ctrl+D/EOFError 발생 시 프로그램 튕김 방지.
        """
        try:
            val = input(prompt)
            return val.strip() if val is not None else ""
        except (KeyboardInterrupt, EOFError):
            print("\n\n[알림] 사용자에 의해 입력이 중단되었습니다. 메인 메뉴로 이동합니다.")
            return None

    def load_state(self):
        """
        state.json 파일로부터 퀴즈 및 게임 기록 로드.
        파일이 없거나 JSON 포맷이 깨진 경우 기본 데이터셋으로 안전 복구 수행.
        """
        if not os.path.exists(self.state_file):
            print(f"[알림] {self.state_file} 파일이 존재하지 않아 기본 데이터로 초기화합니다.")
            self.reset_to_default()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Dict 리스트를 Quiz 객체 리스트로 변환
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = float(data.get("best_score", 0.0))
                self.history = data.get("history", [])

                # 파일 내용이 비어있는 경우 복구
                if not self.quizzes:
                    print("[알림] 불러온 퀴즈가 없어 기본 문제로 복구합니다.")
                    self.reset_to_default()
        except Exception as e:
            print(f"[경고] 데이터 로드 실패({e}). 기본 데이터로 복구합니다.")
            self.reset_to_default()

    def reset_to_default(self):
        """기본 퀴즈 데이터셋으로 객체 상태를 초기화하고 파일에 저장"""
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = 0.0
        self.history = []
        self.save_state()

    def save_state(self):
        """현재 퀴즈 목록, 최고 점수, 플레이 기록을 state.json 파일에 저장 (UTF-8 인코딩)"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[오류] 데이터 파일 저장 중 실패 발생: {e}")

    def show_menu(self):
        """메인 콘솔 메뉴 출력"""
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
        """퀴즈 실행 로직: 문제 수 선택, 랜덤 무작위 추출, 힌트 처리 및 점수 저장"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        name_input = self.safe_input("\n플레이어 이름을 입력하세요: ")
        if name_input is None:
            return
        player_name = name_input if name_input else "익명"

        total_avail = len(self.quizzes)
        print(f"현재 등록된 총 퀴즈 수: {total_avail}개")

        # 풀 문제 수 입력 검증 루프
        while True:
            cnt_str = self.safe_input(
                f"풀 문제 수를 입력하세요 (1~{total_avail}): "
            )
            if cnt_str is None:
                return
            try:
                quiz_count = int(cnt_str)
                if 1 <= quiz_count <= total_avail:
                    break
                print(f"[오류] 1에서 {total_avail} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("[오류] 올바른 숫자를 입력해주세요.")

        # random.sample을 이용한 무작위 퀴즈 추출
        selected_quizzes = random.sample(self.quizzes, quiz_count)
        earned_score = 0.0

        print(f"\n--- {player_name} 님의 퀴즈 시작 (총 {quiz_count}문항) ---")

        for idx, quiz in enumerate(selected_quizzes, 1):
            quiz.display(idx)
            hint_used = False

            # 답안 입력 및 힌트 처리 루프
            while True:
                u_input = self.safe_input("\n답 선택 (1-4, 'h': 힌트): ")
                if u_input is None:
                    return
                u_input = u_input.lower()

                # 힌트 기능 및 예외 방어 로직
                if u_input == "h":
                    raw_hint = getattr(quiz, "hint", None)
                    hint_text = (
                        raw_hint.strip() if isinstance(raw_hint, str) else ""
                    )

                    if not hint_text:
                        print("[힌트] 이 문제에는 등록된 힌트가 없습니다.")
                        continue

                    if not hint_used:
                        print(f"[힌트] {hint_text}")
                        print(
                            "※ 힌트를 사용했으므로 정답 시 0.5점만 인정됩니다."
                        )
                        hint_used = True
                    else:
                        print(f"[힌트] (이미 확인한 힌트) {hint_text}")
                    continue

                try:
                    choice = int(u_input)
                    if 1 <= choice <= len(quiz.options):
                        break
                    print("[오류] 선택지 범위(1~4) 내의 숫자를 입력하세요.")
                except ValueError:
                    print("[오류] 숫자(1~4) 또는 'h'를 입력하세요.")

            # 정답 판정 및 점수 계산
            if quiz.is_correct(choice):
                pts = 0.5 if hint_used else 1.0
                earned_score += pts
                print(f">> 정답입니다! (+{pts}점)")
            else:
                correct_opt = quiz.options[quiz.answer - 1]
                print(f">> 틀렸습니다. (정답: {quiz.answer}번 - {correct_opt})")

        # 100점 만점 기준 백분율 계산
        final_pct = round((earned_score / quiz_count) * 100, 1)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "-" * 40)
        print(
            f"퀴즈 완료! 점수: {final_pct}점 (획득: {earned_score}/{quiz_count}점)"
        )

        # 최고 점수 갱신 확인 및 저장
        if final_pct > self.best_score:
            print(
                f"[축하합니다] 최고 점수 갱신! (이전 최고 점수: {self.best_score}점 -> 신기록: {final_pct}점)"
            )
            self.best_score = final_pct
        else:
            print(f"현재 최고 점수: {self.best_score}점")
        print("-" * 40)

        # 기록 저장
        record = {
            "datetime": now_str,
            "name": player_name,
            "score": final_pct,
            "earned_points": earned_score,
            "total_count": quiz_count,
        }
        self.history.append(record)
        self.save_state()

    def list_quizzes(self):
        """저장된 전체 퀴즈 목록 출력"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 전체 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"{idx:03d}. [{quiz.category}] {quiz.question}")

    def add_quiz(self):
        """사용자 입력을 통한 신규 퀴즈 등록 기능"""
        print("\n--- 새 퀴즈 추가 ---")
        category = self.safe_input("분야 입력 (예: 컴퓨터공학): ")
        if category is None:
            return
        question = self.safe_input("질문 입력: ")
        if question is None:
            return

        options = []
        for i in range(1, 5):
            opt = self.safe_input(f"보기 {i}: ")
            if opt is None:
                return
            options.append(opt)

        while True:
            ans_str = self.safe_input("정답 번호 (1-4): ")
            if ans_str is None:
                return
            try:
                answer = int(ans_str)
                if 1 <= answer <= 4:
                    break
                print("[오류] 1~4 사이 숫자를 입력하세요.")
            except ValueError:
                print("[오류] 숫자를 입력하세요.")

        hint = self.safe_input("힌트 입력 (선택사항, 엔터 시 생략): ")
        if hint is None:
            return

        new_quiz = Quiz(
            question,
            options,
            answer,
            category or "일반",
            hint or "힌트가 없습니다.",
        )
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n[성공] 새 퀴즈가 등록되었습니다!")

    def delete_quiz(self):
        """퀴즈 삭제 기능 및 state.json 동기화"""
        if not self.quizzes:
            print("\n[알림] 삭제할 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        while True:
            del_str = self.safe_input("\n삭제할 퀴즈 번호 입력 (취소: 0): ")
            if del_str is None:
                return
            try:
                del_idx = int(del_str)
                if del_idx == 0:
                    print("삭제를 취소합니다.")
                    return
                if 1 <= del_idx <= len(self.quizzes):
                    target = self.quizzes.pop(del_idx - 1)
                    self.save_state()
                    print(
                        f"\n[성공] '{target.question}' 퀴즈가 삭제되었습니다."
                    )
                    break
                print("[오류] 올바른 문제 번호를 입력하세요.")
            except ValueError:
                print("[오류] 숫자를 입력하세요.")

    def show_history(self):
        """최고 점수 및 게임 플레이 전체 히스토리 출력"""
        print(f"\n[기록] 현재 최고 점수: {self.best_score}점")
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
        """프로그램의 메인 실행 루프"""
        try:
            while True:
                self.show_menu()
                choice = self.safe_input("메뉴 선택 (1-6): ")
                if choice is None or choice == "6":
                    print("\n게임을 안전하게 종료합니다. 이용해 주셔서 감사합니다.")
                    break
                elif choice == "1":
                    self.play_quiz()
                elif choice == "2":
                    self.list_quizzes()
                elif choice == "3":
                    self.add_quiz()
                elif choice == "4":
                    self.delete_quiz()
                elif choice == "5":
                    self.show_history()
                else:
                    print("\n[오류] 1~6 사이의 번호를 입력해주세요.")
        except Exception as e:
            print(f"\n[예외 발생] 안전 종료 후 데이터 저장: {e}")
            self.save_state()


if __name__ == "__main__":
    game = QuizGame()
    game.run()