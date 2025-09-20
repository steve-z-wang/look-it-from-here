from ..html_display_node import HTMLDisplayNode


def normalize_attributes_pass(node: HTMLDisplayNode) -> HTMLDisplayNode:
    """
    Clean and deduplicate data in display nodes.

    This pass:
    1. Trims whitespace from all data values
    2. Removes empty values after trimming
    3. Deduplicates values, keeping first occurrence

    Args:
        node: HTMLDisplayNode tree

    Returns:
        Tree with cleaned data
    """
    def trim_data(raw_data: list) -> list:
        """Trim all values in the data list."""
        trimmed_data = []
        for key, value in raw_data:
            trimmed_value = value.strip()
            if trimmed_value:  # Only keep non-empty after trim
                trimmed_data.append((key, trimmed_value))
        return trimmed_data

    def deduplicate_data(trimmed_data: list, tag_value: str = None, text_value: str = None) -> list:
        """Remove duplicate values, keeping first occurrence. Also considers tag and text values."""
        seen_values = set()
        final_data = []

        # Add tag and text values to seen set if they exist
        if tag_value:
            seen_values.add(tag_value)
        if text_value:
            seen_values.add(text_value)

        for key, value in trimmed_data:
            if value not in seen_values:
                final_data.append((key, value))
                seen_values.add(value)

        return final_data

    # Process children first (bottom-up)
    cleaned_children = []
    for child in node.children:
        cleaned_child = normalize_attributes_pass(child)
        cleaned_children.append(cleaned_child)

    # Create new node without children
    cleaned = node.copy(include_children=False)

    # Clean this node's text
    if cleaned.text:
        cleaned.text = cleaned.text.strip()
        if not cleaned.text:  # If empty after trim, set to None
            cleaned.text = None

    # Clean this node's attributes: trim → deduplicate (considering tag and text values)
    trimmed_attributes = trim_data(cleaned.attributes)
    final_attributes = deduplicate_data(trimmed_attributes, cleaned.tag, cleaned.text)
    cleaned.attributes = final_attributes

    # Add cleaned children
    for child in cleaned_children:
        cleaned.add_child(child)

    return cleaned