from typing import Dict, Optional, Any
from .dom_node import DOMElementNode
from .semantic_node import SemanticElementNode
from .interfaces import WebElement, Snapshot
from .transform import semantic_tree_to_dict


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
        tree_to_semantic: Dict[str, str]
    ):
        self.html_tree = html_tree
        self.semantic_tree = semantic_tree
        self.tree_to_element = tree_to_element
        self.tree_to_semantic = tree_to_semantic

        # Build semantic_to_element mapping
        self.semantic_to_element: Dict[str, WebElement] = {}
        for tree_id, semantic_id in tree_to_semantic.items():
            if tree_id in tree_to_element:
                self.semantic_to_element[semantic_id] = tree_to_element[tree_id]

    def to_dict(self) -> Optional[Dict[str, Any]]:
        """
        Convert the semantic tree to a dictionary representation.

        Returns:
            Dictionary with role, text, and children fields
        """
        if self.semantic_tree:
            return semantic_tree_to_dict(self.semantic_tree)
        return None


    def get_element(self, semantic_node_id: str) -> Optional[WebElement]:
        """
        Get the WebElement corresponding to a semantic node ID.

        Args:
            semantic_node_id: ID of the semantic node

        Returns:
            WebElement or None if not found
        """
        return self.semantic_to_element.get(semantic_node_id)