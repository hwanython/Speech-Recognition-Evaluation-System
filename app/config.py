from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Base directory for data
    # DATA_DIR: Path = Path(r"E:\osstem\Speech-Recognition-Evaluation-System\0data\stt")
    DATA_DIR: Path = Path("/usr/DATA/backup_home_dir/jhhan/02_dev/llm/stt/data/stt")
    
    # Raw data directory
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    
    # Processed data directory
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    
    AUDIO_SUBDIR: str = "audio"  # 오디오 파일이 저장되는 하위 디렉토리 이름
    DEFAULT_AUDIO_EXT: str = ".wav"  # 기본 오디오 파일 확장자
    
    class Config:
        env_file = ".env"

settings = Settings() 