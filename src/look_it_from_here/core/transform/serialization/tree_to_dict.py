from typing import Dict, Any, List, Union
from ...semantic_node import SemanticElementNode, SemanticTextNode


def semantic_tree_to_dict(node: SemanticElementNode) -> Dict[str, Any]:
    """
    Convert a semantic tree to a simple dictionary representation.

    Args:
        node: SemanticElementNode to convert (must be non-None)

    Returns:
        Dictionary with tag and semantic data
    """

    # Start with tag
    result = {"tag": node.tag}

    # Add attributes
    for key, value in node.attributes:
        result[key] = value

    # Build children list
    children: List[Union[Dict[str, Any], str]] = []
    for child in node.content:
        if isinstance(child, SemanticElementNode):
            child_dict = semantic_tree_to_dict(child)
            children.append(child_dict)
        elif isinstance(child, SemanticTextNode):
            children.append(child.text)

    # Only include content field if there are any children
    if children:
        result["content"] = children

    return result