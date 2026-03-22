import faiss
import numpy as np
from typing import List, Tuple

class VectorStoreManager:
    """
    Utility for managing FAISS indexes for lightning-fast candidate retrieval.
    """

    def __init__(self, dimension: int = 384): # Default for all-MiniLM-L6-v2
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.id_to_uuid = {} # Map Index Internal ID -> Database UUID

    def add_vectors(self, vectors: List[List[float]], uuids: List[str]):
        """
        Adds multiple vectors with their corresponding database UUIDs.
        """
        # FAISS expectations
        v_np = np.array(vectors).astype('float32')
        
        # Start adding
        start_idx = self.index.ntotal
        self.index.add(v_np)
        
        for i, uuid in enumerate(uuids):
            self.id_to_uuid[start_idx + i] = uuid

    def search(self, query_vector: List[float], k: int = 5) -> List[Tuple[str, float]]:
        """
        Searches for the k closest vectors and returns their UUIDs and distances.
        """
        q_v = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(q_v, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx in self.id_to_uuid:
                results.append((self.id_to_uuid[idx], float(distances[0][i])))
                
        return results
