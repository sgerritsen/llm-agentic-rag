from llama_index.core import Settings
from .redis_service import RedisService
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor


class SimpleRagQueryEngine():
    def __init__(self, documents: list, index_name: str):
        self.documents = documents
        self.index_name = index_name

    def buildQueryEngine(self):
        redis_store = RedisService(index_name=self.index_name, dimensions=1024, overwrite=True).createVectorStore()

        # Create storage context and index
        storage_context = StorageContext.from_defaults(vector_store=redis_store)
        vector_store = VectorStoreIndex.from_documents(documents=self.documents, storage_context=storage_context)

        retriever = VectorIndexRetriever(index=vector_store, similarity_top_k=4, verbose=True)

        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.6,
                                                         filter_empty=True,
                                                         filter_duplicates=True,
                                                         filter_similar=False, ), ]
        )

        return query_engine
