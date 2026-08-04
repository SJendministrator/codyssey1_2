"""
Quiz Game Runner Module
- 퀴즈 진행, 점수 계산(80+20 가중치 알고리즘), CRUD 로직, 안전 입력 처리 담당
"""

import random
from datetime import datetime
from quiz import Quiz


class QuizGameRunner:
    def __init__(self, quizzes, best_score, history, storage_manager):
        self.quizzes = quizzes
        self.best_score = best_score
        self.history = history
        self.storage = storage_manager

    def safe_input(self, prompt=""):
        """입력 중단(Ctrl+C / Ctrl+D) 발생 시 안전하게 처리"""
        try:
            val = input(prompt)
            return val.strip() if val is not None else ""
        except (KeyboardInterrupt, EOFError):
            print("\n\n[알림] 사용자에 의해 입력이 중단되었습니다. 메뉴로 돌아갑니다.")
            return None

    def play_quiz(self):
        """퀴즈 풀기 모드 (100점 만점 가중치 점수 산출)"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        name_input = self.safe_input("\n플레이어 이름을 입력하세요: ")
        if name_input is None:
            return
        player_name = name_input if name_input else "익명"

        total_avail = len(self.quizzes)
        print(f"현재 등록된 총 퀴즈 수: {total_avail}개")

        # 풀 문제 수 입력
        while True:
            cnt_str = self.safe_input(f"풀 문제 수를 입력하세요 (1~{total_avail}): ")
            if cnt_str is None:
                return
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

        # 퀴즈 진행 루프
        for idx, quiz in enumerate(selected_quizzes, 1):
            quiz.display(idx)
            hint_used = False

            while True:
                u_input = self.safe_input("\n답 선택 (1-4, 'h': 힌트): ")
                if u_input is None:
                    return
                u_input = u_input.lower()

                # 힌트 처리
                if u_input == "h":
                    raw_hint = getattr(quiz, "hint", None)
                    hint_text = raw_hint.strip() if isinstance(raw_hint, str) else ""

                    if not hint_text:
                        print("[힌트] 이 문제에는 등록된 힌트가 없습니다.")
                        continue

                    if not hint_used:
                        print(f"[힌트] {hint_text}")
                        print("※ 힌트를 사용했으므로 정답 시 0.5점만 인정됩니다.")
                        hint_used = True
                    else:
                        print(f"[힌트] (이미 확인한 힌트) {hint_text}")
                    continue

                # 정답 선택 검증
                try:
                    choice = int(u_input)
                    if 1 <= choice <= len(quiz.options):
                        break
                    print("[오류] 선택지 범위(1~4) 내의 숫자를 입력하세요.")
                except ValueError:
                    print("[오류] 숫자(1~4) 또는 'h'를 입력하세요.")

            # 채점
            if quiz.is_correct(choice):
                pts = 0.5 if hint_used else 1.0
                earned_score += pts
                print(f">> 정답입니다! (+{pts}점)")
            else:
                correct_opt = quiz.options[quiz.answer - 1]
                print(f">> 틀렸습니다. (정답: {quiz.answer}번 - {correct_opt})")

        # --- [핵심] 점수 산출 알고리즘 (기본 80점 + 보너스 20점) ---
        accuracy_ratio = earned_score / quiz_count
        base_score = accuracy_ratio * 80.0
        volume_bonus = (quiz_count / total_avail) * 20.0
        final_score = round(base_score + volume_bonus, 1)
        accuracy_pct = round(accuracy_ratio * 100, 1)

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\n" + "-" * 40)
        print(f"퀴즈 완료! 최종 점수: {final_score}점 / 100점")
        print(f"- 순수 정답률 : {accuracy_pct}% ({earned_score}/{quiz_count}개)")
        print(f"- 점수 구성   : 기본 정답 점수 {round(base_score, 1)}점 + 문항 가중치 {round(volume_bonus, 1)}점")

        if final_score > self.best_score:
            print(f"[축하합니다] 최고 점수 갱신! (이전 기록: {self.best_score}점 -> 신기록: {final_score}점)")
            self.best_score = final_score
        else:
            print(f"현재 최고 점수: {self.best_score}점")
        print("-" * 40)

        # 히스토리 기록 및 자동 저장
        record = {
            "datetime": now_str,
            "name": player_name,
            "score": final_score,
            "earned_points": earned_score,
            "total_count": quiz_count,
        }
        self.history.append(record)
        self.storage.save_state(self.quizzes, self.best_score, self.history)

    def list_quizzes(self):
        """퀴즈 목록 출력"""
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n--- 전체 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"{idx:03d}. [{quiz.category}] {quiz.question}")

    def add_quiz(self):
        """새 퀴즈 추가"""
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
            category or "일반",
            question,
            options,
            answer,
            hint or "힌트가 없습니다."
        )
        self.quizzes.append(new_quiz)
        self.storage.save_state(self.quizzes, self.best_score, self.history)
        print("\n[성공] 새 퀴즈가 등록되었습니다!")

    def delete_quiz(self):
        """퀴즈 삭제"""
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
                    self.storage.save_state(self.quizzes, self.best_score, self.history)
                    print(f"\n[성공] '{target.question}' 퀴즈가 삭제되었습니다.")
                    break
                print("[오류] 올바른 문제 번호를 입력하세요.")
            except ValueError:
                print("[오류] 숫자를 입력하세요.")

    def show_history(self):
        """최고 점수 및 기록 조회"""
        print(f"\n[기록] 현재 최고 점수: {self.best_score}점")
        if not self.history:
            print("[알림] 아직 플레이 기록이 없습니다.")
            return

        print("\n--- 전체 게임 히스토리 ---")
        for idx, rec in enumerate(self.history, 1):
            dt = rec.get("datetime", "-")
            name = rec.get("name", "익명")
            score = rec.get("score", 0)
            pts = rec.get("earned_points", 0)
            cnt = rec.get("total_count", 0)
            print(f"{idx:02d}. [{dt}] {name} - {score}점 (획득: {pts}/{cnt}개)")