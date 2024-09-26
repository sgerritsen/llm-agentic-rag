from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from typing import Optional


class OllamaModelService:
    def __init__(
            self,
            settings: Settings,
            llm_model: Optional[str] = 'llama3.1',
            llama_embedding: Optional[str] = 'mxbai-embed-large',
            base_url: Optional[str] = "http://host.docker.internal:11434"
    ):
        self.settings = settings
        self.llm_model = llm_model
        self.llama_embedding = llama_embedding
        self.base_url = base_url

    def llmModel(self):
        self.settings.llm = Ollama(base_url=self.base_url, model=self.llm_model, request_timeout=45.0)
        return self.settings.llm

    def embeddingModel(self):
        self.settings.embed_model = OllamaEmbedding(model_name=self.llama_embedding, base_url=self.base_url)
        return self.settings.embed_model

    def settings(self):
        return self.settings

# Initialize Ollama and embedding models
