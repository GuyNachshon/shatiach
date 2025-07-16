
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agno.client import AgnoClient
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

TRANSCRIPTS_DIR = os.environ.get("TRANSCRIPTS_DIR", "/app/data/transcripts")
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen3:32b")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "ollama")

class ChatRequest(BaseModel):
    transcript_id: str
    message: str
    history: list[dict] = [] # Expects a list of {"role": "user/assistant", "content": "..."}

@router.post("/chat")
async def chat_with_transcript(request: ChatRequest):
    """
    Handles a chat request related to a specific transcript.
    It retrieves the transcript, constructs a prompt with conversation history,
    and generates a response using the specified LLM.
    """
    transcript_file_path = os.path.join(TRANSCRIPTS_DIR, f"{request.transcript_id}.txt")
    
    if not os.path.exists(transcript_file_path):
        logger.error(f"Transcript file not found: {transcript_file_path}")
        raise HTTPException(status_code=404, detail="Transcript not found.")

    try:
        with open(transcript_file_path, "r", encoding='utf-8') as f:
            transcript = f.read()
    except Exception as e:
        logger.error(f"Failed to read transcript file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to read transcript.")

    try:
        agno = AgnoClient(host=OLLAMA_HOST, port=11434)

        # Construct the conversation messages for the LLM
        messages = [
            {"role": "system", "content": f"You are a helpful AI assistant. The user is asking questions about the following document:\n\n---\n{transcript}\n---"}
        ]
        messages.extend(request.history)
        messages.append({"role": "user", "content": request.message})

        logger.info(f"Generating chat response for transcript {request.transcript_id} with model {LLM_MODEL}")
        response = agno.chat(
            model=LLM_MODEL,
            messages=messages,
            stream=False
        )

        return {"response": response['message']['content']}

    except Exception as e:
        logger.error(f"Error during chat generation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate chat response.")
