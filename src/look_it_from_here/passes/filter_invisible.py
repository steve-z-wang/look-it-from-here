from typing import Optional
from html_tree_node import HTMLTreeNode


def filter_invisible(node: HTMLTreeNode) -> Optional[HTMLTreeNode]:
    """
    Filter out invisible nodes from the tree.
    Returns None if the node is invisible, otherwise returns a copy with only visible children.

    Args:
        node: The HTMLTreeNode to filter

    Returns:
        Optional[HTMLTreeNode]: Filtered node or None if invisible
    """
    # Check visibility first
    if not node.is_visible:
        return None

    # Create copy without children
    filtered_node = node.copy(include_children=False)

    # Only add visible children recursively
    for child in node.children:
        filtered_child = filter_invisible(child)
        if filtered_child is not None:
            filtered_node.add_child(filtered_child)

    return filtered_node