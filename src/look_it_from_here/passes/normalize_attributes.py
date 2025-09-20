from ..semantic_node import SemanticElementNode, SemanticTextNode


def normalize_attributes_pass(node: SemanticElementNode) -> SemanticElementNode:
    """
    Clean and deduplicate data in display nodes.

    This pass:
    1. Trims whitespace from all attribute values
    2. Removes empty values after trimming
    3. Deduplicates attribute values, keeping first occurrence
    4. Trims text node content

    Args:
        node: SemanticElementNode tree

    Returns:
        Tree with cleaned data
    """
    def trim_attributes(raw_attributes: list) -> list:
        """Trim all values in the attributes list."""
        trimmed_attributes = []
        for key, value in raw_attributes:
            trimmed_value = value.strip()
            if trimmed_value:  # Only keep non-empty after trim
                trimmed_attributes.append((key, trimmed_value))
        return trimmed_attributes

    def deduplicate_attributes(trimmed_attributes: list, tag_value: str) -> list:
        """Remove duplicate attribute values, keeping first occurrence."""
        seen_values = set()
        final_attributes = []

        # Add tag value to seen set
        seen_values.add(tag_value)

        for key, value in trimmed_attributes:
            if value not in seen_values:
                final_attributes.append((key, value))
                seen_values.add(value)

        return final_attributes

    # Process children
    cleaned_children = []
    for child in node.children:
        if isinstance(child, SemanticElementNode):
            # Recursively process element children
            cleaned_child = normalize_attributes_pass(child)
            cleaned_children.append(cleaned_child)
        elif isinstance(child, SemanticTextNode):
            # Trim text node content
            trimmed_content = child.content.strip()
            if trimmed_content:  # Only keep non-empty text nodes
                cleaned_children.append(SemanticTextNode(trimmed_content))
            # If empty after trim, don't add the text node (effectively removes it)

    # Create new node without children
    cleaned = node.copy(include_children=False)

    # Clean this node's attributes: trim → deduplicate
    trimmed_attributes = trim_attributes(cleaned.attributes)
    final_attributes = deduplicate_attributes(trimmed_attributes, cleaned.tag)
    cleaned.attributes = final_attributes

    # Add cleaned children
    for child in cleaned_children:
        cleaned.add_child(child)

    return cleaned