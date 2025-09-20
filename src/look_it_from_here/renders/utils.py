from html_tree_node import HTMLTreeNode


def extract_text_from_node(node: HTMLTreeNode) -> str:
    """
    Extract all text content from a node and its children.

    This is a shared helper that renderers can use when they want to
    absorb text from their children instead of rendering them separately.

    Args:
        node: The HTMLTreeNode to extract text from

    Returns:
        Combined text content from node and all descendants
    """
    # First check for direct text content
    if node.text:
        return node.text

    # Collect text from all children recursively
    texts = []
    for child in node.children:
        child_text = _extract_text_recursive(child)
        if child_text:
            texts.append(child_text)

    # If no text found in content or children, fallback to aria-label
    if not texts:
        return node.attributes.get('aria-label', '')

    return ' '.join(texts)


def _extract_text_recursive(node: HTMLTreeNode) -> str:
    """
    Recursively extract text from a node and all its descendants.

    Args:
        node: The HTMLTreeNode to extract from

    Returns:
        Combined text content
    """
    texts = []

    # Add this node's text
    if node.text:
        texts.append(node.text)

    # Recursively extract from children
    for child in node.children:
        child_text = _extract_text_recursive(child)
        if child_text:
            texts.append(child_text)

    return ' '.join(texts) if texts else ''