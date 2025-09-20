from typing import Dict, List, Optional, Any
import uuid


class HTMLTreeNode:
    def __init__(
        self,
        tag: str,
        text: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
        children: Optional[List['HTMLTreeNode']] = None,
        is_visible: bool = True
    ):
        self.id = str(uuid.uuid4())
        self.tag = tag
        self.text = text or ""
        self.attributes = attributes or {}
        self.children = children or []
        self.is_visible = is_visible
        self.parent: Optional['HTMLTreeNode'] = None

        for child in self.children:
            child.parent = self

    def add_child(self, child: 'HTMLTreeNode') -> None:
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: 'HTMLTreeNode') -> None:
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def get_attribute(self, name: str, default: Any = None) -> Any:
        return self.attributes.get(name, default)

    def set_attribute(self, name: str, value: str) -> None:
        self.attributes[name] = value

    def has_attribute(self, name: str) -> bool:
        return name in self.attributes

    def get_siblings(self) -> List['HTMLTreeNode']:
        if self.parent is None:
            return []
        return [child for child in self.parent.children if child != self]

    def get_parent_chain(self, max_depth: Optional[int] = None) -> List['HTMLTreeNode']:
        chain = []
        current = self.parent
        depth = 0

        while current and (max_depth is None or depth < max_depth):
            chain.append(current)
            current = current.parent
            depth += 1

        return chain

    def find_children_by_tag(self, tag: str) -> List['HTMLTreeNode']:
        return [child for child in self.children if child.tag == tag]

    def find_children_by_attribute(self, attr_name: str, attr_value: str = None) -> List['HTMLTreeNode']:
        if attr_value is None:
            return [child for child in self.children if child.has_attribute(attr_name)]
        return [child for child in self.children if child.get_attribute(attr_name) == attr_value]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'tag': self.tag,
            'text': self.text,
            'attributes': self.attributes,
            'is_visible': self.is_visible,
            'children': [child.to_dict() for child in self.children]
        }

    def copy(self, include_children: bool = True) -> 'HTMLTreeNode':
        new_node = HTMLTreeNode(
            tag=self.tag,
            text=self.text,
            attributes=self.attributes.copy(),
            is_visible=self.is_visible
        )
        new_node.id = self.id

        if include_children:
            for child in self.children:
                child_copy = child.copy(include_children=True)
                new_node.add_child(child_copy)

        return new_node

    def __repr__(self) -> str:
        attrs_str = ' '.join(f'{k}="{v}"' for k, v in self.attributes.items())
        attrs_part = f' {attrs_str}' if attrs_str else ''
        text_part = f' text="{self.text}"' if self.text.strip() else ''
        children_count = f' children={len(self.children)}' if self.children else ''

        return f'<HTMLTreeNode tag="{self.tag}"{attrs_part}{text_part}{children_count}>'