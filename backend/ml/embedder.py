"""
BERT Sentence Embedder — with offline TF-IDF fallback.

If 'all-MiniLM-L6-v2' cannot be loaded (network blocked, first run),
the module falls back to a local TF-IDF vectorizer so the API still
works without any internet connection.
"""
import time
from typing import List, Union
import numpy as np


def _try_load_bert():
    """Attempt to load the BERT model; return None if unavailable."""
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as e:
        print(f"[Embedder] BERT unavailable ({e}), using TF-IDF fallback.")
        return None


class BERTEmbedder:
    """
    Wraps sentence-transformers with a TF-IDF fallback for offline environments.
    API is identical regardless of which backend is active.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._bert = _try_load_bert()
        self._tfidf = None          # lazy-init TF-IDF only when needed
        self._vectorizer = None

        if self._bert:
            print(f"[Embedder] Loaded BERT model: {self.model_name}")
        else:
            self._init_tfidf()

    # ------------------------------------------------------------------
    # TF-IDF fallback initialisation
    # ------------------------------------------------------------------
    def _init_tfidf(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import TruncatedSVD
        import pickle, os

        # We fit on a small seed corpus so the vectorizer is consistent
        seed = [
            "python machine learning scikit sql pandas data visualization",
            "software engineering backend api javascript react frontend",
            "data science neural network deep learning nlp statistics",
            "java spring microservices kubernetes docker devops cloud",
            "communication problem solving analytical leadership management",
        ]
        self._vectorizer = TfidfVectorizer(max_features=5000)
        raw_matrix = self._vectorizer.fit_transform(seed)

        # Project to 384 dims (same as MiniLM) with TruncatedSVD
        n_components = min(384, raw_matrix.shape[1] - 1)
        self._svd = TruncatedSVD(n_components=n_components, random_state=42)
        self._svd.fit(raw_matrix)
        print(f"[Embedder] TF-IDF+SVD fallback ready (dims={n_components}).")

    def _tfidf_embed(self, text: str) -> np.ndarray:
        vec = self._vectorizer.transform([text])
        reduced = self._svd.transform(vec)           # (1, n_components)
        # Pad to 384 if SVD produced fewer components
        if reduced.shape[1] < 384:
            pad = np.zeros((1, 384 - reduced.shape[1]))
            reduced = np.hstack([reduced, pad])
        return reduced[0]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def embed(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Generate embeddings for one or more texts."""
        if isinstance(texts, str):
            texts = [texts]

        start = time.time()
        if self._bert:
            embeddings = self._bert.encode(texts)
        else:
            embeddings = np.array([self._tfidf_embed(t) for t in texts])

        elapsed = time.time() - start
        print(
            f"[Embedder] model={self.model_name} | n={len(texts)} | "
            f"shape={embeddings.shape} | t={elapsed:.3f}s"
        )
        return embeddings

    def get_embedding(self, text: str) -> List[float]:
        """Return a flat float list for a single text (DB-storable)."""
        return self.embed(text)[0].tolist()
