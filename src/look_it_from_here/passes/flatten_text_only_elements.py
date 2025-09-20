from typing import Set
from ..semantic_node import SemanticElementNode, SemanticTextNode


# Tags whose text should be merged with parent when they have only text content
TEXT_ONLY_TAGS: Set[str] = {'div', 'span', 'em', 'strong', 'i', 'b', 'u', 'small', 'mark'}


def flatten_text_only_wrappers(node: SemanticElementNode) -> SemanticElementNode:
    """
    Convert text-only elements to text nodes.

    Rule: If ALL element children are text-only tags that contain only text nodes,
    convert those elements to text nodes and add them to the parent.
    """
    # First, recursively process all element children
    processed_children = []
    for child in node.children:
        if isinstance(child, SemanticElementNode):
            processed_child = flatten_text_only_wrappers(child)
            processed_children.append(processed_child)
        elif isinstance(child, SemanticTextNode):
            processed_children.append(child)

    # Separate element and text children
    element_children = [child for child in processed_children if isinstance(child, SemanticElementNode)]
    text_children = [child for child in processed_children if isinstance(child, SemanticTextNode)]

    # Check if ALL element children are text-only elements that can be flattened
    text_only_elements = []
    non_text_elements = []

    for child in element_children:
        if (child.tag in TEXT_ONLY_TAGS and
            len(child.get_element_children()) == 0 and  # No element children
            len(child.get_text_children()) > 0):  # Has text children
            text_only_elements.append(child)
        else:
            non_text_elements.append(child)

    # Create new node
    result = node.copy(include_children=False)

    # Only flatten if ALL element children are text-only elements
    if text_only_elements and not non_text_elements:
        # Add existing text children first
        for text_child in text_children:
            result.add_child(text_child)

        # Convert text-only elements to text nodes
        for text_only_element in text_only_elements:
            for text_node in text_only_element.get_text_children():
                result.add_child(text_node)
    else:
        # Mixed content or non-text element children exist, keep all children as-is
        for child in processed_children:
            result.add_child(child)

    return result


def merge_adjacent_text_nodes(node: SemanticElementNode) -> SemanticElementNode:
    """
    Merge adjacent text nodes into single text nodes.

    This combines text nodes that are next to each other with a space.
    """
    # First, recursively process all element children
    processed_children = []
    for child in node.children:
        if isinstance(child, SemanticElementNode):
            processed_child = merge_adjacent_text_nodes(child)
            processed_children.append(processed_child)
        elif isinstance(child, SemanticTextNode):
            processed_children.append(child)

    # Create new node
    result = node.copy(include_children=False)

    # Merge adjacent text nodes
    merged_children = []
    current_text_parts = []

    for child in processed_children:
        if isinstance(child, SemanticTextNode):
            # Collect adjacent text nodes
            current_text_parts.append(child.content)
        else:
            # Non-text node, flush any accumulated text
            if current_text_parts:
                merged_text = ' '.join(current_text_parts)
                merged_children.append(SemanticTextNode(merged_text))
                current_text_parts = []
            merged_children.append(child)

    # Don't forget any remaining text at the end
    if current_text_parts:
        merged_text = ' '.join(current_text_parts)
        merged_children.append(SemanticTextNode(merged_text))

    # Add all merged children
    for child in merged_children:
        result.add_child(child)

    return result


def flatten_text_only_elements_pass(node: SemanticElementNode) -> SemanticElementNode:
    """
    Flatten text-only elements into text nodes and merge adjacent text nodes.

    This is a two-pass process:
    1. Convert text-only wrapper elements to text nodes
    2. Merge adjacent text nodes together

    Args:
        node: SemanticElementNode tree

    Returns:
        Tree with text-only elements flattened and text nodes merged
    """
    # First pass: convert text-only elements to text nodes
    flattened = flatten_text_only_wrappers(node)

    # Second pass: merge adjacent text nodes
    merged = merge_adjacent_text_nodes(flattened)

    return merged