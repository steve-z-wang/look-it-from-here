from typing import Dict, Optional, Any
from .html_tree_node import HTMLTreeNode
from .html_display_node import HTMLDisplayNode
from .interfaces import WebElement, Snapshot
from .pipeline import display_tree_to_dict, display_tree_to_xml


class WebSnapshot(Snapshot):
    """
    Snapshot containing semantic tree and element mappings for interaction.
    Also stores the original HTML tree and intermediate mappings for full detail.
    """

    def __init__(
        self,
        html_tree: Optional[HTMLTreeNode],
        semantic_tree: Optional[HTMLDisplayNode],
        tree_to_element: Dict[str, WebElement],
        tree_to_display: Dict[str, str]
    ):
        self.html_tree = html_tree
        self.semantic_tree = semantic_tree
        self.tree_to_element = tree_to_element
        self.tree_to_display = tree_to_display

        # Build display_to_element mapping
        self.display_to_element: Dict[str, WebElement] = {}
        for tree_id, display_id in tree_to_display.items():
            if tree_id in tree_to_element:
                self.display_to_element[display_id] = tree_to_element[tree_id]

    def to_dict(self) -> Optional[Dict[str, Any]]:
        """
        Convert the semantic tree to a dictionary representation.

        Returns:
            Dictionary with role, text, and children fields
        """
        if self.semantic_tree:
            return display_tree_to_dict(self.semantic_tree)
        return None

    def to_xml(self) -> Optional[str]:
        """
        Convert the semantic tree to XML representation.

        Returns:
            XML string representation or None if no semantic tree
        """
        if self.semantic_tree:
            return display_tree_to_xml(self.semantic_tree)
        return None

    def get_element(self, display_node_id: str) -> Optional[WebElement]:
        """
        Get the WebElement corresponding to a display node ID.

        Args:
            display_node_id: ID of the display node

        Returns:
            WebElement or None if not found
        """
        return self.display_to_element.get(display_node_id)