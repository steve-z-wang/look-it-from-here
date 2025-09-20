from typing import List, Optional, Dict, Any, Union
import uuid
from dataclasses import dataclass


type SemanticNode = Union['SemanticElementNode', 'SemanticTextNode']

@dataclass
class SemanticTextNode:
    """Represents a text node in the DOM tree."""
    content: str

class SemanticElementNode:
    def __init__(
        self,
        tag: str,
        attributes: Optional[List[tuple]] = None,
        children: Optional[List[SemanticNode]] = None
    ):
        self.id = str(uuid.uuid4())
        self.tag = tag
        self.attributes = attributes or []  # HTML attributes (aria-label, role, type, etc.)
        self.children: List[SemanticNode] = children or []
        self.parent: Optional['SemanticElementNode'] = None

        for child in self.children:
            if isinstance(child, SemanticElementNode):
                child.parent = self

    def add_child(self, child: SemanticNode) -> None:
        self.children.append(child)
        if isinstance(child, SemanticElementNode):
            child.parent = self

    def get_element_children(self) -> List['SemanticElementNode']:
        """Get only element children (SemanticNode instances)."""
        return [child for child in self.children if isinstance(child, SemanticElementNode)]

    def get_text_children(self) -> List[SemanticTextNode]:
        """Get only text node children (SemanticTextNode instances)."""
        return [child for child in self.children if isinstance(child, SemanticTextNode)]

    def has_semantic_value(self) -> bool:
        """Check if this node has semantic value (non-whitespace text or attributes)."""
        # Check for text in TextNode children
        has_text = any(
            isinstance(child, SemanticTextNode) and child.content.strip()
            for child in self.children
        )
        has_attributes = bool(self.attributes)
        return has_text or has_attributes

    def copy(self, include_children: bool = True) -> 'SemanticElementNode':
        """
        Create a copy of this display node.

        Args:
            include_children: Whether to copy children nodes as well

        Returns:
            A new HTMLDisplayNode with the same data
        """
        new_node = SemanticElementNode(
            tag=self.tag,
            attributes=self.attributes.copy()
        )
        new_node.id = self.id  # Preserve the ID

        if include_children:
            for child in self.children:
                if isinstance(child, SemanticElementNode):
                    child_copy = child.copy(include_children=True)
                    new_node.add_child(child_copy)
                elif isinstance(child, SemanticTextNode):
                    new_node.add_child(SemanticTextNode(child.content))

        return new_node

    def __repr__(self) -> str:
        children_count = f' children={len(self.children)}' if self.children else ''
        return f'<SemanticNode tag="{self.tag}"{children_count}>'