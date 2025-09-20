from typing import Set
from ..semantic_node import SemanticElementNode, SemanticTextNode


# Tags that should be treated as leaf nodes (children are not semantically meaningful)
LEAF_TAGS: Set[str] = {'svg'}


def convert_to_semantic_leafs_pass(display_node: SemanticElementNode) -> SemanticElementNode:
    """
    Convert certain tags to leaf nodes by removing their children.

    Some elements like SVG have children that are implementation details
    rather than semantic content, so we treat them as leaf nodes for
    cleaner semantic trees.

    Args:
        display_node: SemanticElementNode to process

    Returns:
        SemanticElementNode with specified tags converted to leaf nodes
    """
    # For leaf tags, don't process children - treat as leaf nodes
    if display_node.tag in LEAF_TAGS:
        # Create a copy without children
        leaf_node = display_node.copy(include_children=False)
        return leaf_node

    # For non-leaf tags, recursively process children
    processed_children = []
    for child in display_node.children:
        if isinstance(child, SemanticElementNode):
            # Process element children recursively
            processed_child = convert_to_semantic_leafs_pass(child)
            processed_children.append(processed_child)
        elif isinstance(child, SemanticTextNode):
            # Keep text nodes as-is
            processed_children.append(child)

    # Create new node with processed children
    processed_node = display_node.copy(include_children=False)
    for child in processed_children:
        processed_node.add_child(child)

    return processed_node