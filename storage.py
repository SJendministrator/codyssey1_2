import json
import os
from quiz import Quiz
from constants import STATE_FILE, DEFAULT_QUIZZES

class StorageManager:
    def __init__(self, filepath=STATE_FILE):
        self.filepath = filepath

    def load_state(self):
        if not os.path.exists(self.filepath):
            return self.reset_to_default()

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                best_score = float(data.get("best_score", 0.0))
                history = data.get("history", [])
                
                if not quizzes:
                    return self.reset_to_default()
                return quizzes, best_score, history
        except Exception:
            return self.reset_to_default()

    def reset_to_default(self):
        quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        best_score = 0.0
        history = []
        self.save_state(quizzes, best_score, history)
        return quizzes, best_score, history

    def save_state(self, quizzes, best_score, history):
        data = {
            "quizzes": [q.to_dict() for q in quizzes],
            "best_score": best_score,
            "history": history
        }
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[오류] 저장 실패: {e}")