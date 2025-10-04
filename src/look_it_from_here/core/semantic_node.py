from typing import List, Optional, Dict, Any, Union
import uuid
from dataclasses import dataclass


type SemanticNode = Union['SemanticElementNode', 'SemanticTextNode']

@dataclass
class SemanticTextNode:
    """Represents a text node in the DOM tree."""
    text: str
    

class SemanticElementNode:
    def __init__(
        self,
        tag: str,
        attributes: Optional[List[tuple]] = None,
        content: Optional[List[SemanticNode]] = None
    ):
        self.id = str(uuid.uuid4())
        self.tag = tag
        self.attributes = attributes or []  # HTML attributes (aria-label, role, type, etc.)
        self.content: List[SemanticNode] = content or []

    def add_child(self, child: SemanticNode) -> None:
        self.content.append(child)

    def get_element_children(self) -> List['SemanticElementNode']:
        """Get only element children (SemanticNode instances)."""
        return [child for child in self.content if isinstance(child, SemanticElementNode)]

    def get_text_children(self) -> List[SemanticTextNode]:
        """Get only text node children (SemanticTextNode instances)."""
        return [child for child in self.content if isinstance(child, SemanticTextNode)]


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
            for child in self.content:
                if isinstance(child, SemanticElementNode):
                    child_copy = child.copy(include_children=True)
                    new_node.add_child(child_copy)
                elif isinstance(child, SemanticTextNode):
                    new_node.add_child(SemanticTextNode(text=child.text))

        return new_node

    def __repr__(self) -> str:
        content_count = f' content={len(self.content)}' if self.content else ''
        return f'<SemanticNode tag="{self.tag}"{content_count}>'