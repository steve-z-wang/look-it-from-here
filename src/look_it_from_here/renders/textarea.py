from html_tree_node import HTMLTreeNode
from renders.base import register, DefaultRenderer
from renders.roles import TEXTAREA


@register("textarea")
class TextareaRenderer(DefaultRenderer):
    """Renderer for textarea elements."""

    def get_role(self, node: HTMLTreeNode) -> str:
        """Textarea role with explicit role taking priority."""
        explicit_role = node.attributes.get('role')
        return explicit_role if explicit_role else TEXTAREA

    def get_text(self, node: HTMLTreeNode) -> str:
        """Get text with priority: content > placeholder > aria-label."""
        text = node.text if node.text else ""
        if not text.strip():
            placeholder = node.attributes.get('placeholder', '')
            if placeholder:
                return placeholder
            # Fallback to aria-label for accessibility
            return node.attributes.get('aria-label', '')
        return text