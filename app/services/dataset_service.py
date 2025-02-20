from pathlib import Path
import json
from typing import List, Dict
from app.models.schemas import DatasetInfo, Dataset
from app.config import settings

def get_dataset_info(base_path: Path) -> List[DatasetInfo]:
    """Get information about datasets in the given directory"""
    datasets = []
    
    for path in base_path.iterdir():
        if path.is_dir():
            audio_dir = path / "audio"
            script_dir = path / "script"
            dataset_json = path / "dataset.json"
            
            info = DatasetInfo(
                name=path.name,
                file_count=sum(1 for _ in path.rglob("*") if _.is_file()),
                audio_count=len(list(audio_dir.glob("*.wav"))) if audio_dir.exists() else None,
                script_count=len(list(script_dir.glob("*"))) if script_dir.exists() else None,
                has_dataset_json=dataset_json.exists(),
                path=path
            )
            datasets.append(info)
            
    return datasets

def load_dataset_json(path: Path) -> Dataset:
    """Load and parse dataset.json file"""
    with open(path / "dataset.json") as f:
        data = json.load(f)
    return Dataset(**data) 