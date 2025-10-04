
# Reverse Tree Embeddings for Web Automation

## Overview

The reverse tree approach transforms web page semantic trees to optimize natural language element selection. Instead of searching through a traditional DOM hierarchy, each potential target element becomes the root of its own contextual tree, preserving hierarchical relationships while emphasizing the target element for embedding generation.

## Why Reverse Trees?

Traditional web automation requires complex DOM traversal to find elements based on natural language queries like "click the search button in the header". Reverse trees solve this by:

1. **Context-Aware Selection**: Target elements become roots while maintaining their semantic context
2. **Better Embeddings**: ML models can focus on the target while understanding its hierarchical position
3. **Natural Language Alignment**: Structure matches how humans describe web elements ("button in form in header")

## Example Transformation

### Original Semantic Tree
```json
{
    "tag": "parent-1",
    "role": "parent-1-role",
    "content": [
        {
            "tag": "parent-2",
            "role": "parent-2-role",
            "content": [
                {
                    "tag": "sibling-1",
                    "role": "sibling-1-role"
                },
                {
                    "tag": "a",
                    "role": "my-role",
                    "content": [
                        "my text"
                    ]
                },
                {
                    "tag": "sibling-2",
                    "role": "sibling-2-role"
                }
            ]
        }
    ]
}
```

### Reverse Tree (Rerooted on target element "a")
```json
{
    "tag": "a",
    "role": "my-role",
    "content": [
        "my text"
    ],
    "parent": {
        "tag": "parent-2",
        "role": "parent-2-role",
        "content": [
            {
                "tag": "sibling-1",
                "role": "sibling-1-role"
            },
            "_FOCUS_ELEMENT_",
            {
                "tag": "sibling-2",
                "role": "sibling-2-role"
            }
        ],
        "parent": {
            "tag": "parent-1",
            "role": "parent-1-role",
            "content": [
                "_FOCUS_PATH_"
            ]
        }
    }
}
```

## Use Cases

### Query: "Click the login button"
- Each button element gets its own reverse tree
- Embedding captures: button properties + surrounding context
- Natural language matching finds the best semantic match

### Query: "Fill the email field in the registration form"
- Input field becomes root with form context preserved
- Embedding includes form semantics and field relationships
- Precise element identification with contextual understanding

## Implementation Integration

1. **Generate reverse tree for each SemanticElementNode**
2. **Create embeddings from reverse tree text representation**
3. **Store in EmbeddingNode with mapping to original semantic node**
4. **Use for natural language query matching and element selection**

This approach transforms semantic trees into embedding-optimized structures that align with human mental models of web page navigation.