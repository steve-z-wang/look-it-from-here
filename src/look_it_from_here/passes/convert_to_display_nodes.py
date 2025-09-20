from typing import Optional, Tuple, Dict
from ..html_tree_node import HTMLTreeNode
from ..html_display_node import HTMLDisplayNode


def convert_to_display_nodes_pass(node: HTMLTreeNode) -> Tuple[Optional[HTMLDisplayNode], Dict[str, str]]:
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

    def filter_attributes(tree_node: HTMLTreeNode) -> list:
        """Filter attributes based on semantic relevance for the element type."""
        # Define semantic attributes by element type
        semantic_attributes = {
            # Form elements
            'input': {'type', 'value', 'placeholder', 'name', 'aria-label', 'role', 'disabled', 'checked'},
            'button': {'type', 'value', 'name', 'aria-label', 'role', 'disabled'},
            'textarea': {'name', 'placeholder', 'aria-label', 'role', 'disabled', 'maxlength'},
            'select': {'name', 'aria-label', 'role', 'disabled', 'multiple'},
            'form': {'action', 'method', 'name', 'role'},

            # Navigation elements
            'a': {'aria-label', 'role'},
            'nav': {'role', 'aria-label'},

            # Media elements
            'img': {'alt', 'title'},
            'video': {'controls', 'autoplay', 'muted'},
            'audio': {'controls', 'autoplay', 'muted'},

            # Semantic elements
            'header': {'role'},
            'main': {'role'},
            'section': {'role', 'aria-label'},
            'article': {'role'},
            'aside': {'role'},
            'footer': {'role'},

            # Interactive elements
            'details': {'open'},
            'summary': {'role'},
            'dialog': {'open', 'aria-label', 'role'},

            # Table elements
            'table': {'role', 'aria-label'},
            'th': {'scope', 'role'},
            'td': {'role'},

            # List elements
            'ul': {'role'},
            'ol': {'role'},
            'li': {'role', 'value'},
        }

        # Universal semantic attributes (meaningful for all elements)
        universal_attributes = {'aria-label', 'aria-describedby', 'title'}

        # Get relevant attributes for this element type
        tag = tree_node.tag.lower()
        relevant_attrs = semantic_attributes.get(tag, set()) | universal_attributes

        # Filter attributes to only semantic ones
        filtered_attributes = []
        for key, value in tree_node.attributes.items():
            if key in relevant_attrs and value and value.strip():
                filtered_attributes.append((key, value))

        return filtered_attributes


    def render_node_recursive(tree_node: HTMLTreeNode) -> Optional[HTMLDisplayNode]:
        # Get text directly from tree node
        text = tree_node.text if tree_node.text else None

        # Filter attributes based on semantic relevance
        filtered_attributes = filter_attributes(tree_node)

        # Create display node with tag, text, and filtered attributes
        display_node = HTMLDisplayNode(tag=tree_node.tag, text=text, attributes=filtered_attributes)

        # Store the mapping
        tree_to_display_mapping[tree_node.id] = display_node.id

        # Process children recursively
        for child in tree_node.children:
            child_display = render_node_recursive(child)
            if child_display:
                display_node.add_child(child_display)

        return display_node

    rendered_tree = render_node_recursive(node)
    return rendered_tree, tree_to_display_mapping