from typing import Dict, Optional, Any, List, Union
from .dom_node import DOMElementNode
from .semantic_node import SemanticElementNode, SemanticTextNode
from .interfaces import WebElement, Snapshot


class WebSnapshot(Snapshot):
    """
    Snapshot containing semantic tree and element mappings for interaction.
    Also stores the original HTML tree and intermediate mappings for full detail.
    """

    def __init__(
        self,
        html_tree: Optional[DOMElementNode],
        semantic_tree: Optional[SemanticElementNode],
        tree_to_element: Dict[str, WebElement],
        tree_to_semantic: Dict[str, str],
        semantic_to_embedding: Optional[Dict[str, List[float]]] = None
    ):
        self.html_tree = html_tree
        self.semantic_tree = semantic_tree
        self.tree_to_element = tree_to_element
        self.tree_to_semantic = tree_to_semantic
        self.semantic_to_embedding = semantic_to_embedding or {}

        # Build semantic_to_element mapping
        self.semantic_to_element: Dict[str, WebElement] = {}
        for tree_id, semantic_id in tree_to_semantic.items():
            if tree_id in tree_to_element:
                self.semantic_to_element[semantic_id] = tree_to_element[tree_id]

    def to_dict(self) -> Optional[Dict[str, Any]]:
        """
        Convert the semantic tree to a dictionary representation.

        Returns:
            Dictionary with tag and semantic data
        """
        if self.semantic_tree:
            return self._semantic_tree_to_dict(self.semantic_tree)
        return None

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


    def get_element(self, semantic_node_id: str) -> Optional[WebElement]:
        """
        Get the WebElement corresponding to a semantic node ID.

        Args:
            semantic_node_id: ID of the semantic node

        Returns:
            WebElement or None if not found
        """
        return self.semantic_to_element.get(semantic_node_id)

    def get_embedding(self, semantic_node_id: str) -> Optional[List[float]]:
        """
        Get the embedding vector corresponding to a semantic node ID.

        Args:
            semantic_node_id: ID of the semantic node

        Returns:
            Embedding vector or None if not found
        """
        return self.semantic_to_embedding.get(semantic_node_id)