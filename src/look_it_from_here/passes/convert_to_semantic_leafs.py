from typing import Set
from ..html_display_node import HTMLDisplayNode


# Tags that should be treated as leaf nodes (children are not semantically meaningful)
LEAF_TAGS: Set[str] = {'svg'}


def convert_to_semantic_leafs_pass(display_node: HTMLDisplayNode) -> HTMLDisplayNode:
    """
    Convert certain tags to leaf nodes by removing their children.

    Some elements like SVG have children that are implementation details
    rather than semantic content, so we treat them as leaf nodes for
    cleaner semantic trees.

    Args:
        display_node: HTMLDisplayNode to process

    Returns:
        HTMLDisplayNode with specified tags converted to leaf nodes
    """
    # For leaf tags, don't process children - treat as leaf nodes
    if display_node.tag in LEAF_TAGS:
        # Create a copy without children
        leaf_node = display_node.copy(include_children=False)
        return leaf_node

    # For non-leaf tags, recursively process children
    processed_children = []
    for child in display_node.children:
        processed_child = convert_to_semantic_leafs_pass(child)
        processed_children.append(processed_child)

    # Create new node with processed children
    processed_node = display_node.copy(include_children=False)
    for child in processed_children:
        processed_node.add_child(child)

    return processed_node