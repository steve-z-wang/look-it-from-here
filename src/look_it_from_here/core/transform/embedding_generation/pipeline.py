from typing import Dict, List, Optional, Tuple
from ...semantic_node import SemanticElementNode, SemanticTextNode
from ...embeddings import Embedder
from .reverse_tree_node import ReverseTreeElementNode, ReverseTreeTextNode, ReverseTreeMarkerNode


def convert_semantic_to_reverse_tree(semantic_node: SemanticElementNode) -> ReverseTreeElementNode:
    """
    Convert a complete semantic subtree to reverse tree format recursively.
    This preserves all elements in the subtree.
    """
    reverse_node = ReverseTreeElementNode(
        tag=semantic_node.tag,
        attributes=semantic_node.attributes.copy()
    )

    # Convert all content recursively
    for child in semantic_node.content:
        if isinstance(child, SemanticTextNode):
            reverse_node.add_content(ReverseTreeTextNode(child.text))
        elif isinstance(child, SemanticElementNode):
            child_reverse = convert_semantic_to_reverse_tree(child)
            reverse_node.add_content(child_reverse)

    return reverse_node


def create_parent_mapping(semantic_tree: SemanticElementNode) -> Dict[str, Optional[SemanticElementNode]]:
    """
    Create a mapping from node ID to parent node using DFS traversal.

    Args:
        semantic_tree: Root of the semantic tree

    Returns:
        Dictionary mapping node_id -> parent_node (None for root)
    """
    parent_map = {}

    def dfs(node: SemanticElementNode, parent: Optional[SemanticElementNode] = None):
        parent_map[node.id] = parent
        for child in node.content:
            if isinstance(child, SemanticElementNode):
                dfs(child, node)
            elif isinstance(child, SemanticTextNode):
                parent_map[child.id] = node

    dfs(semantic_tree)
    return parent_map


def generate_reverse_tree(target_node: SemanticElementNode, semantic_tree: SemanticElementNode) -> ReverseTreeElementNode:
    """
    Generate a reverse tree for a target element using temporary parent mapping.

    Args:
        target_node: The element to create reverse tree for
        semantic_tree: The full semantic tree to create parent mapping from

    Returns:
        ReverseTreeElementNode with target as root and parent chain
    """
    # Create temporary parent mapping with single DFS
    parent_map = create_parent_mapping(semantic_tree)

    def create_parent_chain(current_node: SemanticElementNode) -> Optional[ReverseTreeElementNode]:
        """Create parent chain using temporary mapping."""
        current_parent = parent_map.get(current_node.id)
        if not current_parent:
            return None

        # Create reverse tree node for parent
        reverse_parent = ReverseTreeElementNode(
            tag=current_parent.tag,
            attributes=current_parent.attributes.copy()
        )

        # Add siblings and target position marker
        for child in current_parent.content:
            if isinstance(child, SemanticElementNode):
                if child.id == current_node.id:
                    # Mark target element position
                    reverse_parent.add_content(ReverseTreeMarkerNode("_FOCUS_ELEMENT_"))
                else:
                    # Add complete sibling subtree recursively
                    sibling = convert_semantic_to_reverse_tree(child)
                    reverse_parent.add_content(sibling)
            elif isinstance(child, SemanticTextNode):
                reverse_parent.add_content(ReverseTreeTextNode(child.text))

        # Recursively create grandparent chain
        grandparent = parent_map.get(current_parent.id)
        if grandparent:
            reverse_parent.parent = create_parent_chain(current_parent)

        return reverse_parent

    # Create reverse tree with target as root
    reverse_tree = ReverseTreeElementNode(
        tag=target_node.tag,
        attributes=target_node.attributes.copy()
    )

    # Add target's complete content tree
    for child in target_node.content:
        if isinstance(child, SemanticTextNode):
            reverse_tree.add_content(ReverseTreeTextNode(child.text))
        elif isinstance(child, SemanticElementNode):
            # Convert complete child subtree
            child_reverse = convert_semantic_to_reverse_tree(child)
            reverse_tree.add_content(child_reverse)

    # Create parent chain using temporary mapping
    reverse_tree.parent = create_parent_chain(target_node)

    return reverse_tree


def create_embedding_from_text(text: str, embedder: Optional[Embedder] = None) -> List[float]:
    """
    Create embedding vector from text representation.

    Args:
        text: Text representation of reverse tree
        embedder: Embedder instance to use. If None, creates a new one.

    Returns:
        Embedding vector
    """
    if embedder is None:
        embedder = Embedder()

    return embedder.create_embedding(text)


def create_embeddings_from_semantic_tree(semantic_tree: SemanticElementNode, embedder: Optional[Embedder] = None) -> Tuple[Dict[str, List[float]], Dict[str, ReverseTreeElementNode]]:
    """
    Create embeddings for all elements in a semantic tree.

    Args:
        semantic_tree: Root of the semantic tree
        embedder: Embedder instance to use. If None, creates a new one.

    Returns:
        Tuple of (embeddings_dict, reverse_trees_dict) mapping semantic_node_id to embedding vector and reverse tree node
    """
    if embedder is None:
        embedder = Embedder()

    embeddings = {}
    reverse_trees = {}
    total_nodes = 0
    processed_nodes = 0

    # Count total nodes first
    def count_nodes(node: SemanticElementNode):
        nonlocal total_nodes
        total_nodes += 1
        for child in node.content:
            if isinstance(child, SemanticElementNode):
                count_nodes(child)

    count_nodes(semantic_tree)
    print(f"🔍 Processing {total_nodes} elements for embedding generation...")

    def traverse_and_embed(node: SemanticElementNode):
        """Recursively traverse tree and create embeddings."""
        nonlocal processed_nodes

        # Generate reverse tree for this node
        reverse_tree = generate_reverse_tree(node, semantic_tree)

        # Convert to text representation
        text_representation = reverse_tree.to_text()

        # Generate embedding
        embedding_vector = create_embedding_from_text(text_representation, embedder)

        # Store mappings
        embeddings[node.id] = embedding_vector
        reverse_trees[node.id] = reverse_tree

        processed_nodes += 1
        if processed_nodes % 5 == 0 or processed_nodes == total_nodes:
            print(f"✅ Generated {processed_nodes}/{total_nodes} embeddings")

        # Process children
        for child in node.content:
            if isinstance(child, SemanticElementNode):
                traverse_and_embed(child)

    # Start traversal from root
    traverse_and_embed(semantic_tree)

    print(f"🎉 Completed embedding generation for {total_nodes} elements")
    return embeddings, reverse_trees