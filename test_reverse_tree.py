#!/usr/bin/env python3

import sys
import os
import json

# Add src to path so we can import our modules
current_dir = os.getcwd()
sys.path.insert(0, os.path.abspath(os.path.join(current_dir, 'src')))

from look_it_from_here.core.semantic_node import SemanticElementNode, SemanticTextNode
from look_it_from_here.core.transform.embedding_generation.pipeline import generate_reverse_tree, create_parent_mapping

def load_google_snapshot():
    """Load the Google.com snapshot from notebooks/output.json"""
    with open('notebooks/output.json', 'r') as f:
        data = json.load(f)
    return data

def dict_to_semantic_tree(data):
    """Convert dictionary representation back to SemanticElementNode tree"""

    def convert_node(node_data):
        if isinstance(node_data, str):
            return SemanticTextNode(text=node_data)

        # Extract tag and attributes
        tag = node_data['tag']
        attributes = []

        # Convert attributes back to list of tuples
        for key, value in node_data.items():
            if key not in ['tag', 'content']:
                attributes.append((key, value))

        # Convert content
        content = []
        if 'content' in node_data:
            for child_data in node_data['content']:
                content.append(convert_node(child_data))

        return SemanticElementNode(tag=tag, attributes=attributes, content=content)

    return convert_node(data)

def find_button_nodes(node, buttons=None):
    """Find all button nodes in the semantic tree"""
    if buttons is None:
        buttons = []

    if isinstance(node, SemanticElementNode):
        # Check if this is a button (tag="button" or role="button")
        if node.tag == 'button':
            buttons.append(node)
        else:
            # Check attributes for role="button"
            for key, value in node.attributes:
                if key == 'role' and value == 'button':
                    buttons.append(node)
                    break

        # Recursively check children
        for child in node.content:
            find_button_nodes(child, buttons)

    return buttons

def test_reverse_tree():
    """Test the reverse tree generation with Google.com data"""
    print("🔍 Loading Google.com semantic tree...")

    # Load and convert the semantic tree
    google_data = load_google_snapshot()
    semantic_tree = dict_to_semantic_tree(google_data)

    print(f"✅ Loaded semantic tree with tag: {semantic_tree.tag}")

    # Find button nodes
    print("\n🔍 Finding button elements...")
    buttons = find_button_nodes(semantic_tree)

    print(f"✅ Found {len(buttons)} button elements:")
    for i, button in enumerate(buttons):
        print(f"  {i+1}. Tag: {button.tag}, Attributes: {button.attributes}")
        if button.content:
            text_content = []
            for child in button.content:
                if isinstance(child, SemanticTextNode):
                    text_content.append(child.text)
            if text_content:
                print(f"     Text: {' '.join(text_content)}")

    if not buttons:
        print("❌ No buttons found in the semantic tree")
        return

    # Test reverse tree generation on first button
    print(f"\n🔍 Testing reverse tree generation on first button...")
    test_button = buttons[0]

    print(f"Target button - Tag: {test_button.tag}, ID: {test_button.id}")
    print(f"Button attributes: {test_button.attributes}")

    # Test parent mapping first
    print("\n🔍 Creating parent mapping...")
    parent_map = create_parent_mapping(semantic_tree)
    print(f"✅ Created parent mapping with {len(parent_map)} entries")

    # Check if our button is in the mapping
    if test_button.id in parent_map:
        parent = parent_map[test_button.id]
        if parent:
            print(f"Button parent: {parent.tag} (ID: {parent.id})")
        else:
            print("Button is root (no parent)")
    else:
        print("❌ Button not found in parent mapping")
        return

    # Generate reverse tree
    print("\n🔍 Generating reverse tree...")
    try:
        reverse_tree = generate_reverse_tree(test_button, semantic_tree)
        print("✅ Successfully generated reverse tree!")

        # Convert to text representation
        print("\n📝 Reverse tree text representation:")
        text_repr = reverse_tree.to_text()

        # Save to file for better readability
        output_file = "reverse_tree_output.txt"
        with open(output_file, 'w') as f:
            f.write("REVERSE TREE TEST OUTPUT\n")
            f.write("="*80 + "\n\n")
            f.write(f"Target Button Details:\n")
            f.write(f"- Tag: {test_button.tag}\n")
            f.write(f"- ID: {test_button.id}\n")
            f.write(f"- Attributes: {test_button.attributes}\n")
            f.write(f"- Content: {[child.text for child in test_button.content if isinstance(child, SemanticTextNode)]}\n\n")
            f.write("REVERSE TREE STRUCTURE:\n")
            f.write("="*80 + "\n\n")
            f.write(text_repr)
            f.write("\n\n" + "="*80 + "\n")
            f.write("END OF REVERSE TREE OUTPUT\n")

        print(f"✅ Reverse tree saved to: {output_file}")

        # Also save just the JSON part for easier reading
        json_output = "reverse_tree.json"
        reverse_tree_dict = reverse_tree.to_dict()
        with open(json_output, 'w') as f:
            json.dump(reverse_tree_dict, f, indent=2)

        print(f"✅ JSON structure saved to: {json_output}")

    except Exception as e:
        print(f"❌ Error generating reverse tree: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reverse_tree()