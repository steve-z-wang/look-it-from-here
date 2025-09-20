from typing import Set
from html_display_node import HTMLDisplayNode


# Wrapper tags that can be collapsed
WRAPPER_TAGS: Set[str] = {'div', 'span'}


def collapse_pass(node: HTMLDisplayNode) -> HTMLDisplayNode:
    """
    Collapse wrapper elements that have exactly one child.

    Rule: If a div/span has exactly 1 child element,
    replace the wrapper with that child.

    Args:
        node: HTMLDisplayNode tree

    Returns:
        Tree with collapsed wrappers
    """
    # First, recursively process all children
    collapsed_children = []
    for child in node.children:
        collapsed_child = collapse_pass(child)
        collapsed_children.append(collapsed_child)

    # Create new node with collapsed children
    collapsed = node.copy(include_children=False)
    for child in collapsed_children:
        collapsed.add_child(child)

    # Apply collapse rule for wrapper tags
    if collapsed.role in WRAPPER_TAGS:
        # If wrapper has exactly 1 child, replace with child
        if len(collapsed.children) == 1:
            return collapsed.children[0]

    return collapsed