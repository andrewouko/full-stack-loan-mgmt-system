from abc import abstractmethod
from typing import Callable, Generic, Optional, TypeVar, Protocol

from models import PaginationResult


class Identifiable(Protocol):
    id: int


T = TypeVar('T', bound=Identifiable)


DEFAULT_LIMIT = 10


class DataStore(Generic[T]):
    @abstractmethod
    def add(self, item: T) -> T:
        pass

    @abstractmethod
    def get_all(self, cursor: Optional[int], limit: Optional[int], filter_fn: Optional[Callable[[T], bool]] = None) -> tuple[list[T], PaginationResult]:
        """
            Retrieve all items with optional pagination and filtering.

        Args:
            cursor (Optional[int]): The id of the last item from the previous page.
            limit (Optional[int]): Maximum number of items to return. If None, a default limit is applied.
            filter_fn (Optional[Callable[[T], bool]], optional): A function to filter items. E.g. lambda x: x.name == "example". Defaults to None.

        Returns:
            tuple[list[T], PaginationResult]: A tuple containing the list of items and pagination metadata.
        """
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[T]:
        pass


# Uses the in-memory seed data for storage
class InMemoryDataStore(DataStore[T]):
    def __init__(self, initial_items: list[T]) -> None:
        self._items = initial_items

    def add(self, item: T) -> T:
        existing_id = self.get_by_id(item.id)
        if existing_id is not None:
            raise ValueError(f"Item with id {item.id} already exists.")
        self._items.append(item)
        return item

    def get_all(self, cursor: Optional[int], limit: Optional[int], filter_fn: Optional[Callable[[T], bool]] = None) -> tuple[list[T], PaginationResult]:
        filtered_items = self._items
        if filter_fn is not None:
            filtered_items = list(filter(filter_fn, self._items))

        start_index = 0
        if cursor is not None:
            for index, item in enumerate(filtered_items):
                if item.id == cursor:
                    start_index = index + 1
                    break

        result_limit = limit if limit is not None else DEFAULT_LIMIT
        result_items = filtered_items[start_index:start_index + result_limit]
        total_items = len(filtered_items)
        
        # Check if there are more items after the current page
        has_more = start_index + result_limit < total_items
        next_cursor = result_items[-1].id if has_more and len(result_items) > 0 else None

        pagination_result = PaginationResult(total_items=total_items, next_cursor=next_cursor)
        return result_items, pagination_result

    def get_by_id(self, item_id: int) -> Optional[T]:
        for item in self._items:
            if item.id == item_id:
                return item
        return None
