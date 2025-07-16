
import chromadb
import ollama
import os

# Define a custom embedding function for ChromaDB that uses Ollama
class OllamaEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, model_name="nomic-embed-text", ollama_host="ollama"):
        # The host for the Ollama client is determined by an environment variable
        # for flexibility in different deployment scenarios (e.g., local vs. Docker).
        self._ollama_client = ollama.Client(host=f"http://{ollama_host}:11434")
        self._model_name = model_name

    def __call__(self, input_texts: chromadb.Documents) -> chromadb.Embeddings:
        """
        Generates embeddings for a list of documents.
        """
        embeddings = []
        for text in input_texts:
            try:
                response = self._ollama_client.embeddings(model=self._model_name, prompt=text)
                embeddings.append(response["embedding"])
            except Exception as e:
                print(f"Error generating embedding for text: {text}. Error: {e}")
                # Handle error appropriately, e.g., append a zero vector or skip.
                # For simplicity, we'll append a zero vector of a plausible dimension.
                # Note: The dimension should match the model's output dimension.
                # Nomic's is 768.
                embeddings.append([0] * 768)
        return embeddings

class VectorDBService:
    def __init__(self, host="chromadb", port=8000):
        """
        Initializes the VectorDBService, setting up the ChromaDB client and collection
        with a custom embedding function that uses Ollama.
        """
        self.client = chromadb.HttpClient(host=host, port=port)
        
        # Determine the Ollama host from an environment variable, defaulting to "ollama".
        # This allows for connecting to a different Ollama instance if needed.
        ollama_host = os.environ.get("OLLAMA_HOST", "ollama")
        ollama_ef = OllamaEmbeddingFunction(ollama_host=ollama_host)
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=ollama_ef
        )

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """
        Adds documents to the collection. The embedding is handled automatically.
        """
        if not (len(documents) == len(metadatas) == len(ids)):
            raise ValueError("The number of documents, metadatas, and ids must be the same.")
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_texts: list[str], n_results: int = 5) -> dict:
        """
        Queries the collection for similar documents. The query text is embedded automatically.
        """
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
