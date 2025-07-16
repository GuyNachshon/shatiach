
import os
import logging
from agno.client import AgnoClient
from shatiach.services.vector_db_service import VectorDBService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        """
        Initializes the AgentService, setting up the AgnoClient for LLM interaction
        and the VectorDBService for document retrieval.
        """
        ollama_host = os.environ.get("OLLAMA_HOST", "ollama")
        self.agno = AgnoClient(host=ollama_host, port=11434)
        self.vector_db = VectorDBService()
        self.llm_model = os.environ.get("LLM_MODEL", "qwen3:32b") # Default to qwen3:32b

    def query(self, user_query: str) -> dict:
        """
        Performs a RAG query: retrieves documents, constructs a prompt, and generates a response.
        """
        try:
            # 1. Retrieve relevant documents from ChromaDB
            logger.info(f"Retrieving documents for query: '{user_query}'")
            retrieved_docs = self.vector_db.query(query_texts=[user_query], n_results=3)
            
            if not retrieved_docs or not retrieved_docs.get('documents') or not retrieved_docs['documents'][0]:
                logger.warning("No relevant documents found for the query.")
                return {"response": "I could not find any relevant documents to answer your question.", "sources": []}

            # 2. Construct a prompt with the retrieved context
            context = "\n\n".join(
                [f"Source: {meta['source']}\nContent: {doc}" 
                 for doc, meta in zip(retrieved_docs['documents'][0], retrieved_docs['metadatas'][0])]
            )
            
            prompt = f"""You are a helpful AI assistant. Based on the following context, please answer the user's query.
Cite the sources you used in your answer.

Context:
{context}

User Query: {user_query}

Answer:"""

            # 3. Use a local LLM to generate a response
            logger.info(f"Generating response with model: {self.llm_model}")
            response = self.agno.generate(
                model=self.llm_model,
                prompt=prompt,
                stream=False # Keep it simple for now
            )

            return {
                "response": response.get("response", "").strip(),
                "sources": [meta['source'] for meta in retrieved_docs['metadatas'][0]]
            }
        
        except Exception as e:
            logger.error(f"An error occurred during the query process: {e}", exc_info=True)
            return {"response": "An internal error occurred. Please try again later.", "sources": []}

