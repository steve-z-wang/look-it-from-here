from typing import Dict, Tuple, Optional, List, Any, Union
from .dom_node import DOMElementNode
from .semantic_node import SemanticElementNode, SemanticTextNode
from .interfaces import WebPage, WebElement
from .passes.extract_dom_structure import extract_dom_structure
from .passes.propagate_visibility import propagate_visibility_pass
from .passes.filter_non_visual import filter_non_visual_pass
from .passes.filter_hidden_elements import filter_hidden_elements_pass
from .passes.convert_to_display_nodes import convert_to_display_nodes_pass
from .passes.convert_to_semantic_leafs import convert_to_semantic_leafs_pass
from .passes.flatten_text_only_elements import flatten_text_only_elements_pass
from .passes.remove_meaningless_elements import remove_meaningless_elements_pass
from .passes.normalize_attributes import normalize_attributes_pass


async def create_html_tree(page: WebPage) -> Tuple[Optional[DOMElementNode], Dict[str, WebElement]]:
    """
    Create an HTML tree representation from a web page.
    Builds the DOM tree, excludes unwanted tags, and filters invisible elements.

    Args:
        page: WebPage instance to process

    Returns:
        Tuple of (
            Optional[HTMLTreeNode] root,
            Dict mapping tree node IDs to WebElements
        )
    """
    # Pass 1: Extract the initial DOM structure from the page
    tree, tree_id_to_element = await extract_dom_structure(page)

    # Pass 2: Propagate visibility bottom-up (if child is visible, parent becomes visible)
    visibility_corrected_tree = propagate_visibility_pass(tree)

    # Pass 3: Remove non-visual tags (script, style, meta, etc.)
    filtered_tree = filter_non_visual_pass(visibility_corrected_tree)
    if not filtered_tree:
        return None, {}

    # Pass 4: Filter out hidden/invisible elements from the tree
    visible_tree = filter_hidden_elements_pass(filtered_tree)

    return visible_tree, tree_id_to_element


def create_semantic_tree(html_tree: DOMElementNode) -> Tuple[Optional[SemanticElementNode], Dict[str, str]]:
    """
    Create a semantic tree from an HTML tree.
    Applies rendering, content filtering, and collapsing passes.

    Args:
        html_tree: HTMLTreeNode root (must be non-None)

    Returns:
        Tuple of (
            Optional[HTMLDisplayNode] root with semantic roles,
            Dict mapping tree node IDs to display node IDs
        )
    """
    # Pass 1: Convert tree nodes to display nodes
    display_tree, tree_to_display_mapping = convert_to_display_nodes_pass(html_tree)

    if not display_tree:
        return None, {}

    # Pass 2: Flatten text-only elements into parents
    text_flattened_tree = flatten_text_only_elements_pass(display_tree)

    # Pass 3: Convert certain elements to semantic leafs
    semantic_leafs_tree = convert_to_semantic_leafs_pass(text_flattened_tree)

    # Pass 4: Normalize attributes (trim whitespace and deduplicate)
    normalized_tree = normalize_attributes_pass(semantic_leafs_tree)

    # Pass 5: Remove meaningless elements (empty elements + single-child wrappers)
    final_tree = remove_meaningless_elements_pass(normalized_tree)

    if not final_tree:
        return None, {}

    return final_tree, tree_to_display_mapping


def display_tree_to_dict(node: SemanticElementNode) -> Dict[str, Any]:
    """
    Convert a display tree to a simple dictionary representation.

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
    for child in node.children:
        if isinstance(child, SemanticElementNode):
            child_dict = display_tree_to_dict(child)
            children.append(child_dict)
        elif isinstance(child, SemanticTextNode):
            children.append(child.content)

    # Only include children field if there are any children
    if children:
        result["children"] = children

    return result