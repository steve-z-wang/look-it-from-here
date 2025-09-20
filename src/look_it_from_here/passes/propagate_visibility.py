from ..html_tree_node import HTMLTreeNode


def propagate_visibility_pass(node: HTMLTreeNode) -> HTMLTreeNode:
    """
    Bottom-up visibility propagation pass.

    Rule: If any child is visible, make the parent visible too.
    This fixes cases where parent elements report as invisible but contain visible children.

    Args:
        node: HTMLTreeNode tree

    Returns:
        Tree with corrected visibility information
    """
    # First, recursively process all children
    processed_children = []
    has_visible_child = False

    for child in node.children:
        processed_child = propagate_visibility_pass(child)
        processed_children.append(processed_child)
        if processed_child.is_visible:
            has_visible_child = True

    # Create new node with processed children
    result = node.copy(include_children=False)
    for child in processed_children:
        result.add_child(child)

    # If node was invisible but has visible children, make it visible
    if not result.is_visible and has_visible_child:
        result.is_visible = True

    return result