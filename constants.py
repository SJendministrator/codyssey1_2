"""
프로젝트에서 사용하는 상수 및 기본 데이터 정의
"""

STATE_FILE = "state.json"

DEFAULT_QUIZZES = [
    {
        "category": "프로그래밍",
        "question": "파이썬에서 리스트의 맨 뒤에 새로운 요소를 추가할 때 사용하는 메서드는?",
        "options": ["add()", "append()", "insert()", "push()"],
        "answer": 2,
        "hint": "a로 시작하는 6글자 단어입니다."
    },
    {
        "category": "프로그래밍",
        "question": "다음 중 파이썬의 불변(Immutable) 시퀀스 자료형은?",
        "options": ["list", "dict", "set", "tuple"],
        "answer": 4,
        "hint": "소괄호()를 사용하여 선언합니다."
    },
    {
        "category": "Git",
        "question": "Git에서 현재 작업 상태와 커밋되지 않은 변경사항을 확인하는 명령어는?",
        "options": ["git log", "git status", "git diff", "git check"],
        "answer": 2,
        "hint": "상태를 뜻하는 영어 단어입니다."
    },
    {
        "category": "프로그래밍",
        "question": "프로세스 실행 중 무한 루프나 강제 종료 명령(Ctrl+C)이 발생시킬 수 있는 예외는?",
        "options": ["ValueError", "KeyError", "KeyboardInterrupt", "TypeError"],
        "answer": 3,
        "hint": "키보드 중단이라는 뜻을 가집니다."
    },
    {
        "category": "컴퓨터공학",
        "question": "JSON 형식에서 데이터를 주고받을 때 기본이 되는 구조는?",
        "options": ["Key-Value 쌍", "Array 단독", "Binary 데이터", "XML 태그"],
        "answer": 1,
        "hint": "파이썬의 dict(딕셔너리)와 유사합니다."
    }
]