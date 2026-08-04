class Quiz:
    """단일 퀴즈 문제의 데이터와 관련 동작을 관리하는 클래스"""
    def __init__(self, category, question, options, answer, hint=""):
        self.category = category    # 문제 카테고리/분야 (문자열)
        self.question = question    # 질문 내용 (문자열)
        self.options = options      # 보기 목록 (리스트)
        self.answer = answer        # 정답 번호 (1부터 시작하는 정수)
        self.hint = hint            # 힌트 내용 (문자열, 기본값 빈값)

    def is_correct(self, user_choice):
        """사용자가 입력한 답과 정답이 일치하는지 검증"""
        return user_choice == self.answer

    def display(self, number):
        """풀이 화면용: 문제 번호, 카테고리, 질문, 보기 출력"""
        print(f"\n[Q{number}] [{self.category}] {self.question}")
        for idx, option in enumerate(self.options, 1):
            print(f"  {idx}. {option}")

    def to_dict(self):
        """Quiz 객체를 JSON 저장용 딕셔너리로 변환"""
        return {
            "category": self.category,
            "question": self.question,
            "options": self.options,
            "answer": self.answer,
            "hint": self.hint
        }

    @classmethod
    def from_dict(cls, data):
        """딕셔너리 데이터를 받아 Quiz 객체로 복원"""
        return cls(
            category=data.get("category", "일반"),
            question=data.get("question", ""),
            options=data.get("options", []),
            answer=data.get("answer", 1),
            hint=data.get("hint", "")
        )