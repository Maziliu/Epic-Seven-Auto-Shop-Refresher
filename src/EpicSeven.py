from typing import Optional


class Inventory:
    DEFAULT_ITEMS: dict[str, int] = {
        "Covenant": 0,
        "Mystic": 0,
        # "Test": 0
    }

    def __init__(self, initialItems: Optional[dict[str, int]] = None):
        self.items: dict[str, int] = (
            initialItems.copy() if initialItems is not None else self.DEFAULT_ITEMS.copy()
        )

    def incrementItem(self, item: str, amount: int = 1) -> None:
        if item not in self.items:
            self.items[item] = 0
        self.items[item] += amount

    def getItemCount(self, item: str) -> int:
        return self.items.get(item, 0)

    def getItems(self) -> dict[str, int]:
        return self.items.copy()

    def getKeys(self) -> list[str]:
        return list(self.items.keys())

    def reset(self) -> None:
        for key in self.items:
            self.items[key] = 0

    def __getitem__(self, item: str) -> int:
        return self.getItemCount(item)

    def __setitem__(self, item: str, value: int) -> None:
        self.items[item] = value

    def __repr__(self) -> str:
        return f"Inventory({self.items})"
