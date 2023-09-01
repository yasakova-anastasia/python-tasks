from dataclasses import dataclass, field, InitVar
from abc import ABC, abstractmethod


DISCOUNT_PERCENTS = 15


@dataclass(frozen=True, order=True)
class Item:
    # note: mind the order of fields (!)
    item_id: int = field(compare=False)
    title: str = field(compare=True)
    cost: int = field(compare=True)

    def __post_init__(self) -> None:
        assert self.cost > 0
        assert self.title


# Do not remove `# type: ignore`
# It is [a really old issue](https://github.com/python/mypy/issues/5374)
@dataclass  # type: ignore
class Position(ABC):
    item: Item

    @abstractmethod
    def cost(self) -> None:
        pass


@dataclass
class CountedPosition(Position):
    count: int = field(default=1)

    @property
    def cost(self) -> float:  # type: ignore
        return self.item.cost * self.count


@dataclass
class WeightedPosition(Position):
    weight: float = field(default=1)

    @property
    def cost(self) -> float:  # type: ignore
        return self.item.cost * self.weight


@dataclass
class Order:
    order_id: int
    positions: list[Position] = field(default_factory=list)
    have_promo: InitVar[bool] = False

    def __post_init__(self, val: bool) -> None:
        self._cost = 0
        if self.positions:
            temp = (100 - DISCOUNT_PERCENTS) / 100 if val else 1
            pos = [pos.cost for pos in self.positions]
            self._cost = int(sum(pos) * temp)  # type: ignore

    @property
    def cost(self) -> float:
        return self._cost
