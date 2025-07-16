
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from shatiach.services.vector_db_service import VectorDBService
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
vector_db = VectorDBService()
DATA_DIR = os.environ.get("DATA_DIR", "/app/data")

@router.get("/files/search")
async def search_files(query: str):
    """
    Performs a semantic search for files based on the query.
    Returns a list of matching documents and their metadata.
    """
    try:
        logger.info(f"Searching for files with query: '{query}'")
        results = vector_db.query(query_texts=[query], n_results=10)
        return results
    except Exception as e:
        logger.error(f"File search failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="File search failed.")

@router.get("/files/{file_id}/download")
async def download_file(file_id: str):
    """
    Allows downloading a specific file by its ID (filename).
    """
    file_path = os.path.join(DATA_DIR, file_id)
    
    if not os.path.exists(file_path):
        logger.error(f"File not found for download: {file_path}")
        raise HTTPException(status_code=404, detail="File not found.")
    
    logger.info(f"Serving file for download: {file_path}")
    return FileResponse(file_path, media_type='application/octet-stream', filename=file_id)
