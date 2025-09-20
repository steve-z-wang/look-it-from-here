#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from look_it_from_here.html_display_node import HTMLDisplayNode

def display_tree_to_xml(node, indent=0):
    """Test version of XML converter"""
    indent_str = "  " * indent

    # Build opening tag with attributes
    attrs = ""
    for key, value in node.attributes:
        # Escape XML special characters in attribute values
        escaped_value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        attrs += f' {key}="{escaped_value}"'

    opening_tag = f"{indent_str}<{node.tag}{attrs}>"

    # Handle self-closing tags
    if not node.text and not node.children:
        return f"{indent_str}<{node.tag}{attrs}/>"

    # Build content
    content_parts = []

    # Add text if present
    if node.text:
        # Escape XML special characters in text content
        escaped_text = node.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        content_parts.append(escaped_text)

    # Add children
    if node.children:
        if node.text:
            # Mixed content - put children inline
            child_xml = []
            for child in node.children:
                child_xml.append(display_tree_to_xml(child, 0).strip())
            content_parts.extend(child_xml)
            return f"{opening_tag}{''.join(content_parts)}</{node.tag}>"
        else:
            # Children only - use proper indentation
            child_xml = []
            for child in node.children:
                child_xml.append(display_tree_to_xml(child, indent + 1))
            closing_tag = f"{indent_str}</{node.tag}>"
            return f"{opening_tag}\n" + "\n".join(child_xml) + f"\n{closing_tag}"

    # Text only
    return f"{opening_tag}{''.join(content_parts)}</{node.tag}>"

# Create test mixed content structure
root = HTMLDisplayNode(tag='body')

# Paragraph with mixed content: "This is a link in the middle of some text."
p = HTMLDisplayNode(tag='p', text='This is ')
a = HTMLDisplayNode(tag='a', text='a link', attributes=[('href', '#')])
p.add_child(a)
# Add more text after the link - but our current model doesn't support this
# So let's test what we have

root.add_child(p)

print('XML Output (Current approach - paragraph with initial text + child):')
print(display_tree_to_xml(root))
print()

# Test case 2: Mixed content with full text AND children (new approach)
root2 = HTMLDisplayNode(tag='body')
p2 = HTMLDisplayNode(tag='p', text='This is a link in the middle of some text.')  # Full readable text
a2 = HTMLDisplayNode(tag='a', text='a link', attributes=[('href', '#')])
strong = HTMLDisplayNode(tag='strong', text='some text')

p2.add_child(a2)
p2.add_child(strong)
root2.add_child(p2)

print('XML Output (Mixed content with full text + children):')
print(display_tree_to_xml(root2))