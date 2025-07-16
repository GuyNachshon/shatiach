
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TRANSCRIPTS_DIR = os.environ.get("TRANSCRIPTS_DIR", "/app/data/transcripts")
# Ensure the transcripts directory exists
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

def transcribe_audio(file_path: str, task_id: str, tasks: dict):
    """
    Transcribes an audio file using a pre-trained model and saves the result to a file.
    Updates the task status dictionary with the progress.
    """
    try:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = os.environ.get("TRANSCRIPTION_MODEL_PATH", "ivrit-ai/whisper-large-v3")
        logger.info(f"Loading transcription model: {model_id}")

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)

        processor = AutoProcessor.from_pretrained(model_id)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )

        logger.info(f"Starting transcription for task: {task_id}")
        result = pipe(file_path, generate_kwargs={"language": "hebrew"})
        transcript_text = result["text"]
        
        # Save the transcript to a file
        transcript_file_path = os.path.join(TRANSCRIPTS_DIR, f"{task_id}.txt")
        with open(transcript_file_path, "w", encoding='utf-8') as f:
            f.write(transcript_text)

        tasks[task_id] = {"status": "completed", "result": transcript_text}
        logger.info(f"Transcription task {task_id} completed successfully.")

    except Exception as e:
        logger.error(f"Transcription task {task_id} failed: {e}", exc_info=True)
        tasks[task_id] = {"status": "failed", "result": str(e)}
    finally:
        # Clean up the temporary audio file
        if os.path.exists(file_path):
            os.remove(file_path)
