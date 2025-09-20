import asyncio
from typing import Dict, Tuple
from html_tree_node import HTMLTreeNode
from interfaces import WebPage, WebElement


async def build_dom_tree(page: WebPage) -> Tuple[HTMLTreeNode, Dict[str, WebElement]]:
    """
    Build DOM tree using DFS with parallelization at each level.
    Returns tuple of (tree_root, id_to_element_mapping)
    """
    id_to_element = {}

    root_element = await page.get_root()
    if not root_element:
        raise ValueError("Could not get root element")

    async def build_node(element: WebElement) -> HTMLTreeNode:
        # Gather all element data in parallel
        tag_task = element.get_tag()
        text_task = element.get_text()
        children_task = element.get_children()
        is_visible_task = element.is_visible()

        # Get common attributes in parallel
        id_attr_task = element.get_attribute("id")
        class_attr_task = element.get_attribute("class")
        name_attr_task = element.get_attribute("name")
        type_attr_task = element.get_attribute("type")

        # Wait for all data
        tag, text, children, is_visible, id_attr, class_attr, name_attr, type_attr = await asyncio.gather(
            tag_task, text_task, children_task, is_visible_task,
            id_attr_task, class_attr_task, name_attr_task, type_attr_task
        )

        # Build attributes dict
        attributes = {}
        if id_attr:
            attributes["id"] = id_attr
        if class_attr:
            attributes["class"] = class_attr
        if name_attr:
            attributes["name"] = name_attr
        if type_attr:
            attributes["type"] = type_attr

        # Create tree node
        tree_node = HTMLTreeNode(
            tag=tag or "unknown",
            text=text or "",
            attributes=attributes,
            is_visible=is_visible
        )

        # Store mapping
        id_to_element[tree_node.id] = element

        # Process children in parallel if any exist
        if children:
            child_nodes = await asyncio.gather(*[build_node(child) for child in children])
            for child_node in child_nodes:
                tree_node.add_child(child_node)

        return tree_node

    root_tree_node = await build_node(root_element)
    return root_tree_node, id_to_element