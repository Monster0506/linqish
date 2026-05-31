from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import Protocol

type Predicate[T] = Callable[[T], bool]
type Operator[T] = Callable[[Iterable[T]], None]
type Mapper[T, U] = Callable[[T], U]
type KeySelector[T, K] = Callable[[T], K]
type Group[K, T] = tuple[K, list[T]]


class SupportsLessThan(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


class Find[T: Hashable](Iterable[T]):
    def __init__(
        self,
        items: Iterable[T],
        predicate: Predicate[T] | None = None,
    ):
        self._items = items
        self._predicate = predicate

    def __iter__(self) -> Iterator[T]:
        if self._predicate is None:
            yield from self._items
        else:
            yield from filter(self._predicate, self._items)

    def thatAre(self, predicate: Predicate[T]) -> Find[T]:
        if self._predicate is None:
            return Find(self._items, predicate)

        current = self._predicate
        return Find(
            self._items,
            lambda x: current(x) and predicate(x),
        )

    def andAre(self, predicate: Predicate[T]) -> Find[T]:
        return self.thatAre(predicate)

    def orAre(self, predicate: Predicate[T]) -> Find[T]:
        if self._predicate is None:
            return Find(self._items, predicate)

        current = self._predicate
        return Find(
            self._items,
            lambda x: current(x) or predicate(x),
        )

    def without(self, predicate: Predicate[T]) -> Find[T]:
        if self._predicate is None:
            return Find(
                self._items,
                lambda x: not predicate(x),
            )

        current = self._predicate
        return Find(
            self._items,
            lambda x: current(x) and not predicate(x),
        )

    def select[U](self, mapper: Mapper[T, U]) -> Find[U]:
        return Find(map(mapper, self))

    def selectMany[U](
        self,
        mapper: Callable[[T], Iterable[U]],
    ) -> Find[U]:
        return Find(item for parent in self for item in mapper(parent))

    def distinct(self) -> Find[T]:
        def _distinct() -> Iterator[T]:
            seen: set[Hashable] = set()

            for item in self:
                if item not in seen:
                    seen.add(item)
                    yield item

        return Find(_distinct())

    def distinctBy[K: Hashable](self, key: KeySelector[T, K]) -> Find[T]:
        def _distinct() -> Iterator[T]:
            seen: set[Hashable] = set()

            for item in self:
                k = key(item)
                if k not in seen:
                    seen.add(k)
                    yield item

        return Find(_distinct())

    def first(self) -> T | None:
        return next(iter(self), None)

    def count(self) -> int:
        return sum(1 for _ in self)

    def toList(self) -> list[T]:
        return list(self)

    def then(self, operator: Operator[T]) -> Find[T]:
        operator(self)
        return self

    def any(self) -> bool:
        return any(True for _ in self)

    def all(self, predicate: Predicate[T]) -> bool:
        return all(predicate(x) for x in self)

    def orderBy[K: SupportsLessThan](self, key: KeySelector[T, K]) -> Find[T]:
        return Find(sorted(self, key=key))

    def groupBy[K: Hashable](
        self,
        key: KeySelector[T, K],
    ) -> Find[Group[K, T]]:
        groups: defaultdict[K, list[T]] = defaultdict(list)

        for item in self:
            groups[key(item)].append(item)

        return Find[Group[K, T]](groups.items())

