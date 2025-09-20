from typing import List, Optional, Dict, Any
import uuid


class HTMLDisplayNode:
    def __init__(
        self,
        tag: str,
        text: Optional[str] = None,
        attributes: Optional[List[tuple]] = None,
        children: Optional[List['HTMLDisplayNode']] = None
    ):
        self.id = str(uuid.uuid4())
        self.tag = tag
        self.text = text  # Keep text separate from other attributes
        self.attributes = attributes or []  # HTML attributes (aria-label, role, type, etc.)
        self.children = children or []
        self.parent: Optional['HTMLDisplayNode'] = None

        for child in self.children:
            child.parent = self

    def add_child(self, child: 'HTMLDisplayNode') -> None:
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: 'HTMLDisplayNode') -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def with_text(self, text: str) -> 'HTMLDisplayNode':
        self.display_text = text
        return self

    def with_child(self, child: 'HTMLDisplayNode') -> 'HTMLDisplayNode':
        self.add_child(child)
        return self

    def has_semantic_value(self) -> bool:
        """Check if this node has semantic value (non-whitespace text or attributes)."""
        has_text = bool(self.text and self.text.strip())
        has_attributes = bool(self.attributes)
        return has_text or has_attributes

    def copy(self, include_children: bool = True) -> 'HTMLDisplayNode':
        """
        Create a copy of this display node.

        Args:
            include_children: Whether to copy children nodes as well

        Returns:
            A new HTMLDisplayNode with the same data
        """
        new_node = HTMLDisplayNode(
            tag=self.tag,
            text=self.text,
            attributes=self.attributes.copy()
        )
        new_node.id = self.id  # Preserve the ID

        if include_children:
            for child in self.children:
                child_copy = child.copy(include_children=True)
                new_node.add_child(child_copy)

        return new_node

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'role': self.role,
            'display_text': self.display_text,
            'children': [child.to_dict() for child in self.children]
        }

    def __repr__(self) -> str:
        text_part = f' text="{self.display_text[:20]}..."' if len(self.display_text) > 20 else f' text="{self.display_text}"' if self.display_text else ''
        children_count = f' children={len(self.children)}' if self.children else ''
        return f'<HTMLDisplayNode role="{self.role}"{text_part}{children_count}>'