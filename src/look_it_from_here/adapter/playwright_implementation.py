from typing import List, Optional, Dict, Union
from playwright.async_api import Page, Locator
from ..core.interfaces import WebElement, WebPage, Snapshot
from ..core.snapshot import WebSnapshot
from ..core.transform import create_html_tree, create_semantic_tree, create_embeddings_from_semantic_tree
from ..core.embeddings import Embedder


class PlaywrightElement(WebElement):
    def __init__(self, locator: Locator):
        self.locator = locator

    async def click(self) -> bool:
        try:
            await self.locator.click()
            return True
        except Exception:
            return False

    async def fill(self, text: str) -> bool:
        try:
            await self.locator.fill(text)
            return True
        except Exception:
            return False

    async def is_visible(self) -> bool:
        try:
            return await self.locator.is_visible()
        except Exception:
            return False


    async def get_attributes(self) -> Dict[str, str]:
        """Get ALL attributes from the element."""
        try:
            # Use JavaScript to get all attributes at once
            result = await self.locator.evaluate("""
                el => {
                    const result = {};
                    for (const attr of el.attributes) {
                        result[attr.name] = attr.value;
                    }
                    return result;
                }
            """)
            return result
        except Exception:
            return {}

    async def get_tag(self) -> Optional[str]:
        try:
            return await self.locator.evaluate("el => el.tagName.toLowerCase()")
        except Exception:
            return None

    async def get_children(self) -> List[Union[WebElement, str]]:
        """Get all child nodes including text nodes."""
        try:
            # Get information about all child nodes
            children_info = await self.locator.evaluate("""
                el => {
                    const children = [];
                    for (const node of el.childNodes) {
                        if (node.nodeType === Node.TEXT_NODE) {
                            const text = node.textContent;
                            // Only include non-empty text nodes
                            if (text && text.trim()) {
                                children.push({type: 'text', content: text});
                            }
                        } else if (node.nodeType === Node.ELEMENT_NODE) {
                            children.push({type: 'element', index: [...el.children].indexOf(node)});
                        }
                    }
                    return children;
                }
            """)

            # Build mixed list of WebElements and strings
            result = []
            element_locators = self.locator.locator("xpath=./*")

            for child_info in children_info:
                if child_info['type'] == 'text':
                    result.append(child_info['content'])
                elif child_info['type'] == 'element':
                    index = child_info['index']
                    if index >= 0:
                        result.append(PlaywrightElement(element_locators.nth(index)))

            return result
        except Exception:
            return []


class PlaywrightPage(WebPage):
    def __init__(self, page: Page):
        self.page = page

    async def find(self, selector: str) -> Optional[WebElement]:
        try:
            locator = self.page.locator(selector).first
            count = await locator.count()
            if count > 0:
                return PlaywrightElement(locator)
            return None
        except Exception:
            return None

    async def find_all(self, selector: str) -> List[WebElement]:
        try:
            locator = self.page.locator(selector)
            count = await locator.count()
            return [PlaywrightElement(locator.nth(i)) for i in range(count)]
        except Exception:
            return []

    async def get_root(self) -> Optional[WebElement]:
        try:
            html_locator = self.page.locator("html")
            count = await html_locator.count()
            if count > 0:
                return PlaywrightElement(html_locator)
            return None
        except Exception:
            return None

    async def get_snapshot(self) -> Snapshot:
        """Create a snapshot of the current page state."""
        # Build the trees
        html_tree, element_mapping = await create_html_tree(self)

        # Only create semantic tree if html_tree exists
        if html_tree:
            semantic_tree, node_mapping = create_semantic_tree(html_tree)
        else:
            semantic_tree, node_mapping = None, {}

        # Generate embeddings for semantic tree
        semantic_to_embedding = None
        if semantic_tree:
            embedder = Embedder()
            semantic_to_embedding = create_embeddings_from_semantic_tree(semantic_tree, embedder)

        # Create and return snapshot
        return WebSnapshot(html_tree, semantic_tree, element_mapping, node_mapping, semantic_to_embedding)