from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Base directory for data
    DATA_DIR: Path = Path("/usr/DATA/backup_home_dir/jhhan/02_dev/llm/stt/data/stt")
    
    # Raw data directory
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    
    # Processed data directory
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    
    class Config:
        env_file = ".env"

settings = Settings() 