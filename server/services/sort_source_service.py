from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

class SortSourceService:
  def __init__(self):
    self.embedding_model = SentenceTransformer("all-miniLM-L6-v2")
  
  def sort_sources(self, query: str, search_results: List[dict]):
    relevant_docs = []
    query_embedding = self.embedding_model.encode(query)
    
    for result in search_results:
      try:
        content = result.get('content')
        if not content:
          continue

        res_embedding = self.embedding_model.encode(content)
        similarity = (np.dot(query_embedding, res_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(res_embedding)))
        result['relevance_score'] = similarity

        if similarity > 0.3:
          relevant_docs.append(result)
      except Exception as e:
        print(f"Skipping result due to error...")
        continue

    return sorted(relevant_docs, key=lambda x: x['relevance_score'], reverse=True)