# quiz.py

class Quiz:
    """단일 퀴즈 문제의 데이터와 관련 동작을 관리하는 클래스"""
    def __init__(self, question, options, answer, category):
        self.question = question    # 질문 내용 (문자열)
        self.options = options      # 보기 목록 (리스트)
        self.answer = answer        # 정답 번호 (1부터 시작하는 정수)
        self.category = category    # 문제 카테고리/분야 (문자열)

    def is_correct(self, user_choice):
        """사용자가 입력한 답과 정답이 일치하는지 검증"""
        return user_choice == self.answer

    def display(self, number):
        """풀이 화면용: 문제 번호, 카테고리, 질문, 보기 출력"""
        print(f"\n[Q{number}] [{self.category}] {self.question}")
        for idx, option in enumerate(self.options, 1):
            print(f"  {idx}. {option}")


# 시스템 기본 제공 과학·공학 퀴즈 데이터 세트
DEFAULT_QUIZZES = [
    Quiz(
        question="파이썬(Python)에서 리스트의 맨 뒤에 새로운 요소를 추가할 때 사용하는 메서드는?",
        options=["add()", "append()", "insert()", "push()"],
        answer=2,
        category="프로그래밍"
    ),
    Quiz(
        question="비행기가 공중으로 떠오르는 힘인 '양력'을 설명하는 대표적인 유체역학 원리는?",
        options=["베르누이 정리", "파스칼의 원리", "아르키메데스의 원리", "뉴턴의 쿨롱 법칙"],
        answer=1,
        category="항공공학"
    ),
    Quiz(
        question="내연기관 자동차의 4행정 엔진 순서로 올바른 것은?",
        options=[
            "흡입 -> 폭발 -> 압축 -> 배기",
            "흡입 -> 압축 -> 폭발 -> 배기",
            "압축 -> 흡입 -> 폭발 -> 배기",
            "폭발 -> 흡입 -> 압축 -> 배기"
        ],
        answer=2,
        category="자동차공학"
    ),
    Quiz(
        question="열역학 제2법칙에 따르면, 고립계 전체의 '이것'은 항상 증가하는 방향으로 변화합니다. '이것'은?",
        options=["엔탈피", "엔트로피", "탄성력", "점성계수"],
        answer=2,
        category="기계공학"
    ),
    Quiz(
        question="생명체 내에서 유전 정보를 담고 있는 물질인 DNA의 기본 구성 단위는?",
        options=["아미노산", "뉴클레오타이드", "지방산", "글루코스"],
        answer=2,
        category="생명공학"
    )
]