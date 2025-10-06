from typing import List, Optional, Tuple, Dict, Any
import numpy as np
from .interfaces import WebElement, Snapshot
from .embeddings import Embedder


class ElementSelector:
    def __init__(self, embedder: Optional[Embedder] = None):
        self.embedder = embedder or Embedder()

    def select_elements(
        self,
        snapshot: Snapshot,
        query: str,
        top_k: int = 5,
        threshold: float = 0.5
    ) -> List[Tuple[str, WebElement, float]]:
        """
        Select elements using natural language query with similarity scoring.

        Args:
            snapshot: WebSnapshot containing semantic tree and embeddings
            query: Natural language description of desired elements
            top_k: Maximum number of elements to return
            threshold: Minimum similarity score (0.0 to 1.0)

        Returns:
            List of (semantic_id, element, similarity_score) tuples, sorted by score
        """
        if not snapshot.semantic_id_to_embedding:
            return []

        # Get query embedding
        query_embedding = self.embedder.create_embedding(query)

        # Calculate similarities for all elements
        similarities = []
        for semantic_id, element_embedding in snapshot.semantic_id_to_embedding.items():
            similarity = self._cosine_similarity(query_embedding, element_embedding)

            # Only include if above threshold and element exists
            if similarity >= threshold and semantic_id in snapshot.semantic_id_to_webelement:
                element = snapshot.semantic_id_to_webelement[semantic_id]
                similarities.append((semantic_id, element, similarity))

        # Sort by similarity (descending) and return top_k
        similarities.sort(key=lambda x: x[2], reverse=True)
        return similarities[:top_k]

    def select_element(
        self,
        snapshot: Snapshot,
        query: str,
        threshold: float = 0.5
    ) -> Optional[Tuple[str, WebElement, float]]:
        """
        Select the single best matching element using natural language query.

        Args:
            snapshot: WebSnapshot containing semantic tree and embeddings
            query: Natural language description of desired element
            threshold: Minimum similarity score (0.0 to 1.0)

        Returns:
            Tuple of (semantic_id, element, similarity_score) or None if no match
        """
        results = self.select_elements(snapshot, query, top_k=1, threshold=threshold)
        return results[0] if results else None

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two embedding vectors.

        Args:
            vec1: First embedding vector
            vec2: Second embedding vector

        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        # Convert to numpy arrays for efficient computation
        a = np.array(vec1)
        b = np.array(vec2)

        # Calculate cosine similarity
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        # Avoid division by zero
        if norm_a == 0 or norm_b == 0:
            return 0.0

        # Return similarity clamped to [0, 1] range
        similarity = dot_product / (norm_a * norm_b)
        return max(0.0, min(1.0, similarity))