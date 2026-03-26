# CaMP-Eval: Software-Web Benchmark Evaluation

CaMP (Collaborative Agent Multi-Phase) 프레임워크의 Software-Web 벤치마크 평가 도구입니다.

## Structure

```
CaMP-Eval/
├── evaluate_CaMP.py              # 평가 스크립트
├── benchmark/Software/web/
│   ├── data/                     # 20개 웹앱 테스트 데이터
│   ├── specification/            # 웹앱 스펙 문서
│   └── testcode/                 # Selenium 테스트 코드
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone <repo-url>
cd CaMP-Eval
pip install -r requirements.txt
```

### Prerequisites

- Python 3.8+
- Google Chrome / Chromium
- ChromeDriver (or use `webdriver-manager`)

## Usage

```bash
python evaluate_CaMP.py
```

실행 후 메뉴에서 `[1] Web Applications`를 선택하고, `results/` 디렉토리 내의 평가 대상 폴더를 지정합니다.

### Results Directory Structure

평가 대상 결과물은 다음 구조를 따라야 합니다:

```
results/Software-web-<name>/
└── <timestamp>/
    └── <TaskName>/
        └── <scenario>/
            └── app.py          # 생성된 Flask 웹앱
```

### Supported Scenarios

- `vanilla` - 기본 시나리오
- `agent_chaos` - 에이전트 카오스
- `stress_chaos` - 스트레스 카오스
- `io_chaos` - IO 카오스
- `complex_chaos` - 복합 카오스
- `compound_chaos` - 합성 카오스
- `compound` - 컴파운드

## Benchmark Details

20개의 Flask 웹 애플리케이션 태스크:

BookstoreOnline, CarRental, ContentPublishingHub, EventPlanning, FoodDelivery, GymMembership, JobBoard, MovieTicketing, MusicStreaming, NewsPortal, OnlineAuction, OnlineCourse, OnlineLibrary, PetAdoptionCenter, RealEstate, RestaurantReservation, SmartHomeManager, TravelPlanner, VirtualMuseum, WeatherForecast
