from fastapi import FastAPI
from shatiach.api.routers import transcription, query, chat, files

app = FastAPI()

app.include_router(transcription.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(files.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}
