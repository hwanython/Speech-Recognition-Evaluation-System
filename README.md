# Speech Recognition Evaluation System

A comprehensive web-based system for evaluating speech recognition model performance and managing speech datasets.

## Features

### Evaluation
- Upload and process evaluation JSON files containing transcription results
- Compare Character Error Rate (CER) metrics between different models
- Visualize performance metrics with interactive charts
- View detailed transcription results in a tabulated format
- Support for multiple model comparisons

### Dataset Management
- Manage and organize speech datasets
- View dataset statistics and information
- Process raw and processed audio files
- Track dataset versions and modifications

## Technical Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: SQLite (for temporary data storage)
- **File Processing**: JSON, Audio file handling
- **Internationalization**: Multi-language support (English/Korean)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd speech-recognition-evaluation
```

2. Create and activate virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the web interface:
```
http://localhost:8000
```

3. Navigate to the evaluation page:
```
http://localhost:8000/evaluation
```

4. Upload your evaluation JSON file with the following structure:
```json
{
  "transcriptions": {
    "model-name": [
      {
        "audio_filepath": "path/to/audio.wav",
        "pred_sentence": "predicted transcription"
      }
    ]
  },
  "CER metric": {
    "model-name": 0.123
  }
}
```

## Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── models/             
│   ├── database.py      # Database models
│   └── evaluation.py    # Evaluation data models
├── routers/
│   ├── evaluation.py    # Evaluation routes
│   ├── dataset.py       # Dataset management routes
│   └── main_routes.py   # Main page routes
├── services/
│   └── evaluation_service.py  # Evaluation processing logic
├── templates/           # HTML templates
└── utils/
    └── i18n.py         # Internationalization support
```

## Features in Detail

### Evaluation System
- **Model Comparison**: Compare multiple speech recognition models side by side
- **Metric Visualization**: Interactive charts showing CER metrics
- **Detailed Results**: View complete transcription results in a searchable table
- **Error Analysis**: Identify and analyze transcription errors

### User Interface
- Clean and intuitive web interface
- Responsive design for various screen sizes
- Interactive data visualization
- Drag-and-drop file upload support

## Language Support

- English (Default)
- Korean (한국어)

Language can be switched using the selector in the navigation bar.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[License Type] - see LICENSE file for details

## 주요 기능

1. **평가 비교 그래프 제작**
   - evaluation.json 파일 드래그 앤 드롭 업로드
   - 모델별 CER 비교 그래프 자동 생성
   - 문장 단위 전사 결과 테이블 뷰

2. **데이터셋 확인**
   - Raw 데이터셋 탐색 (audio-script 페어)
   - Processed 데이터셋 탐색 (chunked audio segments)
   - 데이터셋 상세 정보 및 파일 목록 확인

3. **메인 페이지**
   - 프로젝트 소개 및 사용법 안내
   - 마크다운 기반 문서

## 설치 방법

1. 저장소 클론
```bash
git clone <repository-url>
cd stt-evaluation-viewer
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

1. 개발 서버 실행
```bash
python run.py
```

2. 브라우저에서 접속
- 메인 페이지: http://localhost:8000/
- 평가 페이지: http://localhost:8000/evaluation
- 데이터셋 페이지: http://localhost:8000/dataset

## 데이터 구조

### Raw 데이터셋
```
raw/
├── eval_v1/
│   ├── audio/
│   └── script/
└── v1/
    ├── audio/
    └── script/
```

### Processed 데이터셋
```
processed/
├── dataset_v1/
│   ├── audio/
│   ├── cache_features/
│   ├── logs/
│   ├── dataset.json
│   └── script/
└── eval_v1/
    ├── audio/
    ├── cache_features/
    ├── logs/
    └── script/
```

## evaluation.json 형식

```json
{
  "transcriptions": {
    "model1": [
      {
        "audio_filepath": "path/to/audio.wav",
        "pred_sentence": "예측된 전사 문장"
      }
    ]
  },
  "CER metric": {
    "model1": 0.15
  }
}
```

## 개발 환경

- Python 3.8+
- FastAPI
- Pydantic
- Chart.js (프론트엔드 차트 시각화)

## 테스트

테스트 실행:
```bash
pytest
```

## 라이선스

MIT License

## 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 