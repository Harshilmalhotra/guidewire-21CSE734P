from fastapi import APIRouter
from models.schemas import FNOLRequest, FNOLResponse
from services.ingestion import IngestionPipeline

router = APIRouter()
pipeline = IngestionPipeline()

@router.post("/fnol", response_model=FNOLResponse)
async def submit_fnol(request: FNOLRequest):
    response = pipeline.process_claim(request)
    return response
