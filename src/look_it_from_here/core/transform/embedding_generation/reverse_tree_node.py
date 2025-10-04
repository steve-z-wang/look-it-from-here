from typing import List, Optional, Union
from dataclasses import dataclass
import json


type ReverseTreeNode = Union['ReverseTreeElementNode', 'ReverseTreeTextNode', 'ReverseTreeMarkerNode']


@dataclass
class ReverseTreeTextNode:
    """Represents text content in a reverse tree."""
    text: str


@dataclass
class ReverseTreeMarkerNode:
    """Represents position markers in reverse tree (_FOCUS_ELEMENT_, _FOCUS_PATH_)."""
    marker: str  # "_FOCUS_ELEMENT_" or "_FOCUS_PATH_"


class ReverseTreeElementNode:
    """Element node in reverse tree structure with parent chain instead of children."""

    def __init__(
        self,
        tag: str,
        attributes: Optional[List[tuple]] = None,
        content: Optional[List[ReverseTreeNode]] = None,
        parent: Optional['ReverseTreeElementNode'] = None
    ):
        self.tag = tag
        self.attributes = attributes or []
        self.content: List[ReverseTreeNode] = content or []
        self.parent = parent  # Parent chain for reverse tree structure

    def add_content(self, item: ReverseTreeNode) -> None:
        """Add content item (text, marker, or sibling element)."""
        self.content.append(item)

    def to_dict(self) -> dict:
        """Convert reverse tree to dictionary for serialization."""
        result = {"tag": self.tag}

        # Add attributes
        for key, value in self.attributes:
            result[key] = value

        # Add content
        if self.content:
            content_list = []
            for item in self.content:
                if isinstance(item, ReverseTreeTextNode):
                    content_list.append(item.text)
                elif isinstance(item, ReverseTreeMarkerNode):
                    content_list.append(item.marker)
                elif isinstance(item, ReverseTreeElementNode):
                    content_list.append(item.to_dict())
            result["content"] = content_list

        # Add parent chain
        if self.parent:
            result["parent"] = self.parent.to_dict()

        return result

    def to_text(self) -> str:
        """Convert reverse tree to prompt-enhanced text for embedding generation."""

        prompt = """This is a web element represented as a reverse tree structure for natural language web automation. The reverse tree places the target element at the root while preserving its hierarchical context through a parent chain.

Structure explanation:
- Root element: The target web element that can be interacted with
- "content": Direct children and text content of the target element
- "parent": Hierarchical chain showing containers and context
- "_FOCUS_ELEMENT_": Marker showing where the target element (or its ancestor) sits among siblings at each level of the parent chain

Use this structure to match natural language queries like:
- "click the submit button"
- "fill the email field in the login form"
- "find the search button in the header"
- "click the add to cart button for wireless headphones"

The _FOCUS_ELEMENT_ markers trace the path from target to root, showing spatial relationships and context at each level.

Match based on element semantics, text content, hierarchy, and spatial relationships.

Element description:
"""

        reverse_tree_json = json.dumps(self.to_dict(), indent=2)

        return prompt + reverse_tree_json