from typing import Callable

type Predicate[T] = Callable[[T], bool]
type Operator[T] = Callable[[list[T]], None]


class Find[T]:
    def __init__(self, cards: list[T]):
        self._cards = cards
        self._predicate: Predicate | None = None

    def thatAre(self, predicate: Predicate) -> Find:
        self._predicate = predicate
        return self

    def andAre(self, predicate: Predicate) -> Find:
        if self._predicate is None:
            self._predicate = predicate
        else:
            current = self._predicate
            self._predicate = lambda c: current(c) and predicate(c)

        return self

    def orAre(self, predicate: Predicate) -> Find:
        if self._predicate is None:
            self._predicate = predicate
        else:
            current = self._predicate
            self._predicate = lambda c: current(c) or predicate(c)

        return self

    def without(self, predicate: Predicate) -> Find:
        return self.andAre(lambda c: not predicate(c))

    def toList(self) -> list[T]:
        if self._predicate is None:
            return self._cards.copy()

        return [c for c in self._cards if self._predicate(c)]

    def count(self) -> int:
        return len(self.toList())

    def first(self) -> T | None:
        cards = self.toList()
        return cards[0] if cards else None

    def then(self, operator: Operator) -> Find:
        operator(self.toList())
        return self
