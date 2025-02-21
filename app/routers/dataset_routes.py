from fastapi import APIRouter, Request, HTTPException, Query, Form
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.services.dataset_service import get_dataset_info
import json
from ..utils.i18n import get_text, TRANSLATIONS
from fastapi.responses import HTMLResponse, RedirectResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional
from datetime import datetime
from pathlib import Path
import logging
from urllib.parse import quote

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

logger = logging.getLogger(__name__)

# 번역 딕셔너리 추가
translations = {
    "dataset_title": "데이터셋",
    "raw_data": "원본 데이터",
    "processed_data": "처리된 데이터",
    "total_files": "전체 파일",
    "audio_files": "오디오 파일",
    "script_files": "스크립트 파일",
    "includes_dataset_json": "dataset.json 포함",
    "view_details": "상세 보기"
}

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
            "processed_datasets": processed_datasets,
            "translations": translations
        }
    )

@router.get("/raw/{dataset_name}", response_class=HTMLResponse)
async def view_raw_dataset(
    request: Request, 
    dataset_name: str,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = None
):
    """Raw 데이터셋 상세 페이지"""
    try:
        dataset_path = settings.RAW_DATA_DIR / dataset_name
        if not dataset_path.exists():
            raise HTTPException(status_code=404, detail="Dataset not found")
            
        audio_dir = dataset_path / "audio"
        script_dir = dataset_path / "script"
        
        # 디렉토리가 없는 경우 빈 데이터셋으로 처리
        if not audio_dir.exists() and not script_dir.exists():
            return templates.TemplateResponse(
                "dataset_details.html",
                {
                    "request": request,
                    "dataset": {
                        "name": dataset_name,
                        "collection": "raw",
                    },
                    "segments": [],
                    "total_segments": 0,
                    "current_page": page,
                    "total_pages": 1,  # 최소 1페이지는 있어야 함
                    "search": search,
                    "translations": translations,
                    "is_empty": True  # 빈 데이터셋 표시
                }
            )
        
        # 오디오 파일과 스크립트 파일 매칭
        audio_files = list(audio_dir.glob("*.wav")) if audio_dir.exists() else []
        all_segments = []
        
        for audio_file in audio_files:
            script_file = script_dir / f"{audio_file.stem}.txt" if script_dir.exists() else None
            sentence = ""
            if script_file and script_file.exists():
                with open(script_file, 'r', encoding='utf-8') as f:
                    sentence = f.read().strip()
            
            # 검색 필터링
            if search and search.lower() not in sentence.lower():
                continue
                    
            all_segments.append({
                "audio_file_path": str(audio_file.relative_to(settings.DATA_DIR)),
                "sentences": sentence
            })
        
        # 페이지네이션 계산
        total_segments = len(all_segments)
        total_pages = (total_segments + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        segments = all_segments[start_idx:end_idx]
            
        return templates.TemplateResponse(
            "dataset_details.html",
            {
                "request": request,
                "dataset": {
                    "name": dataset_name,
                    "collection": "raw",
                },
                "segments": segments,
                "total_segments": total_segments,
                "current_page": page,
                "total_pages": total_pages,
                "search": search,
                "translations": translations
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_page_range(current_page: int, total_pages: int, show_pages: int = 10) -> range:
    """
    현재 페이지를 중심으로 표시할 페이지 범위를 계산합니다.
    
    Args:
        current_page: 현재 페이지
        total_pages: 전체 페이지 수
        show_pages: 표시할 페이지 수 (기본값 10)
    
    Returns:
        표시할 페이지 범위
    """
    half = show_pages // 2
    start_page = max(current_page - half, 1)
    end_page = min(start_page + show_pages - 1, total_pages)
    
    # 끝부분에서 범위 조정
    if end_page - start_page < show_pages - 1:
        start_page = max(end_page - show_pages + 1, 1)
    
    return range(start_page, end_page + 1)

@router.get("/processed/{dataset_name}", response_class=HTMLResponse)
async def view_processed_dataset(
    request: Request, 
    dataset_name: str,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = None
):
    """Processed 데이터셋 상세 페이지"""
    try:
        dataset_path = settings.PROCESSED_DATA_DIR / dataset_name
        if not dataset_path.exists():
            raise HTTPException(status_code=404, detail="Dataset not found")
            
        dataset_json = dataset_path / "dataset.json"
        all_segments = []
        
        if dataset_json.exists():
            with open(dataset_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                segments_data = data.get('data', data) if isinstance(data, dict) else data

                for item in segments_data:
                    if not isinstance(item, dict):
                        continue
                        
                    sentence = item.get('sentence', '')
                    audio_path = item.get('audio_filepath', '')
                    
                    try:
                        if audio_path:
                            # 파일명만 추출
                            filename = Path(audio_path).name
                            # 데이터셋의 audio 폴더 기준으로 경로 생성
                            relative_path = f"{dataset_name}/audio/{filename}"
                            
                            # URL 인코딩 (특수문자 처리)
                            encoded_path = quote(relative_path)
                            
                            if search and search.lower() not in sentence.lower():
                                continue
                                
                            all_segments.append({
                                "audio_file_path": encoded_path,
                                "filename": filename,
                                "sentences": sentence
                            })
                            
                    except Exception as e:
                        logger.error(f"Error processing path {audio_path}: {e}")
                        continue
        
        # 페이지네이션 계산
        total_segments = len(all_segments)
        total_pages = max(1, (total_segments + per_page - 1) // per_page)
        page_range = get_page_range(page, total_pages)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        segments = all_segments[start_idx:end_idx]
        
        return templates.TemplateResponse(
            "dataset_details.html",
            {
                "request": request,
                "dataset": {
                    "name": dataset_name,
                    "collection": "processed",
                },
                "segments": segments,
                "total_segments": total_segments,
                "current_page": page,
                "total_pages": total_pages,
                "page_range": page_range,
                "search": search,
                "translations": translations,
                "is_empty": total_segments == 0
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dataset_id}", response_class=HTMLResponse)
async def get_dataset_details(
    request: Request, 
    dataset_id: str,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    search: Optional[str] = None
):
    try:
        # 데이터베이스에서 dataset_id에 해당하는 데이터셋 정보 조회
        client = MongoClient()
        db = client.get_database()
        dataset = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # 검색 필터 구성
        filter_query = {"dataset_id": ObjectId(dataset_id)}
        if search:
            filter_query["sentences"] = {"$regex": search, "$options": "i"}

        # 전체 세그먼트 수 계산
        total_segments = await db.segments.count_documents(filter_query)
        
        # 페이지네이션 적용
        skip = (page - 1) * per_page
        segments = await db.segments.find(filter_query)\
            .skip(skip)\
            .limit(per_page)\
            .to_list(length=None)

        # 총 페이지 수 계산
        total_pages = (total_segments + per_page - 1) // per_page

        return templates.TemplateResponse(
            "dataset_details.html",
            {
                "request": request,
                "dataset": dataset,
                "segments": segments,
                "current_page": page,
                "total_pages": total_pages,
                "search": search,
                "total_segments": total_segments,
                "translations": translations
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/create", response_class=HTMLResponse)
# async def create_dataset(
#     request: Request,
#     name: str = Form(...),
#     collection: str = Form(...),  # collection 필드 추가
# ):
#     try:
#         dataset = {
#             "name": name,
#             "collection": collection,
#             "created_at": datetime.utcnow()
#         }
#         result = await db.datasets.insert_one(dataset)
#         return RedirectResponse(url="/datasets", status_code=303)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) 