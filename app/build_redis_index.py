import os
from llama_index.core import Settings, SimpleDirectoryReader
from support.ollama_model_service import OllamaModelService
from support.redis_service import RedisService
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_inference import AzureAIEmbeddingsModel

from dotenv import load_dotenv
load_dotenv(os.getenv('ENV_PATH'))

# Initialize Ollama and embedding models
# ollama_model_service = OllamaModelService(settings=Settings)
# ollama_model_service.llmModel()
# ollama_model_service.embeddingModel()

Settings.llm = AzureOpenAI(
    engine="gpt-4o",
    model="gpt-4o",
    azure_endpoint=os.getenv('AZURE_ENDPOINT'),
    api_key=os.getenv('AZURE_API_KEY'),
    api_version=os.getenv('AZURE_API_VERSION'),
)

Settings.embed_model = AzureAIEmbeddingsModel(
    model_name='txt-embed',
    endpoint=os.getenv('AZURE_ENDPOINT_EMBEDDING'),
    credential=os.getenv('AZURE_API_KEY'),
    api_version=os.getenv('AZURE_API_VERSION_EMBEDDING'),
)

# def get_meta(file_path):
#     return {"foo": "bar"}

# Load documents
# documents = SimpleDirectoryReader(input_files=[('/opt/project/LLM-RAG/app/data/%s' % os.getenv('DOCUMENT_NAME'))], file_metadata=get_meta, recursive=True).load_data(show_progress=True)
documents = SimpleDirectoryReader('data/QM', required_exts=[".pdf", ".docx"], recursive=False).load_data(show_progress=True)

redis_store = RedisService(index_name=os.getenv('TOOL_NAME'), dimensions=1024, overwrite=True).createVectorStore()

# Create storage context and index
storage_context = StorageContext.from_defaults(vector_store=redis_store)

vector_store = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context)