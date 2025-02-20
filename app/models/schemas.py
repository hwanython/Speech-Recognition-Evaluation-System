from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path

class TranscriptionResult(BaseModel):
    audio_filepath: str
    pred_sentence: str

class EvaluationResult(BaseModel):
    transcriptions: Dict[str, List[TranscriptionResult]]
    cer_metric: Dict[str, float]

class DatasetEntry(BaseModel):
    audio_filepath: str
    sentence: str

class Dataset(BaseModel):
    title: str
    dataset_type: str
    data: List[DatasetEntry]

class DatasetInfo(BaseModel):
    name: str
    file_count: int
    audio_count: Optional[int] = None
    script_count: Optional[int] = None
    has_dataset_json: bool = False
    path: Path 