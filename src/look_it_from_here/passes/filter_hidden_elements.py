from typing import Optional
from ..dom_node import DOMElementNode, DOMTextNode


def filter_hidden_elements_pass(node: DOMElementNode) -> Optional[DOMElementNode]:
    """
    Filter out invisible nodes from the tree.
    Returns None if the node is invisible, otherwise returns a copy with only visible children.

    Args:
        node: The DOMElementNode to filter

    Returns:
        Optional[DOMElementNode]: Filtered node or None if invisible
    """
    # Check visibility first
    if not node.is_visible:
        return None

    # Create copy without children
    filtered_node = node.copy(include_children=False)

    # Process children - filter element children and keep text children
    for child in node.children:
        if isinstance(child, DOMElementNode):
            # Filter element children based on visibility
            filtered_child = filter_hidden_elements_pass(child)
            if filtered_child is not None:
                filtered_node.add_child(filtered_child)
        elif isinstance(child, DOMTextNode):
            # Text nodes are always included (they don't have visibility)
            filtered_node.add_child(child)

    return filtered_node