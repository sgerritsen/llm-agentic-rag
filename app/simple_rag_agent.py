import os
from llama_index.core import Settings, SimpleDirectoryReader
from support.ollama_model_service import OllamaModelService

from support.redis_service import RedisService
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

# Initialize Ollama and embedding models
ollama_model_service = OllamaModelService(settings=Settings)
llm_model = ollama_model_service.llmModel()
ollama_model_service.embeddingModel()

# Load documents
documents = SimpleDirectoryReader(input_dir='data', recursive=True).load_data(show_progress=True)

redis_store = RedisService(index_name=os.getenv('TOOL_NAME'), dimensions=1024, overwrite=False).createVectorStore()

# Create storage context and index
storage_context = StorageContext.from_defaults(vector_store=redis_store)
vector_store = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context)

retriever = VectorIndexRetriever(index=vector_store, similarity_top_k=10)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7,
                                                 filter_empty=True,
                                                 filter_duplicates=True,
                                                 filter_similar=False, ), ]
)
user_query = "?"
response = query_engine.query(user_query)
print(response)
