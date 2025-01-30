import os, sys
from llama_index.core import Settings
from llama_index.core.response.pprint_utils import pprint_response
from support.ollama_model_service import OllamaModelService

from support.redis_service import RedisService
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_inference import AzureAIEmbeddingsModel

def main(input_text):
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

    # Get the loaded index from the Redis server
    vector_store = RedisService(index_name=os.getenv('TOOL_NAME'), dimensions=1024).load_index()

    vector_store_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    retriever = VectorIndexRetriever(index=vector_store_index, similarity_top_k=10)

    api_key = os.getenv('COHERE_API_KEY')
    cohere_rerank = CohereRerank(api_key=api_key, top_n=5)

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        node_postprocessors=[
            cohere_rerank,
            SimilarityPostprocessor(similarity_cutoff=0.7,
                                    filter_empty=True,
                                    filter_duplicates=True,
                                    filter_similar=False, ),
        ]
    )

    response = query_engine.query(
        f"Answer the following question using only the extracts from the RSM quality manual. If you are uncertain, answer with: \'I'm unable to answer your question. Could you refrase the question?\'.\nQuestion: '{input_text}'. Answer only!")

    print(f"Question: {input_text} \n")
    print(f"Response {response} \n")
    if response.metadata is not None:
        print(f"Source files: \n")
        for key, value in response.metadata.items() or []:
            print(f"- {value['file_name']}")
    else:
        print("No meta data available")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        main(input_text)
    else:
        print("No input provided.")

# # Initialize Ollama and embedding models
# ollama_model_service = OllamaModelService(settings=Settings)
# llm_model = ollama_model_service.llmModel()
# ollama_model_service.embeddingModel()
#
# # Get the loaded index from the Redis server
# vector_store = RedisService(index_name=os.getenv('TOOL_NAME')).load_index()
#
# vector_store_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
#
# retriever = VectorIndexRetriever(index=vector_store_index, similarity_top_k=10)
#
# # api_key = os.getenv('COHERE_API_KEY')
# # cohere_rerank = CohereRerank(api_key=api_key, top_n=3)
#
# query_engine = RetrieverQueryEngine(
#     retriever=retriever,
#     node_postprocessors=[
#         # cohere_rerank,
#         SimilarityPostprocessor(similarity_cutoff=0.7,
#                                 filter_empty=True,
#                                 filter_duplicates=True,
#                                 filter_similar=False, ),
#     ]
# )
#
# my_list = [
#     {"TC001": "Where are errors and success logs stored when jobs are executed?"},
#     # {"TC002": "What is the backup requirement for business data in RSM custom software?"},
#     # {"TC003": "What tools are used for backing up custom software code?"},
#     # {"TC004": "How does the new employee get their druppel (coffee and printing tag) and room key?"},
#     # {"TC005": "Who should be notified to add the new employee to Teams and meetings?"},
#     # {"TC006": "What happens with the ERNA ID when an employee leaves EUR?"},
#     # {"TC007": "Where should the employee's laptop and other devices be returned when leaving?"},
#     # {"TC008": "What kinds of incidents are considered security violations at RSM?"},
#     # {"TC009": "What happens if a security incident involves a SAAS supplier?"},
#     # {"TC010": "What is a SYS-account used for in the envelope procedure?"},
#     # {"TC011": "Who can modify user categories and roles in SAAS systems?"},
#     # {"TC015": "How often are job descriptions reviewed"},
#     # {"TC016": "Where can job descriptions and vacancy texts be accessed?"},
#     # {"TC017": "What are the key positions within the RDIS department?"},
#     # {"TC018": "How do Privacy Officers and Information Security Officers manage back-ups?"},
#     # {"TC019": "What are the key resources identified, and how are they protected?"},
#     # {"TC020": "What certification is required for the BI Consultant role?"},
#     # {"TC021": "What level of education is preferred for the BI Consultant?"},
#     # {"TC022": "What is the BI Consultant’s main responsibility within the organization?"},
#     # {"TC023": "What is the principle of segregation of duties (SoD)?"},
#     # {"TC024": "Why is segregation of duties important in RSM?"},
#     # {"TC025": "What key responsibilities does RDIS have regarding SoD?"},
#     # {"TC026": "How does RDIS ensure that sensitive activities are performed by at least two individuals?"},
#     # {"TC027": "What steps are involved in implementing segregation of duties controls?"},
#     # {"TC028": "What should an end-user do if they notice suspicious activity or a potential breach of SoD controls?"},
#     # {"TC029": "What type of security incidents might violate confidentiality or integrity in RSM?"},
#     # {"TC030": "What is the role of the Response Team in handling security incidents?"},
#     # {"TC031": "How does RDIS handle incidents involving RSM-controlled SaaS?"},
#     # {"TC032": "What steps are taken when a custom software security incident occurs in RSM?"},
#     # {"TC033": "What mitigating actions are taken for security incidents across different system types (SaaS vs. Custom software)?"},
# ]
#
# for item in my_list:
#     # Write each key-value pair to the file
#     for key, value in item.items():
#         # for x in range(5):
#         response = query_engine.query(
#             f"Answer the following question using the RSM quality manual. If you are uncertain, don't answer.\nQuestion: {value}")
#         # file.write(f"{response}\n-------------------------------------------------------\n")
#         # file.write(f"{response.metadata}\n-------------------------------------------------------\n")
#         # print(f"{response.metadata}\n-------------------------------------------------------\n")
#         # print(f"Meta data: \n")
#         # for key, value in response.metadata.items():
#         #     print(f"{value['file_name']}\n")
#         pprint_response(response, show_source=True)
#         # print(f"Response: {response}\n")
#
# exit()
#
# # Open a file in write mode
# with open("data/file.txt", "w") as file:
#     # Loop through the list
#     for item in my_list:
#         # Write each key-value pair to the file
#         for key, value in item.items():
#             # for x in range(5):
#             response = query_engine.query(
#                 f"Answer the following question using the RSM quality manual.\nQuestion: {value}")
#             file.write(f"Response: {response}\nFile origin")
#             for key, value in response.metadata.items():
#                 file.write(f"{value['file_name']}, ")
#             file.write(";;\n")
#             pprint_response(response, show_source=True)
#
# user_query = "?"
# response = query_engine.query(user_query)
# print(response)
