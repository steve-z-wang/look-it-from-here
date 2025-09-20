from typing import Optional
from html_display_node import HTMLDisplayNode


def content_filter_pass(display_node: HTMLDisplayNode) -> Optional[HTMLDisplayNode]:
    """
    Filter out DisplayNodes that have no meaningful content.

    A node has meaningful content if:
    - It has non-empty text content, OR
    - It has children with meaningful content

    This pass removes empty wrapper elements and nodes that don't
    contribute to the final output.

    Args:
        display_node: HTMLDisplayNode to process

    Returns:
        HTMLDisplayNode with only meaningful children, or None if no meaningful content
    """
    # Process children first (bottom-up), keeping only those with content
    meaningful_children = []
    for child in display_node.children:
        meaningful_child = content_filter_pass(child)
        if meaningful_child:
            meaningful_children.append(meaningful_child)

    # Check if this node has meaningful text content
    has_meaningful_text = bool(display_node.display_text and display_node.display_text.strip())

    # This node has meaningful content if it has text OR meaningful children
    has_meaningful_content = has_meaningful_text or len(meaningful_children) > 0

    # If this node has no meaningful content, filter it out
    if not has_meaningful_content:
        return None

    # Create a copy without children first
    filtered_node = display_node.copy(include_children=False)

    # Add only meaningful children
    for child in meaningful_children:
        filtered_node.add_child(child)

    return filtered_node