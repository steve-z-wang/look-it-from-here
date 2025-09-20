from html_tree_node import HTMLTreeNode
from renders.base import register, DefaultRenderer
from renders.roles import BUTTON, CHECKBOX, RADIO, TEXTBOX


@register("input")
class InputRenderer(DefaultRenderer):
    """Renderer for input elements."""

    def get_role(self, node: HTMLTreeNode) -> str:
        """Determine role based on input type, with explicit role taking priority."""
        # Check for explicit role attribute first
        explicit_role = node.attributes.get('role')
        if explicit_role:
            return explicit_role

        # Infer role from input type
        input_type = node.attributes.get('type', 'text').lower()
        if input_type in ('submit', 'button', 'reset'):
            return BUTTON
        elif input_type == 'checkbox':
            return CHECKBOX
        elif input_type == 'radio':
            return RADIO
        elif input_type == 'file':
            return BUTTON  # File inputs act like buttons
        else:
            # text, email, password, search, url, tel, etc.
            return TEXTBOX

    def get_text(self, node: HTMLTreeNode) -> str:
        """Get text with priority: value > placeholder > aria-label."""
        value = node.attributes.get('value', '')
        if value:
            return value

        placeholder = node.attributes.get('placeholder', '')
        if placeholder:
            return placeholder

        return node.attributes.get('aria-label', '')