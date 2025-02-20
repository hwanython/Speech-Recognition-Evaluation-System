# 언어 리소스 정의
TRANSLATIONS = {
    "ko": {
        # 공통
        "home": "홈",
        "evaluation": "평가",
        "dataset": "데이터셋",
        
        # Home 페이지
        "welcome_title": "음성인식 평가 및 데이터셋 관리 시스템",
        "welcome_description": "음성인식 모델의 성능을 평가하고 데이터셋을 관리하는 시스템입니다.",
        
        # 평가 페이지
        "title": "음성인식 평가 및 데이터셋 관리 시스템",
        "upload_title": "평가 파일 업로드",
        "upload_description": "평가 JSON 파일을 여기에 드래그하거나 클릭하여 업로드하세요",
        "metrics_title": "CER 메트릭 비교",
        "results_title": "전사 결과 비교",
        "error_processing": "파일 처리 중 오류가 발생했습니다.",
        "no_data": "데이터가 없습니다.",
        
        # 데이터셋 페이지
        "dataset_title": "데이터셋 관리",
        "dataset_upload": "데이터셋 업로드",
        "dataset_list": "데이터셋 목록",
        "dataset_stats": "데이터셋 통계",
        "no_datasets": "사용 가능한 데이터셋이 없습니다."
    },
    "en": {
        # Common
        "home": "Home",
        "evaluation": "Evaluation",
        "dataset": "Dataset",
        
        # Home page
        "welcome_title": "Speech Recognition Evaluation and Dataset Management System",
        "welcome_description": "A system for evaluating speech recognition models and managing datasets.",
        
        # Evaluation page
        "title": "Speech Recognition Evaluation and Dataset Management System",
        "upload_title": "Upload Evaluation File",
        "upload_description": "Drag and drop evaluation JSON file here or click to upload",
        "metrics_title": "CER Metrics Comparison",
        "results_title": "Transcription Results Comparison",
        "error_processing": "An error occurred while processing the file.",
        "no_data": "No data available.",
        
        # Dataset page
        "dataset_title": "Dataset Management",
        "dataset_upload": "Upload Dataset",
        "dataset_list": "Dataset List",
        "dataset_stats": "Dataset Statistics",
        "no_datasets": "No datasets available."
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Get translated text for given key and language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key) 