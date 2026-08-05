# Python Console Quiz Game

> **콘솔 기반의 대화형 퀴즈 게임 프로젝트**  
> Python **표준 라이브러리만** 사용하여 객체지향 설계(OOP), 예외 처리, 파일 I/O 및 Git Workflow를 적용해 제작한 프로젝트입니다.

---

# 프로젝트 개요 (Overview)

본 프로젝트는 **컴퓨터공학 및 다양한 전공 분야의 핵심 개념을 학습할 수 있는 콘솔 기반 퀴즈 프로그램**입니다.

사용자는 원하는 문제 수를 선택하여 무작위로 퀴즈를 풀 수 있으며, 힌트 기능, 최고 점수 기록, 플레이 히스토리 저장 등 다양한 기능을 제공합니다.

---

# 퀴즈 주제 및 선정 이유

### 주제

- 컴퓨터공학
- 프로그래밍 (Python / C / C++ / Java / JavaScript)
- 운영체제(OS)
- 네트워크
- 데이터베이스(DB)
- 소프트웨어 공학
- 기계공학
- 전자공학
- 생명공학

### 선정 이유

1. 단순한 상식 퀴즈가 아닌 **전공 학습과 면접 대비**에 도움이 되는 문제를 제작하고자 했습니다.

2. **총 103개의 다양한 문제**를 수록하여 반복 플레이 시에도 새로운 문제를 경험할 수 있도록 구성했습니다.

---

# 실행 방법 (How to Run)

## 필수 조건

- Python 3.10 이상
- 별도의 패키지 설치 필요 없음 (표준 라이브러리만 사용)

## 실행

프로젝트 루트 디렉터리에서 아래 명령어를 실행합니다.

```bash
python3 main.py
```

---

# 주요 기능 (Features)

## 메인 화면

![메인 화면](src/mainscreen.png)

---

## 퀴즈 기능

| 기능 | 설명 |
|------|------|
| 랜덤 출제 | `random.sample()`을 이용한 무작위 문제 출제 |
| 문제 수 선택 | 전체 103문항 중 원하는 개수 선택 |
| 힌트 기능 | `h` 입력 시 힌트 제공 (점수 차감) |
| 점수 계산 | 정답률 및 점수 계산 |
| 플레이 기록 | 플레이 결과 및 최고 점수 저장 |

---

## 문제 관리

| 퀴즈 목록 | 퀴즈 추가 |
|-----------|-----------|
| ![](src/quizlist.png) | ![](src/addquiz.png) |

| 추가 후 목록 | 종료 화면 |
|--------------|-----------|
| ![](src/quizlist2.png) | ![](src/exitgame.png) |

### 지원 기능

- 전체 퀴즈 목록 조회
- 퀴즈 직접 추가
- 기존 퀴즈 삭제
- 최고 점수 조회
- 플레이 히스토리 조회

---

# 예외 처리 및 방어 로직

- 입력값 검증 (`strip()`을 이용한 공백 제거)
- 빈 입력 및 잘못된 메뉴 번호 재입력
- `ValueError` 발생 시 안전하게 복구
- `KeyboardInterrupt (Ctrl + C)` 및 `EOFError` 발생 시 저장 후 정상 종료
- `state.json`이 없거나 손상된 경우 기본 데이터로 자동 복구

![예외 처리](exprossece.png)

---

# 프로젝트 구조

```text
.
├── constants.py   # 기본 퀴즈 데이터 및 상수
├── quiz.py        # Quiz 모델 클래스
├── storage.py     # JSON 저장 및 로드
├── game.py        # 게임 진행 및 점수 계산
├── main.py        # 메인 메뉴 및 프로그램 실행
└── state.json     # 퀴즈, 최고 점수, 플레이 기록 저장
```

---

# 데이터 파일 (state.json)

프로그램은 `state.json` 파일을 이용하여 데이터를 영구적으로 저장합니다.

### 저장 항목

- 퀴즈 목록
- 최고 점수
- 플레이 히스토리

### JSON 예시

```json
{
  "quizzes": [
    {
      "category": "프로그래밍",
      "question": "파이썬에서 리스트의 맨 뒤에 요소를 추가하는 메서드는?",
      "options": [
        "append()",
        "push()",
        "add()",
        "insert()"
      ],
      "answer": 1,
      "hint": "리스트 끝에 항목을 덧붙이는 메서드입니다."
    }
  ],
  "best_score": 100.0,
  "history": [
    {
      "date": "2026-08-04 14:30:00",
      "score": 100.0,
      "total_questions": 5
    }
  ]
}
```

---

# Git Workflow

본 프로젝트는 기능별 브랜치를 활용하여 개발을 진행하였으며, Git을 이용한 협업 및 버전 관리를 실습했습니다.

- Feature Branch 사용
- Merge를 통한 기능 통합
- `git clone`
- `git pull`
- 원격 저장소 동기화

| Clone / Pull 실습 |
|-------------------|
| ![](src/clone_test1.png) |
| ![](src/clone_test2.png) |
| ![](src/clone_test3.png) |
| ![](src/clone_test4.png) |
| ![](src/clone_test5.png) |

---

# 개발 환경

- Python 3.10+
- Standard Library Only
- JSON
- Git
- GitHub
- VS Code