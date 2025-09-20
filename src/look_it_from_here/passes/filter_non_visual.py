from typing import Optional
from ..html_tree_node import HTMLTreeNode


# Tags that should be excluded from display
EXCLUDED_TAGS = {'script', 'style', 'meta', 'link', 'head', 'noscript', 'title'}


def filter_non_visual_pass(node: HTMLTreeNode) -> Optional[HTMLTreeNode]:
    """
    Remove nodes that should never be displayed.

    This pass filters out script, style, meta, and other non-visual elements
    that contribute to the large text content but aren't useful for interaction.

    Args:
        node: HTMLTreeNode tree

    Returns:
        HTMLTreeNode tree with excluded nodes removed, None if node itself is excluded
    """
    # Check if this node should be excluded
    if node.tag in EXCLUDED_TAGS:
        return None

    # Process children, filtering out excluded ones
    filtered_children = []
    for child in node.children:
        filtered_child = filter_non_visual_pass(child)
        if filtered_child:
            filtered_children.append(filtered_child)

    # Create new node with filtered children
    filtered_node = HTMLTreeNode(
        tag=node.tag,
        text=node.text,
        attributes=node.attributes.copy(),
        is_visible=node.is_visible
    )
    filtered_node.id = node.id  # Preserve the ID

    # Add filtered children
    for child in filtered_children:
        filtered_node.add_child(child)

    return filtered_node