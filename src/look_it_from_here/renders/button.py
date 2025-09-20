from html_tree_node import HTMLTreeNode
from renders.base import register, DefaultRenderer
from renders.utils import extract_text_from_node
from renders.roles import BUTTON


@register("button")
class ButtonRenderer(DefaultRenderer):
    """Renderer for button elements."""

    def get_role(self, node: HTMLTreeNode) -> str:
        """Button role with explicit role taking priority."""
        explicit_role = node.attributes.get('role')
        return explicit_role if explicit_role else BUTTON

    def get_text(self, node: HTMLTreeNode) -> str:
        """Extract text from button and its children."""
        return extract_text_from_node(node) or ""

    def should_render_children(self) -> bool:
        """
        Don't render children as separate nodes.
        Text has already been extracted from children in render_node.
        """
        return False