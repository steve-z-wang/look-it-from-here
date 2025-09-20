from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class WebElement(ABC):
    @abstractmethod
    async def click(self) -> bool:
        pass

    @abstractmethod
    async def fill(self, text: str) -> bool:
        pass

    @abstractmethod
    async def is_visible(self) -> bool:
        pass

    @abstractmethod
    async def get_text(self) -> Optional[str]:
        pass

    @abstractmethod
    async def get_inner_text(self) -> Optional[str]:
        pass

    @abstractmethod
    async def get_attributes(self) -> Dict[str, str]:
        pass

    @abstractmethod
    async def get_tag(self) -> Optional[str]:
        pass

    @abstractmethod
    async def get_children(self) -> List['WebElement']:
        pass

class Snapshot(ABC):
    @abstractmethod
    def to_dict(self) -> Optional[Dict[str, Any]]:
        pass

class WebPage(ABC):
    @abstractmethod
    async def find(self, selector: str) -> Optional[WebElement]:
        pass

    @abstractmethod
    async def find_all(self, selector: str) -> List[WebElement]:
        pass

    @abstractmethod
    async def get_root(self) -> Optional[WebElement]:
        pass

    @abstractmethod
    async def get_snapshot(self) -> Snapshot:
        pass

