from .dom_extraction import create_html_tree
from .semantic_conversion import create_semantic_tree
from .serialization import semantic_tree_to_dict

__all__ = [
    'create_html_tree',
    'create_semantic_tree',
    'semantic_tree_to_dict'
]