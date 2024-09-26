from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine


class TopKRetriever():
    def __init__(self, top_ks: list, vector_store_index: VectorStoreIndex, query: str):
        self.top_ks = top_ks
        self.vector_store_index = vector_store_index
        self.query = query

    def compare(self):
        results = []
        # Make sure that the top_ks list is passed correctly and is not redefined here.
        for top_k in self.top_ks:
            # Set the retriever to the current value of top_k.
            retriever = self.vector_store_index.as_retriever(similarity_top_k=top_k)
            #  Create a new query engine with the retriever configured.
            query_engine = RetrieverQueryEngine.from_args(retriever, llm=Settings.llm)
            # Performs the consultation.
            response = query_engine.query(self.query)
            # Save the result in the results list
            results.append({
                "top_k": top_k,
                "text": str(response)
            })

        # for item in results:
        #     print('top_k ' + str(item['top_k']) + ' ' + item['text'] + '\n ......................')
        return results
