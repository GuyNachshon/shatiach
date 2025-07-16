
from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
import uuid

from shatiach.services.transcription_service import transcribe_audio

router = APIRouter()

tasks = {}

@router.post("/transcribe")
async def create_transcription_task(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing", "result": None}
    
    file_path = f"/tmp/{task_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    background_tasks.add_task(transcribe_audio, file_path, task_id, tasks)
    
    return {"task_id": task_id}

@router.get("/transcription/{transcription_id}")
async def get_transcription_status(transcription_id: str):
    task = tasks.get(transcription_id)
    if not task:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    return task
