from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.services.dataset_service import get_dataset_info
import json
from ..utils.i18n import get_text, TRANSLATIONS

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def dataset_page(request: Request, lang: str = "en"):
    """Render the dataset exploration page"""
    raw_datasets = get_dataset_info(settings.RAW_DATA_DIR)
    processed_datasets = get_dataset_info(settings.PROCESSED_DATA_DIR)
    
    return templates.TemplateResponse(
        "dataset.html",
        {
            "request": request,
            "lang": lang,
            "translations": {k: get_text(k, lang) for k in TRANSLATIONS["en"].keys()},
            "raw_datasets": raw_datasets,
            "processed_datasets": processed_datasets
        }
    )

@router.get("/raw/{dataset_name}")
async def get_raw_dataset(dataset_name: str):
    """Get details of a specific raw dataset"""
    dataset_path = settings.RAW_DATA_DIR / dataset_name
    if not dataset_path.exists():
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    audio_dir = dataset_path / "audio"
    script_dir = dataset_path / "script"
    
    return {
        "name": dataset_name,
        "file_count": sum(1 for _ in dataset_path.rglob("*") if _.is_file()),
        "audio_count": len(list(audio_dir.glob("*.wav"))) if audio_dir.exists() else 0,
        "script_count": len(list(script_dir.glob("*"))) if script_dir.exists() else 0,
        "files": {
            "audio": [f.name for f in audio_dir.glob("*.wav")] if audio_dir.exists() else [],
            "script": [f.name for f in script_dir.glob("*")] if script_dir.exists() else []
        }
    }

@router.get("/processed/{dataset_name}")
async def get_processed_dataset(dataset_name: str):
    """Get details of a specific processed dataset"""
    dataset_path = settings.PROCESSED_DATA_DIR / dataset_name
    if not dataset_path.exists():
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    dataset_json = dataset_path / "dataset.json"
    audio_dir = dataset_path / "audio"
    
    data = None
    if dataset_json.exists():
        with open(dataset_json) as f:
            data = json.load(f)
    
    return {
        "name": dataset_name,
        "file_count": sum(1 for _ in dataset_path.rglob("*") if _.is_file()),
        "audio_count": len(list(audio_dir.glob("*.wav"))) if audio_dir.exists() else 0,
        "has_dataset_json": dataset_json.exists(),
        "dataset_info": data,
        "files": {
            "audio": [f.name for f in audio_dir.glob("*.wav")] if audio_dir.exists() else []
        }
    } 