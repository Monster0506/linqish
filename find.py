from collections.abc import Iterable, Callable

type Predicate[T] = Callable[[T], bool]
type Operator[T] = Callable[[Iterable[T]], None]
type Mapper[T, U] = Callable[[T], U]


class Find[T]:
    def __init__(self, cards: Iterable[T]):
        self._items = cards
        self._predicate: Predicate[T] | None = None

    def __iter__(self):
        if self._predicate is None:
            yield from self._items
        else:
            yield from filter(self._predicate, self._items)


    def thatAre(self, predicate: Predicate[T]) -> Find[T]:
        self._predicate = predicate
        return self

    def andAre(self, predicate: Predicate[T]) -> Find[T]:
        if self._predicate is None:
            self._predicate = predicate
        else:
            current = self._predicate
            self._predicate = lambda c: current(c) and predicate(c)

        return self

    def orAre(self, predicate: Predicate[T]) -> Find[T]:
        if self._predicate is None:
            self._predicate = predicate
        else:
            current = self._predicate
            self._predicate = lambda c: current(c) or predicate(c)

        return self

    def without(self, predicate: Predicate[T]) -> Find[T]:
        return self.andAre(lambda c: not predicate(c))

    def toList(self) -> list[T]:
        if self._predicate is None:
            return list(self._items).copy()

        return [c for c in self._items if self._predicate(c)]

    def count(self) -> int:
        return len(self.toList())

    def first(self) -> T | None:
        cards = self.toList()
        return cards[0] if cards else None

    def then(self, operator: Operator[T]) -> Find[T]:
        operator(self.toList())
        return self
        
    def select(self, _map: Mapper[T, U]) -> Find[U]:
        return Find(map(_map, self.toList()))
