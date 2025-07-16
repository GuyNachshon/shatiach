
import os
import logging
import docx
import PyPDF2
from shatiach.services.vector_db_service import VectorDBService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = "".join(page.extract_text() for page in reader.pages)
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def ingest_data():
    vector_db = VectorDBService()
    data_dir = os.environ.get("DATA_DIR", "/app/data")
    
    logger.info(f"Starting data ingestion from directory: {data_dir}")

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        content = None
        try:
            if filename.endswith(".txt"):
                with open(file_path, "r", encoding='utf-8') as f:
                    content = f.read()
            elif filename.endswith(".pdf"):
                content = extract_text_from_pdf(file_path)
            elif filename.endswith(".docx"):
                content = extract_text_from_docx(file_path)
            else:
                logger.warning(f"Skipping unsupported file type: {filename}")
                continue

            if content:
                vector_db.add_documents(
                    documents=[content],
                    metadatas=[{"source": filename}],
                    ids=[filename]
                )
                logger.info(f"Successfully ingested and vectorized {filename}")

        except Exception as e:
            logger.error(f"Failed to ingest {filename}. Error: {e}", exc_info=True)

if __name__ == "__main__":
    ingest_data()
