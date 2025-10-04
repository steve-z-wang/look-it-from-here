from typing import Dict, Tuple, Optional
from ...dom_node import DOMElementNode
from ...semantic_node import SemanticElementNode
from .convert_to_semantic_nodes import convert_to_semantic_nodes_pass
from .remove_meaningless_elements import remove_meaningless_elements_pass


def create_semantic_tree(html_tree: DOMElementNode) -> Tuple[Optional[SemanticElementNode], Dict[str, str]]:
    """
    Create a semantic tree from an HTML tree.
    Applies rendering, content filtering, and collapsing passes.

    Args:
        html_tree: HTMLTreeNode root (must be non-None)

    Returns:
        Tuple of (
            Optional[HTMLDisplayNode] root with semantic roles,
            Dict mapping tree node IDs to display node IDs
        )
    """
    # Pass 1: Convert tree nodes to semantic nodes
    semantic_tree, tree_to_semantic_mapping = convert_to_semantic_nodes_pass(html_tree)

    if not semantic_tree:
        return None, {}

    # Pass 2: Remove meaningless elements (empty elements + single-child wrappers)
    final_tree = remove_meaningless_elements_pass(semantic_tree)

    if not final_tree:
        return None, {}

    return final_tree, tree_to_semantic_mapping