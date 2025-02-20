import json
from typing import Dict, List
from app.models.schemas import EvaluationResult, TranscriptionResult

async def process_evaluation_json(contents: bytes) -> EvaluationResult:
    """Process uploaded evaluation.json file"""
    try:
        data = json.loads(contents)
        
        # Convert raw data to Pydantic models for validation
        transcriptions = {
            model: [TranscriptionResult(**t) for t in results]
            for model, results in data["transcriptions"].items()
        }
        
        return EvaluationResult(
            transcriptions=transcriptions,
            cer_metric=data["CER metric"]
        )
    except Exception as e:
        raise ValueError(f"Invalid evaluation.json format: {str(e)}")

def prepare_graph_data(eval_result: EvaluationResult) -> Dict:
    """Prepare data for graph visualization"""
    return {
        "models": list(eval_result.cer_metric.keys()),
        "cer_values": list(eval_result.cer_metric.values())
    } 