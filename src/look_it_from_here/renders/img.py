from html_tree_node import HTMLTreeNode
from renders.base import register, DefaultRenderer
from renders.roles import IMG


@register("img")
class ImageRenderer(DefaultRenderer):
    """Renderer for image elements."""

    def get_role(self, node: HTMLTreeNode) -> str:
        """Image role with explicit role taking priority."""
        explicit_role = node.attributes.get('role')
        return explicit_role if explicit_role else IMG

    def get_text(self, node: HTMLTreeNode) -> str:
        """Get alt text for images."""
        return node.attributes.get('alt', '')