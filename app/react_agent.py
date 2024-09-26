import os

from llama_index.core import Settings, SimpleDirectoryReader
from support.ollama_model_service import OllamaModelService

from support.simple_rag_query_engine import SimpleRagQueryEngine


from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core.memory.chat_memory_buffer import ChatMemoryBuffer

# Initialize Ollama and embedding models
ollama_model_service = OllamaModelService(settings=Settings)
llm_model = ollama_model_service.llmModel()
ollama_model_service.embeddingModel()

query_engine_tool = []

# Load documents
documents = (SimpleDirectoryReader(input_files=[('/opt/project/LLM-RAG/app/data/%s' % os.getenv('DOCUMENT_NAME'))], recursive=True)
             .load_data(show_progress=True))

query_engine = SimpleRagQueryEngine(documents=documents, index_name=os.getenv('TOOL_NAME')).buildQueryEngine()

query_engine_tool += [QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name=os.getenv('TOOL_NAME'),
        description="This is a RAG AGENT with a broad range of information about ...",
    ),
)]

agent = ReActAgent(llm=llm_model, tools=query_engine_tool, verbose=True,
                   memory=ChatMemoryBuffer.from_defaults(llm=llm_model, token_limit=10000), max_iterations=50)

user_query = '?'

print(user_query)

response = agent.chat(message=user_query)
print(response)
print('-------------------------------------------------------')