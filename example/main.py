from collections.abc import Iterable
from enum import Enum
from typing import NamedTuple

from find import Find, Operator, Predicate


class Suit(Enum):
    HEARTS = 1
    SPADES = 2
    DIAMONDS = 3
    CLUBS = 4

    def __str__(self) -> str:
        return self.name.capitalize()


class Card(NamedTuple):
    rank: int
    suit: Suit


cards: list[Card] = [Card(rank, suit) for suit in Suit for rank in range(1, 14)]

type CardPredicate = Predicate[Card]
type CardOperator = Operator[Card]


def lessThan(n: int) -> CardPredicate:
    def _less(c: Card) -> bool:
        return c.rank < n

    return _less


def suit(s: Suit) -> CardPredicate:
    def _match(c: Card) -> bool:
        return c.suit == s

    return _match


def faceCard(c: Card) -> bool:
    return c.rank >= 11 or c.rank == 1


def printThem(items: Iterable[Card]) -> None:
    items = list(items)
    print("[", end="")
    for i, item in enumerate(items):
        if i < len(items) - 1:
            print(f"{item.rank} of {item.suit}, ", end="")
        else:
            print(f"{item.rank} of {item.suit}", "]", sep="")


def rank(i: int) -> CardPredicate:
    def _match(c: Card) -> bool:
        return c.rank == i

    return _match


def main():
    print(
        Find(cards)
        .thatAre(faceCard)
        .mappedTo(lambda c: c.suit)
        .withoutDuplicates()
        .toList()
    )
    print(
        Find(cards)
        .distinctBy(lambda c: c.suit)
        .then(printThem)
        .areAll(lambda c: c.rank == 1)
    )
    Find(cards).orderedBy(lambda c: c.rank).then(printThem)

    Find(cards).thatAre(lambda c: c.rank > 4).groupedBy(lambda c: c.suit).then(
        lambda groups: print(
            "\n".join(
                (f"Suit: {suit}, Items: {[n.rank for n in card]}")
                for suit, card in groups
            )
        )
    )


if __name__ == "__main__":
    main()
