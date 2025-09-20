import asyncio
from typing import Dict, Tuple
from ..dom_node import DOMElementNode, DOMTextNode
from ..interfaces import WebPage, WebElement


async def extract_dom_structure(page: WebPage) -> Tuple[DOMElementNode, Dict[str, WebElement]]:
    """
    Build DOM tree using DFS with parallelization at each level.
    Returns tuple of (tree_root, id_to_element_mapping)
    """
    id_to_element = {}

    root_element = await page.get_root()
    if not root_element:
        raise ValueError("Could not get root element")

    async def build_node(element: WebElement) -> DOMElementNode:
        # Gather all element data in parallel
        tag_task = element.get_tag()
        children_task = element.get_children()
        is_visible_task = element.is_visible()

        # Get ALL attributes from the element
        attributes_task = element.get_attributes()

        # Wait for all data
        tag, children, is_visible, attributes = await asyncio.gather(
            tag_task, children_task, is_visible_task, attributes_task
        )

        # Create tree node
        tree_node = DOMElementNode(
            tag=tag or "unknown",
            attributes=attributes,
            is_visible=is_visible
        )

        # Store mapping
        id_to_element[tree_node.id] = element

        # Process mixed children (WebElements and text strings)
        if children:
            for child in children:
                if isinstance(child, str):
                    # It's a text node
                    tree_node.add_child(DOMTextNode(child))
                else:
                    # It's an element node - process recursively
                    child_node = await build_node(child)
                    tree_node.add_child(child_node)

        return tree_node

    root_tree_node = await build_node(root_element)
    return root_tree_node, id_to_element