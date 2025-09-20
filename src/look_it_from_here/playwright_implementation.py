from typing import List, Optional, Dict
from playwright.async_api import Page, Locator
from .interfaces import WebElement, WebPage, Snapshot
from .snapshot import WebSnapshot
from .pipeline import create_html_tree, create_semantic_tree


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

    async def get_text(self) -> Optional[str]:
        try:
            # Get direct text nodes only (not from child elements)
            result = await self.locator.evaluate("""
                el => {
                    const textNodes = [...el.childNodes]
                        .filter(node => node.nodeType === Node.TEXT_NODE)
                        .map(node => node.textContent)
                        .join('');

                    return textNodes.trim() || null;
                }
            """)
            return result if result else None
        except Exception:
            return None

    async def get_inner_text(self) -> Optional[str]:
        """Get the complete inner text including text from all descendant elements."""
        try:
            result = await self.locator.evaluate("el => el.innerText")
            return result.strip() if result and result.strip() else None
        except Exception:
            return None

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

    async def get_children(self) -> List[WebElement]:
        try:
            child_locators = self.locator.locator("xpath=./*")
            count = await child_locators.count()
            return [PlaywrightElement(child_locators.nth(i)) for i in range(count)]
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

        # Create and return snapshot
        return WebSnapshot(html_tree, semantic_tree, element_mapping, node_mapping)