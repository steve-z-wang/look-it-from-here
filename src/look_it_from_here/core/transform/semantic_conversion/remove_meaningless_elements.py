from typing import Optional
from ...semantic_node import SemanticElementNode, SemanticTextNode, SemanticNode
from ...constants import INTERACTIVE_ELEMENTS


def remove_empty_elements(node: SemanticElementNode) -> Optional[SemanticElementNode]:
    """
    Remove elements that have no semantic value and no children.

    These are essentially meaningless leaf nodes that don't contribute anything.
    """
    # Process children
    filtered_children = []
    for child in node.content:
        if isinstance(child, SemanticElementNode):
            # Recursively process element children
            filtered_child = remove_empty_elements(child)
            if filtered_child is not None:
                filtered_children.append(filtered_child)
        elif isinstance(child, SemanticTextNode):
            # Always keep text nodes (they're never "empty")
            filtered_children.append(child)

    # Create new node with filtered children
    result = node.copy(include_children=False)
    for child in filtered_children:
        result.add_child(child)

    # If this node has no attributes and no children, remove it
    # (empty elements like <div></div> with no attributes)
    if not result.attributes and not result.content:
        return None

    return result


def remove_meaningless_wrappers(node: SemanticElementNode) -> SemanticNode:
    """
    Remove elements that have exactly one child and no semantic value.

    These are unnecessary wrapper elements that don't add meaning.
    This includes spans/divs that only contain text without any attributes.
    """
    # First, recursively process all element children
    processed_children = []
    for child in node.content:
        if isinstance(child, SemanticElementNode):
            processed_child = remove_meaningless_wrappers(child)
            # The processed child might now be a text node if wrapper was removed
            processed_children.append(processed_child)
        elif isinstance(child, SemanticTextNode):
            processed_children.append(child)

    # Create new node with processed children
    result = node.copy(include_children=False)
    for child in processed_children:
        result.add_child(child)

    # Apply collapse rule: element with 1 child and no attributes
    # BUT preserve interactive elements even without attributes
    if len(result.content) == 1 and not result.attributes and result.tag.lower() not in INTERACTIVE_ELEMENTS:
        return result.content[0]

    return result


def remove_meaningless_elements_pass(node: SemanticElementNode) -> Optional[SemanticElementNode]:
    """
    Remove semantically meaningless elements from the tree.

    This is a two-pass process:
    1. Remove empty elements (no semantic value, no children)
    2. Remove meaningless wrappers (no semantic value, exactly 1 child)

    Args:
        node: SemanticElementNode tree

    Returns:
        Tree with meaningless elements removed, or None if root should be removed
    """
    # First pass: remove empty elements (meaningless leaves)
    after_empty_removal = remove_empty_elements(node)
    if after_empty_removal is None:
        return None

    # Second pass: remove meaningless wrappers
    after_wrapper_removal = remove_meaningless_wrappers(after_empty_removal)

    # The result should still be an element node (we don't expect the root to become a text node)
    if isinstance(after_wrapper_removal, SemanticElementNode):
        return after_wrapper_removal
    else:
        # This shouldn't happen for the root, but handle gracefully
        return None