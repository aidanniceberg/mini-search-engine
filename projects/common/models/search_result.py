from dataclasses import dataclass
from typing import List


@dataclass
class SearchResultItem:
    title: str
    description: str
    url: str
    linked_data: dict


@dataclass
class SearchResult:
    query: str
    count: int
    page: int
    page_size: int
    items: List[SearchResultItem]
