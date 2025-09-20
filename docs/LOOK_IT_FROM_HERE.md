# Look It from Here: Reverse Tree Embeddings for Web Automation

## 1. Problem

Current web automation relies on brittle CSS selectors and XPath expressions that are difficult to write, maintain, and understand. Developers must manually craft complex selectors like `div.form-container > fieldset:nth-child(2) > input[type="submit"]` instead of simply saying "submit button for shipping address". Even state-of-the-art AI models still struggle with medium (58% SOTA) and hard (43.2% SOTA) cases on Mind2Web benchmark, suggesting current approaches hit fundamental limitations in understanding hierarchical element relationships.

## 2. Solution

Our "Look It from Here" approach enables natural language specification of hierarchical elements through reverse tree embeddings. Instead of complex selectors, users can specify elements semantically: "submit button for billing form" or "add to cart for the wireless headphones". We encode DOM structure from each element's perspective - building reverse trees that capture parent chains, nearby siblings, and local context, then combine with page-level embeddings. This creates a natural language interface for hierarchical element selection that understands structural relationships and semantic meaning.

## Todo

- [ ] Build 'Look It from Here' breakthrough prototype
- [ ] Create GitHub repo and initial implementation
- [ ] Download Mind2Web dataset for validation
- [ ] Test reverse tree approach on real examples
- [ ] Implement page + element embedding fusion
- [ ] Target natural language element specification improvements