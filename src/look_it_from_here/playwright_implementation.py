from typing import List, Optional
from playwright.async_api import Page, Locator
from interfaces import WebElement, WebPage


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
            return await self.locator.text_content()
        except Exception:
            return None

    async def get_attribute(self, attribute: str) -> Optional[str]:
        try:
            return await self.locator.get_attribute(attribute)
        except Exception:
            return None

    async def get_tag(self) -> Optional[str]:
        try:
            return await self.locator.evaluate("el => el.tagName.toLowerCase()")
        except Exception:
            return None

    async def get_children(self) -> List[WebElement]:
        try:
            child_locators = self.locator.locator("> *")
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