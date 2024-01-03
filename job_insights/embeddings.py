import os

from sentence_transformers import SentenceTransformer
from typing import List, Dict, Union
from pymongo import MongoClient

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
db_name = "hackathon"
coll_name = "job_postings"
mongo_client = MongoClient(os.environ.get("MONGODB_URI"))


def get_transformer_embeddings(query: str) -> Union[List[float], object]:
    embeddings = model.encode(query, convert_to_tensor=True)
    return embeddings.tolist()


def search_similar_docs(query: str, limit: int = 5) -> List[Dict]:
    query_embeddings: List = get_transformer_embeddings(query)
    db = mongo_client[db_name]
    coll = db[coll_name]
    res = coll.aggregate([
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
                'score': {
                    '$meta': 'searchScore'
                }
            }
        }
    ])
    return list(res)
