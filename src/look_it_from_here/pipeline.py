from typing import Dict, Tuple, Optional, List, Any
from html_tree_node import HTMLTreeNode
from html_display_node import HTMLDisplayNode
from interfaces import WebPage, WebElement
from passes.build_dom_tree import build_dom_tree
from passes.filter_invisible import filter_invisible
from passes.render import render_pass
from passes.content_filter import content_filter_pass
from passes.collapse import collapse_pass


async def create_html_tree(page: WebPage) -> Tuple[Optional[HTMLTreeNode], Dict[str, WebElement]]:
    """
    Create an HTML tree representation from a web page.
    Builds the DOM tree and filters invisible elements.

    Args:
        page: WebPage instance to process

    Returns:
        Tuple of (
            Optional[HTMLTreeNode] root,
            Dict mapping tree node IDs to WebElements
        )
    """
    # Pass 1: Build the initial DOM tree from the page
    tree, tree_id_to_element = await build_dom_tree(page)

    # Pass 2: Filter out invisible elements from the tree
    filtered_tree = filter_invisible(tree)

    return filtered_tree, tree_id_to_element


def create_semantic_tree(html_tree: Optional[HTMLTreeNode]) -> Tuple[Optional[HTMLDisplayNode], Dict[str, str]]:
    """
    Create a semantic tree from an HTML tree.
    Applies rendering, content filtering, and collapsing passes.

    Args:
        html_tree: HTMLTreeNode root

    Returns:
        Tuple of (
            Optional[HTMLDisplayNode] root with semantic roles,
            Dict mapping tree node IDs to display node IDs
        )
    """
    if not html_tree:
        return None, {}

    # Pass 1: Render tree nodes to display nodes
    display_tree, tree_to_display_mapping = render_pass(html_tree)

    # Pass 2: Filter out nodes without meaningful content
    content_filtered_tree = content_filter_pass(display_tree)

    # Pass 3: Collapse single-child wrapper elements
    final_tree = collapse_pass(content_filtered_tree)

    return final_tree, tree_to_display_mapping


def display_tree_to_dict(node: Optional[HTMLDisplayNode]) -> Optional[Dict[str, Any]]:
    """
    Convert a display tree to a simple dictionary representation.

    Args:
        node: HTMLDisplayNode to convert

    Returns:
        Dictionary with role, text, and children fields
    """
    if not node:
        return None

    result = {
        "role": node.role,
        "text": node.display_text,
        "children": []
    }

    for child in node.children:
        child_dict = display_tree_to_dict(child)
        if child_dict:
            result["children"].append(child_dict)

    return result