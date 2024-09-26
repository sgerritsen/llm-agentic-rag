from llama_index.vector_stores.redis import RedisVectorStore
from redisvl.schema import IndexSchema
from typing import Optional


class RedisService:
    # Default dimensions are for the mxbai-embed-large model
    def __init__(
            self,
            index_name: str,
            dimensions: Optional[int] = 1024,
            overwrite: Optional[bool] = False,
            redis_url: Optional[str] = 'redis://host.docker.internal:6379'
    ):
        self.index_name = index_name
        self.dimensions = dimensions
        self.overwrite = overwrite
        self.redis_url = redis_url
        self.schema = None

    def createIndex(self):
        self.schema = IndexSchema(
            index={
                "name": self.index_name,  # Ensure this is a string
                "prefix": f"{self.index_name}:",
                "key_separator": ":",
                "storage_type": "hash"
            },
            fields=[
                {"name": "id", "type": "tag"},
                {"name": "doc_id", "type": "tag"},
                {"name": "text", "type": "text"},
                {"name": "vector", "type": "vector",
                 "attrs": {
                     "algorithm": "HNSW",
                     "dims": self.dimensions,
                     "distance_metric": "COSINE",
                     "datatype": "FLOAT32"
                 }}
            ],
            version='0.1.0'
        )

    def createVectorStore(self):
        if self.schema is None:
            self.createIndex()
        # Initialize RedisVectorStore
        redis_store = RedisVectorStore(schema=self.schema, redis_url=self.redis_url, overwrite=self.overwrite)
        return redis_store
