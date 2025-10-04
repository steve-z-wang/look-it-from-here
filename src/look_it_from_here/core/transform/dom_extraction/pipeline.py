from typing import Dict, Tuple, Optional
from ...dom_node import DOMElementNode
from ...interfaces import WebPage, WebElement
from .extract_dom_structure import extract_dom_structure
from .filter_non_visual import filter_non_visual_pass
from .propagate_visibility import propagate_visibility_pass
from .filter_hidden_elements import filter_hidden_elements_pass


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

    # Pass 2: Remove non-visual tags (script, style, meta, etc.) first
    # This avoids wasting computation on elements we'll remove anyway
    filtered_tree = filter_non_visual_pass(tree)
    if not filtered_tree:
        return None, {}

    # Pass 3: Propagate visibility bottom-up (if child is visible, parent becomes visible)
    # Now we only propagate through meaningful elements
    visibility_corrected_tree = propagate_visibility_pass(filtered_tree)

    # Pass 4: Filter out hidden/invisible elements from the tree
    visible_tree = filter_hidden_elements_pass(visibility_corrected_tree)

    return visible_tree, tree_id_to_element