# Look It from Here: Reverse Tree Embeddings for Web Automation

from .core.transform import create_html_tree, create_semantic_tree
from .adapter.playwright_implementation import PlaywrightPage, PlaywrightElement
from .core.snapshot import WebSnapshot
from .core.interfaces import WebPage, WebElement, Snapshot

__all__ = [
    'create_html_tree',
    'create_semantic_tree',
    'PlaywrightPage',
    'PlaywrightElement',
    'WebSnapshot',
    'WebPage',
    'WebElement',
    'Snapshot'
]