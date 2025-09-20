from typing import Optional, Set
from ..html_display_node import HTMLDisplayNode


# Wrapper/container tags that should be filtered out when they have no meaningful content
FILTERABLE_TAGS: Set[str] = {'div', 'span'}


def remove_empty_containers_pass(display_node: HTMLDisplayNode) -> Optional[HTMLDisplayNode]:
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
        meaningful_child = remove_empty_containers_pass(child)
        if meaningful_child:
            meaningful_children.append(meaningful_child)

    # Check if this node has meaningful content
    has_text = display_node.text is not None and display_node.text.strip()
    has_attributes = len(display_node.attributes) > 0
    has_meaningful_content = has_text or has_attributes or len(meaningful_children) > 0

    # Only filter out nodes that are filterable tags AND have no meaningful content
    # Non-filterable tags (like img, button, etc.) are always preserved
    if display_node.tag in FILTERABLE_TAGS and not has_meaningful_content:
        return None

    # Create a copy without children first
    filtered_node = display_node.copy(include_children=False)

    # Add only meaningful children
    for child in meaningful_children:
        filtered_node.add_child(child)

    return filtered_node