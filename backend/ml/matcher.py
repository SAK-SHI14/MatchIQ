import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Union

class MatchEngine:
    """
    Match engine to compute similarity between resume and job description.
    """

    @staticmethod
    def calculate_match_score(resume_vector: Union[List[float], np.ndarray],
                              jd_vector: Union[List[float], np.ndarray]) -> float:
        """
        Computes cosine similarity between two vectors and returns a score 0-100.
        """
        # Ensure vectors are numpy arrays and reshaped
        r_v = np.array(resume_vector).reshape(1, -1)
        j_v = np.array(jd_vector).reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(r_v, j_v)[0][0]
        
        # Log requirements
        print(f"Computed cosine_similarity: {similarity:.4f}")
        
        # Return percentage
        return round(float(similarity) * 100, 2)

    @staticmethod
    def batch_match(resume_vectors: List[List[float]],
                    jd_vector: List[float]) -> List[float]:
        """
        Computes match scores for multiple resumes against a single job description.
        """
        # Efficient batch processing
        r_vs = np.array(resume_vectors)
        j_v = np.array(jd_vector).reshape(1, -1)
        
        similarities = cosine_similarity(r_vs, j_v).flatten()
        return [round(float(s) * 100, 2) for s in similarities]
