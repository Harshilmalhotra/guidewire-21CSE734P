from fastapi import APIRouter
from models.schemas import FNOLRequest, FNOLResponse
from services.orchestrator import AgenticOrchestrator

router = APIRouter()
orchestrator = AgenticOrchestrator()

@router.post("/fnol", response_model=FNOLResponse)
async def submit_fnol(request: FNOLRequest):
    response = await orchestrator.process(request)
    return response
