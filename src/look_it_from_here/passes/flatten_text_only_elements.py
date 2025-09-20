from typing import Set
from ..html_display_node import HTMLDisplayNode


# Tags whose text should be merged with parent when they have no children
TEXT_ONLY_TAGS: Set[str] = {'div', 'span', 'em', 'strong', 'i', 'b', 'u', 'small', 'mark'}


def flatten_text_only_elements_pass(node: HTMLDisplayNode) -> HTMLDisplayNode:
    """
    Merge text from text-only elements into parent nodes.

    Rule: If an element has only text content and no children,
    merge its text into the parent and remove the element.

    Args:
        node: HTMLDisplayNode tree

    Returns:
        Tree with styling text merged into parents
    """
    # First, recursively process all children
    processed_children = []
    for child in node.children:
        processed_child = flatten_text_only_elements_pass(child)
        processed_children.append(processed_child)

    # Check if ALL children are text-only elements that can be flattened
    text_only_children = []
    non_text_children = []

    for child in processed_children:
        if (child.tag in TEXT_ONLY_TAGS and
            len(child.children) == 0 and
            child.text):
            text_only_children.append(child)
        else:
            non_text_children.append(child)

    # Create new node
    merged = node.copy(include_children=False)

    # Only flatten if ALL children are text-only elements
    if text_only_children and not non_text_children:
        # All children are text-only, merge their texts
        combined_texts = []
        if merged.text:
            combined_texts.append(merged.text)
        combined_texts.extend(child.text for child in text_only_children)
        merged.text = ' '.join(combined_texts)
        # Don't add children since we flattened them
    else:
        # Mixed content or non-text children exist, keep all children as-is
        for child in processed_children:
            merged.add_child(child)

    return merged