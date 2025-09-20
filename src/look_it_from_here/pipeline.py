from typing import Dict, Tuple, Optional, List, Any
from .html_tree_node import HTMLTreeNode
from .html_display_node import HTMLDisplayNode
from .interfaces import WebPage, WebElement
from .passes.extract_dom_structure import extract_dom_structure
from .passes.propagate_visibility import propagate_visibility_pass
from .passes.filter_non_visual import filter_non_visual_pass
from .passes.filter_hidden_elements import filter_hidden_elements_pass
from .passes.convert_to_display_nodes import convert_to_display_nodes_pass
from .passes.convert_to_semantic_leafs import convert_to_semantic_leafs_pass
from .passes.flatten_text_only_elements import flatten_text_only_elements_pass
from .passes.remove_single_child_wrappers import remove_single_child_wrappers_pass
from .passes.remove_empty_elements import remove_empty_elements_pass
from .passes.normalize_attributes import normalize_attributes_pass


async def create_html_tree(page: WebPage) -> Tuple[Optional[HTMLTreeNode], Dict[str, WebElement]]:
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


def create_semantic_tree(html_tree: HTMLTreeNode) -> Tuple[Optional[HTMLDisplayNode], Dict[str, str]]:
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

    # Pass 4: Remove empty elements (no text, no attributes, no children)
    empty_removed_tree = remove_empty_elements_pass(semantic_leafs_tree)

    if not empty_removed_tree:
        return None, {}

    # Pass 5: Remove single-child wrapper elements
    wrappers_removed_tree = remove_single_child_wrappers_pass(empty_removed_tree)

    # Pass 6: Normalize attributes (trim whitespace and deduplicate)
    final_tree = normalize_attributes_pass(wrappers_removed_tree)

    return final_tree, tree_to_display_mapping


def display_tree_to_dict(node: HTMLDisplayNode) -> Dict[str, Any]:
    """
    Convert a display tree to a simple dictionary representation.

    Args:
        node: HTMLDisplayNode to convert (must be non-None)

    Returns:
        Dictionary with tag and semantic data
    """
    # Start with tag
    result = {"tag": node.tag}

    # Add text if present
    if node.text:
        result["text"] = node.text

    # Add attributes
    for key, value in node.attributes:
        result[key] = value

    # Build children list
    children = []
    for child in node.children:
        child_dict = display_tree_to_dict(child)
        children.append(child_dict)

    # Only include children field if there are any children
    if children:
        result["children"] = children

    return result


def display_tree_to_xml(node: HTMLDisplayNode, indent: int = 0) -> str:
    """
    Convert a display tree to XML representation.

    Args:
        node: HTMLDisplayNode to convert (must be non-None)
        indent: Current indentation level

    Returns:
        XML string representation
    """
    indent_str = "  " * indent

    # Build opening tag with attributes
    attrs = ""
    for key, value in node.attributes:
        # Escape XML special characters in attribute values
        escaped_value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        attrs += f' {key}="{escaped_value}"'

    opening_tag = f"{indent_str}<{node.tag}{attrs}>"

    # Handle self-closing tags
    if not node.text and not node.children:
        return f"{indent_str}<{node.tag}{attrs}/>"

    # Build content
    content_parts = []

    # Add text if present
    if node.text:
        # Escape XML special characters in text content
        escaped_text = node.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        content_parts.append(escaped_text)

    # Add children
    if node.children:
        if node.text:
            # Mixed content - put children inline
            child_xml = []
            for child in node.children:
                child_xml.append(display_tree_to_xml(child, 0).strip())
            content_parts.extend(child_xml)
            return f"{opening_tag}{''.join(content_parts)}</{node.tag}>"
        else:
            # Children only - use proper indentation
            child_xml = []
            for child in node.children:
                child_xml.append(display_tree_to_xml(child, indent + 1))
            closing_tag = f"{indent_str}</{node.tag}>"
            return f"{opening_tag}\n" + "\n".join(child_xml) + f"\n{closing_tag}"

    # Text only
    return f"{opening_tag}{''.join(content_parts)}</{node.tag}>"