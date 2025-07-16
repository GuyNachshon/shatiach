
from fastapi import APIRouter
from pydantic import BaseModel
from shatiach.services.agent_service import AgentService

router = APIRouter()
agent_service = AgentService()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def query(request: QueryRequest):
    return agent_service.query(request.query)
