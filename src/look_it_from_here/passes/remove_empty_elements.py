from typing import Optional
from ..html_display_node import HTMLDisplayNode


def remove_empty_elements_pass(node: HTMLDisplayNode) -> Optional[HTMLDisplayNode]:
    """
    Remove elements that have no semantic value (no text, no attributes).

    Rule: If an element has no text, no attributes, and no children with semantic value,
    remove it from the tree.

    Args:
        node: HTMLDisplayNode tree

    Returns:
        Tree with empty elements removed, or None if this node should be removed
    """
    # First, recursively process all children
    filtered_children = []
    for child in node.children:
        filtered_child = remove_empty_elements_pass(child)
        if filtered_child is not None:
            filtered_children.append(filtered_child)

    # Create new node with filtered children
    result = node.copy(include_children=False)
    for child in filtered_children:
        result.add_child(child)

    # If this node has no semantic value and no children, remove it
    if not result.has_semantic_value() and not result.children:
        return None

    return result