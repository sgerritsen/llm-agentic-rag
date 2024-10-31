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



my_list = [
    {"TC001": "Where are errors and success logs stored when jobs are executed?"},
    {"TC002": "What is the backup requirement for business data in RSM custom software?"},
    {"TC003": "What tools are used for backing up custom software code?"},
    {"TC004": "How does the new employee get their druppel (coffee and printing tag) and room key?"},
    {"TC005": "Who should be notified to add the new employee to Teams and meetings?"},
    {"TC006": "What happens with the ERNA ID when an employee leaves EUR?"},
    {"TC007": "Where should the employee's laptop and other devices be returned when leaving?"},
    {"TC008": "What kinds of incidents are considered security violations at RSM?"},
    {"TC009": "What happens if a security incident involves a SAAS supplier?"},
    {"TC010": "What is a SYS-account used for in the envelope procedure?"},
    {"TC011": "Who can modify user categories and roles in SAAS systems?"},
    {"TC015": "How often are job descriptions reviewed"},
    {"TC016": "Where can job descriptions and vacancy texts be accessed?"},
    {"TC017": "What are the key positions within the RDIS department?"},
    {"TC018": "How do Privacy Officers and Information Security Officers manage back-ups?"},
    {"TC019": "What are the key resources identified, and how are they protected?"},
    {"TC020": "What certification is required for the BI Consultant role?"},
    {"TC021": "What level of education is preferred for the BI Consultant?"},
    {"TC022": "What is the BI Consultant’s main responsibility within the organization?"},
    {"TC023": "What is the principle of segregation of duties (SoD)?"},
    {"TC024": "Why is segregation of duties important in RSM?"},
    {"TC025": "What key responsibilities does RDIS have regarding SoD?"},
    {"TC026": "How does RDIS ensure that sensitive activities are performed by at least two individuals?"},
    {"TC027": "What steps are involved in implementing segregation of duties controls?"},
    {"TC028": "What should an end-user do if they notice suspicious activity or a potential breach of SoD controls?"},
    {"TC029": "What type of security incidents might violate confidentiality or integrity in RSM?"},
    {"TC030": "What is the role of the Response Team in handling security incidents?"},
    {"TC031": "How does RDIS handle incidents involving RSM-controlled SaaS?"},
    {"TC032": "What steps are taken when a custom software security incident occurs in RSM?"},
    {"TC033": "What mitigating actions are taken for security incidents across different system types (SaaS vs. Custom software)?"},
]

# Open a file in write mode
with open("data/file.txt", "w") as file:
    # Loop through the list
    for item in my_list:
        # Write each key-value pair to the file
        for key, value in item.items():
            response = agent.chat(message=f"Answer the following question using the RSM quality manual.\nQuestion: {value}")
            file.write(f"{response}\n-------------------------------------------------------\n")

exit()

print(user_query)

response = agent.chat(message=user_query)
print(response)
print('-------------------------------------------------------')