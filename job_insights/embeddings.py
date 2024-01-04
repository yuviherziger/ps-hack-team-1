import os

from motor.motor_asyncio import AsyncIOMotorClient
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Union

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
db_name = "hackathon"
coll_name = "job_postings"
mongo_client = AsyncIOMotorClient(os.environ.get("MONGODB_URI"))


async def get_transformer_embeddings(query: str) -> Union[List[float], object]:
    embeddings = model.encode(query, convert_to_tensor=True)
    return embeddings.tolist()


async def search_similar_docs(query: str, limit: int = 5) -> List[Dict]:
    query_embeddings: List = await get_transformer_embeddings(query)
    db = mongo_client[db_name]
    coll = db[coll_name]
    docs = []
    async for doc in coll.aggregate([
        {
            "$vectorSearch": {
                "index": "job_index",
                "queryVector": query_embeddings,
                "path": "embedding_summary",
                "numCandidates": 100,
                "limit": limit
            }
        },
        {
            "$project": {
                "embedding_summary": 0,
                "_id": 0,
                "score": {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]):
        docs.append(doc)
    return docs
