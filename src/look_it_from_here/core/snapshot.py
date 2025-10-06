from typing import Dict, Optional, Any, List, Union, Tuple
from .dom_node import DOMElementNode
from .semantic_node import SemanticElementNode, SemanticTextNode
from .interfaces import WebElement, Snapshot
from .embeddings import Embedder
from .element_selector import ElementSelector


class WebSnapshot(Snapshot):
    """
    Snapshot containing semantic tree and element mappings for interaction.
    Also stores the original HTML tree and intermediate mappings for full detail.
    """

    def __init__(
        self,
        html_tree: Optional[DOMElementNode],
        semantic_tree: Optional[SemanticElementNode],
        dom_id_to_webelement: Dict[str, WebElement],
        dom_id_to_semantic_id: Dict[str, str],
        semantic_id_to_embedding: Optional[Dict[str, List[float]]] = None,
        embedder: Optional[Embedder] = None
    ):
        self.html_tree = html_tree
        self.semantic_tree = semantic_tree
        self.dom_id_to_webelement = dom_id_to_webelement
        self.dom_id_to_semantic_id = dom_id_to_semantic_id
        self.semantic_id_to_embedding = semantic_id_to_embedding or {}

        # Build semantic_id_to_webelement mapping
        self.semantic_id_to_webelement: Dict[str, WebElement] = {}
        for dom_id, semantic_id in dom_id_to_semantic_id.items():
            if dom_id in dom_id_to_webelement:
                self.semantic_id_to_webelement[semantic_id] = dom_id_to_webelement[dom_id]

        # Initialize element selector
        self._element_selector = ElementSelector(embedder)

    def to_dict(self) -> Optional[Dict[str, Any]]:
        """
        Convert the semantic tree to a dictionary representation.

        Returns:
            Dictionary with tag and semantic data
        """
        if self.semantic_tree:
            return self._semantic_tree_to_dict(self.semantic_tree)
        return None

    def select_elements(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0
    ) -> List[Tuple[str, WebElement, float]]:
        """
        Select elements using natural language query with similarity scoring.

        Args:
            query: Natural language description of desired elements
            top_k: Maximum number of elements to return
            threshold: Minimum similarity score (0.0 to 1.0)

        Returns:
            List of (semantic_id, element, similarity_score) tuples, sorted by score
        """
        return self._element_selector.select_elements(self, query, top_k, threshold)

    def select_element(
        self,
        query: str,
        threshold: float = 0
    ) -> Optional[Tuple[str, WebElement, float]]:
        """
        Select the single best matching element using natural language query.

        Args:
            query: Natural language description of desired element
            threshold: Minimum similarity score (0.0 to 1.0)

        Returns:
            Tuple of (semantic_id, element, similarity_score) or None if no match
        """
        return self._element_selector.select_element(self, query, threshold)
   
    
    def _semantic_tree_to_dict(self, node: SemanticElementNode) -> Dict[str, Any]:
        """
        Convert a semantic tree to a simple dictionary representation.

        Args:
            node: SemanticElementNode to convert (must be non-None)

        Returns:
            Dictionary with tag and semantic data
        """
        # Start with tag
        result = {"tag": node.tag}

        # Add attributes
        for key, value in node.attributes:
            result[key] = value

        # Build children list
        children: List[Union[Dict[str, Any], str]] = []
        for child in node.content:
            if isinstance(child, SemanticElementNode):
                child_dict = self._semantic_tree_to_dict(child)
                children.append(child_dict)
            elif isinstance(child, SemanticTextNode):
                children.append(child.text)

        # Only include content field if there are any children
        if children:
            result["content"] = children

        return result

