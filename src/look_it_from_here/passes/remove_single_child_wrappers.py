from ..html_display_node import HTMLDisplayNode


def remove_single_child_wrappers_pass(node: HTMLDisplayNode) -> HTMLDisplayNode:
    """
    Collapse elements that have exactly one child and no meaningful content.

    Rule: If any element has exactly 1 child, no text, and no attributes,
    replace the wrapper with that child.

    Args:
        node: HTMLDisplayNode tree

    Returns:
        Tree with collapsed wrappers
    """
    # First, recursively process all children
    collapsed_children = []
    for child in node.children:
        collapsed_child = remove_single_child_wrappers_pass(child)
        collapsed_children.append(collapsed_child)

    # Create new node with collapsed children
    collapsed = node.copy(include_children=False)
    for child in collapsed_children:
        collapsed.add_child(child)

    # Apply collapse rule: any element with 1 child and no semantic value
    if len(collapsed.children) == 1 and not collapsed.has_semantic_value():
        return collapsed.children[0]

    return collapsed