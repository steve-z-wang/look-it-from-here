from typing import Optional, Tuple, Dict
from ...dom_node import DOMElementNode, DOMTextNode
from ...semantic_node import SemanticElementNode, SemanticTextNode
from ...constants import SEMANTIC_ATTRIBUTES, NON_SEMANTIC_ROLES


def convert_to_semantic_nodes_pass(node: DOMElementNode) -> Tuple[Optional[SemanticElementNode], Dict[str, str]]:
    """
    Convert DOMElementNode tree to SemanticElementNode tree.
    Also creates a mapping from DOMElementNode IDs to SemanticElementNode IDs.

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

    def filter_attributes(tree_node: DOMElementNode) -> list:
        """Filter attributes to only include standardized semantic attributes."""
        # Use semantic attributes from constants
        semantic_attributes = SEMANTIC_ATTRIBUTES

        # Filter attributes: only keep semantic ones
        filtered_attributes = []
        for key, value in tree_node.attributes.items():
            # Keep attribute if it's in the semantic set and has a value
            if key in semantic_attributes and value and value.strip():
                filtered_attributes.append((key, value))

        return filtered_attributes


    def render_node_recursive(tree_node: DOMElementNode) -> Optional[SemanticElementNode]:
        # Skip elements with non-semantic roles (explicitly non-semantic)
        role = tree_node.attributes.get('role', '').lower()
        if role in NON_SEMANTIC_ROLES:
            return None

        # Filter attributes based on semantic relevance
        filtered_attributes = filter_attributes(tree_node)

        # Create display node with tag and filtered attributes
        display_node = SemanticElementNode(tag=tree_node.tag, attributes=filtered_attributes)

        # Store the mapping
        tree_to_display_mapping[tree_node.id] = display_node.id

        # Process mixed children
        for child in tree_node.children:
            if isinstance(child, DOMTextNode):
                # Convert text node
                display_node.add_child(SemanticTextNode(text=child.text))
            elif isinstance(child, DOMElementNode):
                # Convert element node recursively
                child_display = render_node_recursive(child)
                if child_display:
                    display_node.add_child(child_display)

        return display_node

    rendered_tree = render_node_recursive(node)
    return rendered_tree, tree_to_display_mapping