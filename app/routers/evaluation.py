from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Depends
from fastapi.templating import Jinja2Templates
import json
from sqlalchemy.orm import Session
from ..models.database import SessionLocal, Transcription
from typing import Dict, List
from fastapi.responses import JSONResponse
from ..utils.i18n import get_text, TRANSLATIONS

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
async def evaluation_page(request: Request, lang: str = "en"):
    """Render the evaluation comparison page"""
    return templates.TemplateResponse(
        "evaluation.html",
        {
            "request": request,
            "lang": lang,
            "translations": {k: get_text(k, lang) for k in TRANSLATIONS["en"].keys()}
        }
    )

@router.post("/upload")
async def upload_evaluation(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Handle evaluation.json file upload and processing"""
    try:
        # Read and parse JSON file
        contents = await file.read()
        data = json.loads(contents.decode())
        
        # Extract CER metrics
        cer_metrics = data.get("CER metric", {})
        if not cer_metrics:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "CER metric data not found"}
            )

        # Extract transcriptions
        transcriptions = data.get("transcriptions", {})
        if not transcriptions:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Transcriptions data not found"}
            )
        
        try:
            # Clear previous data
            db.query(Transcription).delete()
            
            # Store new data
            for model_name, predictions in transcriptions.items():
                cer = cer_metrics.get(model_name, 0.0)
                for pred in predictions:
                    db_trans = Transcription(
                        model_name=model_name,
                        audio_filepath=pred["audio_filepath"],
                        prediction=pred["pred_sentence"],
                        cer=cer
                    )
                    db.add(db_trans)
            
            db.commit()
        except Exception as db_error:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")

        # Prepare response data
        response_data = {
            "status": "success",
            "metrics": {
                "labels": list(cer_metrics.keys()),
                "values": list(cer_metrics.values())
            }
        }

        return JSONResponse(content=response_data)

    except json.JSONDecodeError as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Invalid JSON format"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@router.get("/results")
async def get_results(db: Session = Depends(get_db)):
    """Get stored transcription results"""
    try:
        # Get unique model names
        models = db.query(Transcription.model_name).distinct().all()
        models = [m[0] for m in models]
        
        if not models:
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "No data found"
                }
            )
        
        # Get all transcriptions
        transcriptions = db.query(Transcription).all()
        
        # Group by audio_filepath
        results = {}
        for trans in transcriptions:
            if trans.audio_filepath not in results:
                results[trans.audio_filepath] = {}
            results[trans.audio_filepath][trans.model_name] = trans.prediction
        
        return JSONResponse(
            content={
                "status": "success",
                "models": models,
                "results": results
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        ) 