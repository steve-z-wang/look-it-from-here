from typing import Optional
from ..dom_node import DOMElementNode, DOMTextNode


# Tags that should be excluded from display
EXCLUDED_TAGS = {'script', 'style', 'meta', 'link', 'head', 'noscript', 'title'}


def filter_non_visual_pass(node: DOMElementNode) -> Optional[DOMElementNode]:
    """
    Remove nodes that should never be displayed.

    This pass filters out script, style, meta, and other non-visual elements
    that contribute to the large text content but aren't useful for interaction.

    Args:
        node: DOMElementNode tree

    Returns:
        DOMElementNode tree with excluded nodes removed, None if node itself is excluded
    """
    # Check if this node should be excluded
    if node.tag in EXCLUDED_TAGS:
        return None

    # Process children, filtering out excluded element nodes and keeping text nodes
    filtered_children = []
    for child in node.children:
        if isinstance(child, DOMElementNode):
            # Process element children recursively
            filtered_child = filter_non_visual_pass(child)
            if filtered_child:
                filtered_children.append(filtered_child)
        elif isinstance(child, DOMTextNode):
            # Keep text nodes as-is
            filtered_children.append(child)

    # Create new node with filtered children
    filtered_node = DOMElementNode(
        tag=node.tag,
        attributes=node.attributes.copy(),
        is_visible=node.is_visible
    )
    filtered_node.id = node.id  # Preserve the ID

    # Add filtered children
    for child in filtered_children:
        filtered_node.add_child(child)

    return filtered_node