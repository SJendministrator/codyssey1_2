# main.py
import json
import os
import random
from quiz import Quiz

# 상태 데이터 및 마스터 퀴즈 데이터 파일 경로
STATE_FILE = "state.json"
QUIZ_DATA_FILE = "quizzes_data.json"

def load_master_quizzes():
    """quizzes_data.json 파일에서 전체 퀴즈 목록을 읽어옴"""
    if not os.path.exists(QUIZ_DATA_FILE):
        print(f"[경고] {QUIZ_DATA_FILE} 파일이 없습니다.")
        return []
    
    try:
        with open(QUIZ_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Quiz.from_dict(q) for q in data]
    except Exception as e:
        print(f"[오류] 퀴즈 데이터 로드 실패: {e}")
        return []

def load_state():
    """state.json 파일이 존재하면 플레이 기록을 로드"""
    if not os.path.exists(STATE_FILE):
        initial_data = {"history": []}
        save_state_to_file(initial_data)
        return []

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("history", [])
    except Exception as e:
        print(f"[경고] 기록 파일 로드 중 오류 발생: {e}")
        return []

def save_state(history):
    """도전자 기록을 state.json 파일에 저장"""
    data = {"history": history}
    save_state_to_file(data)

def save_state_to_file(data):
    """실제 파일에 JSON 형식으로 쓰기 함수"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def show_menu():
    """메인 메뉴 옵션을 화면에 출력"""
    print("\n" + "=" * 40)
    print(" Science & Engineering Quiz Game")
    print("=" * 40)
    print("1. 퀴즈 풀기 (랜덤 10문항)")
    print("2. 전체 퀴즈 목록 보기")
    print("3. 새 퀴즈 추가하기")
    print("4. 점수 및 기록 보기")
    print("5. 게임 종료")
    print("=" * 40)

def play_quiz(quizzes, history):
    """등록된 전체 퀴즈 중 10문제를 랜덤 추출하여 진행"""
    if not quizzes:
        print("\n[경고] 등록된 퀴즈가 없습니다.")
        return

    player_name = input("\n플레이어 이름을 입력해 주세요: ").strip()
    if not player_name:
        player_name = "익명"

    # 전체 문항 중 최대 10문제를 무작위 선택 (문항 수가 10개 미만이면 전체 선택)
    sample_count = min(10, len(quizzes))
    selected_quizzes = random.sample(quizzes, sample_count)

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

    # 결과 및 점수 기록
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
    history.append(record)
    save_state(history)
    print("[시스템] 플레이 기록이 state.json에 저장되었습니다.")

def list_quizzes(quizzes):
    """현재 시스템에 등록되어 있는 모든 퀴즈 목록 출력"""
    if not quizzes:
        print("\n[경고] 등록된 퀴즈가 없습니다.")
        return

    print(f"\n--- 전체 퀴즈 목록 (총 {len(quizzes)}문제) ---")
    for idx, quiz in enumerate(quizzes, 1):
        print(f"{idx:03d}. [{quiz.category}] {quiz.question}")

def add_quiz(quizzes):
    """새로운 퀴즈 객체를 생성하고 master JSON 파일(quizzes_data.json)에 추가 반영"""
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
    quizzes.append(new_quiz)
    
    # quizzes_data.json 에 변경사항 쓰기
    data = [q.to_dict() for q in quizzes]
    with open(QUIZ_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("\n[성공] 새 퀴즈가 성공적으로 추가되었으며 quizzes_data.json에 저장되었습니다!")

def show_history(history):
    """누적된 플레이어 기록 출력"""
    if not history:
        print("\n[알림] 아직 저장된 점수 기록이 없습니다.")
        return

    print("\n--- 점수 및 누적 기록 ---")
    for idx, rec in enumerate(history, 1):
        print(f"{idx}. {rec['name']} - {rec['score']}점 ({rec['correct_count']}/{rec['total_count']} 정답)")

def main():
    """프로그램 시작 및 데이터 초기화"""
    quizzes = load_master_quizzes()
    history = load_state()

    while True:
        show_menu()
        choice = input("원하는 메뉴 번호를 입력하세요 (1-5): ").strip()
        
        if choice == '1':
            play_quiz(quizzes, history)
        elif choice == '2':
            list_quizzes(quizzes)
        elif choice == '3':
            add_quiz(quizzes)
        elif choice == '4':
            show_history(history)
        elif choice == '5':
            print("\n게임을 종료합니다. 이용해 주셔서 감사합니다.")
            break
        else:
            print("\n[오류] 잘못된 입력입니다. 1부터 5 사이의 숫자를 입력해 주세요.")

if __name__ == "__main__":
    main()