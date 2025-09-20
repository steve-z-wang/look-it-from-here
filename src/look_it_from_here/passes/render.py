from typing import Optional, Tuple, Dict
from html_tree_node import HTMLTreeNode
from html_display_node import HTMLDisplayNode
from renders.base import RENDERERS, DefaultRenderer
import renders  # Import to register all renderers


def render_pass(node: HTMLTreeNode) -> Tuple[Optional[HTMLDisplayNode], Dict[str, str]]:
    """
    Convert HTMLTreeNode tree to HTMLDisplayNode tree using appropriate renderers.
    Also creates a mapping from HTMLTreeNode IDs to HTMLDisplayNode IDs.

    This pass handles:
    - Applying tag-specific renderers
    - Building the HTMLDisplayNode tree structure
    - Creating ID mapping between trees

    Args:
        node: HTMLTreeNode to render

    Returns:
        Tuple of (HTMLDisplayNode tree, mapping of tree_node_id -> display_node_id)
    """
    # Mapping from HTMLTreeNode ID to HTMLDisplayNode ID
    tree_to_display_mapping = {}

    def render_node_recursive(tree_node: HTMLTreeNode) -> Optional[HTMLDisplayNode]:
        # Get appropriate renderer for this node type
        renderer = RENDERERS.get(tree_node.tag, DefaultRenderer())

        # Render this node (without children)
        display_node = renderer.render_node(tree_node)

        # Store the mapping
        tree_to_display_mapping[tree_node.id] = display_node.id

        # Process children recursively only if the renderer wants them
        if renderer.should_render_children():
            for child in tree_node.children:
                child_display = render_node_recursive(child)
                if child_display:
                    display_node.with_child(child_display)

        return display_node

    rendered_tree = render_node_recursive(node)
    return rendered_tree, tree_to_display_mapping