from html_tree_node import HTMLTreeNode
from renders.base import register, DefaultRenderer
from renders.utils import extract_text_from_node
from renders.roles import LINK


@register("a")
class AnchorRenderer(DefaultRenderer):
    """Renderer for anchor/link elements with smart context."""

    def get_role(self, node: HTMLTreeNode) -> str:
        """Link role with explicit role taking priority."""
        explicit_role = node.attributes.get('role')
        return explicit_role if explicit_role else LINK

    def get_text(self, node: HTMLTreeNode) -> str:
        """Get link text with context hints when appropriate."""
        # Get text from content, children, or aria-label
        text = extract_text_from_node(node)
        href = node.attributes.get('href', '')

        # Add context hints for special link types
        return self._format_link_text(text, href)

    def should_render_children(self) -> bool:
        """
        Don't render children as separate nodes.
        Text has already been extracted from children in render_node.
        """
        return False

    def _format_link_text(self, text: str, href: str) -> str:
        """
        Format link text with context hints when appropriate.

        Args:
            text: The link's display text
            href: The href attribute value

        Returns:
            Formatted text with context hints if needed
        """
        if not href:
            return text or "Link"

        # Email links
        if href.startswith('mailto:'):
            email = href[7:]  # Remove 'mailto:' prefix
            return f"{text} (email)" if text else email

        # Phone links
        if href.startswith('tel:'):
            phone = href[4:]  # Remove 'tel:' prefix
            return f"{text} (phone)" if text else phone

        # File downloads - check common extensions
        href_lower = href.lower()
        file_hints = {
            '.pdf': 'PDF',
            '.doc': 'DOC',
            '.docx': 'DOC',
            '.xls': 'Excel',
            '.xlsx': 'Excel',
            '.zip': 'ZIP',
            '.csv': 'CSV',
            '.txt': 'TXT',
            '.mp4': 'Video',
            '.mp3': 'Audio',
            '.png': 'Image',
            '.jpg': 'Image',
            '.jpeg': 'Image',
        }

        for ext, hint in file_hints.items():
            if href_lower.endswith(ext):
                return f"{text} ({hint})" if text else f"Download ({hint})"

        # Regular links and in-page anchors - no extra context needed
        return text or "Link"