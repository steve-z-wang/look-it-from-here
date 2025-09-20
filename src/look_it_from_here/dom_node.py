from typing import Dict, List, Optional, Any, Union
import uuid
from dataclasses import dataclass

type DOMNode = Union['DOMElementNode', 'DOMTextNode'] 

@dataclass
class DOMTextNode:
    """Represents a text node in the DOM tree."""
    content: str


class DOMElementNode:
    def __init__(
        self,
        tag: str,
        attributes: Optional[Dict[str, str]] = None,
        children: Optional[List[DOMNode]] = None,
        is_visible: bool = True
    ):
        self.id = str(uuid.uuid4())
        self.tag = tag
        self.attributes = attributes or {}
        self.children: List[DOMNode] = children or []
        self.is_visible = is_visible
        self.parent: Optional['DOMElementNode'] = None

        for child in self.children:
            if isinstance(child, DOMElementNode):
                child.parent = self

    def add_child(self, child: DOMNode) -> None:
        self.children.append(child)
        if isinstance(child, DOMElementNode):
            child.parent = self

    def get_element_children(self) -> List['DOMElementNode']:
        """Get only element children (DOMNode instances)."""
        return [child for child in self.children if isinstance(child, DOMElementNode)]

    def get_text_children(self) -> List[DOMTextNode]:
        """Get only text node children (DOMTextNode instances)."""
        return [child for child in self.children if isinstance(child, DOMTextNode)]

    def to_dict(self) -> Dict[str, Any]:
        children_data = []
        for child in self.children:
            if isinstance(child, DOMElementNode):
                children_data.append(child.to_dict())
            elif isinstance(child, DOMTextNode):
                children_data.append({'type': 'text', 'content': child.content})

        return {
            'id': self.id,
            'tag': self.tag,
            'attributes': self.attributes,
            'is_visible': self.is_visible,
            'children': children_data
        }

    def copy(self, include_children: bool = True) -> 'DOMElementNode':
        new_node = DOMElementNode(
            tag=self.tag,
            attributes=self.attributes.copy(),
            is_visible=self.is_visible
        )
        new_node.id = self.id

        if include_children:
            for child in self.children:
                if isinstance(child, DOMElementNode):
                    child_copy = child.copy(include_children=True)
                    new_node.add_child(child_copy)
                elif isinstance(child, DOMTextNode):
                    new_node.add_child(DOMTextNode(child.content))

        return new_node

    def __repr__(self) -> str:
        attrs_str = ' '.join(f'{k}="{v}"' for k, v in self.attributes.items())
        attrs_part = f' {attrs_str}' if attrs_str else ''
        children_count = f' children={len(self.children)}' if self.children else ''

        return f'<DOMNode tag="{self.tag}"{attrs_part}{children_count}>'