from typing import Dict
from html_tree_node import HTMLTreeNode
from html_display_node import HTMLDisplayNode


class DefaultRenderer:
    """Default renderer for generic elements."""

    def render_node(self, node: HTMLTreeNode) -> HTMLDisplayNode:
        """Template method that constructs HTMLDisplayNode using overridable methods."""
        # Get role and text using overridable methods
        role = self.get_role(node)
        text = self.get_text(node)

        # Create display node
        return HTMLDisplayNode(role=role, display_text=text)

    def get_role(self, node: HTMLTreeNode) -> str:
        """Get the semantic role for this node. Override in subclasses."""
        # Check for explicit role attribute first
        explicit_role = node.attributes.get('role')
        if explicit_role:
            return explicit_role

        # Fallback to tag name
        return node.tag

    def get_text(self, node: HTMLTreeNode) -> str:
        """Get the display text for this node. Override in subclasses."""
        # Use text content if available, otherwise fallback to aria-label
        return node.text or node.attributes.get('aria-label', '')

    def should_render_children(self) -> bool:
        """Default behavior is to render all children."""
        return True


# Registry for tag-specific renderers
RENDERERS: Dict[str, DefaultRenderer] = {}


def register(tag: str):
    """Decorator to register a renderer for a specific tag."""
    def decorator(cls):
        RENDERERS[tag] = cls()
        return cls
    return decorator