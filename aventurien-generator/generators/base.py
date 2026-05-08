import random
from typing import Any, Optional
import yaml
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class Generator:
    """Basisklasse für alle Generatoren mit Seed-Unterstützung."""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed if seed is not None else random.randint(0, 999999)
        random.seed(self.seed)

    def roll(self, sides: int = 100) -> int:
        return random.randint(1, sides)

    def roll_from_options(self, options: list[dict]) -> dict:
        """Wählt eine Option basierend auf min/max Bereichen."""
        roll = self.roll()
        for opt in options:
            min_val = opt.get("min", 0)
            max_val = opt.get("max", 100)
            if min_val <= roll <= max_val:
                return opt
        return options[-1]

    def pick(self, items: list) -> Any:
        return random.choice(items)

    def pick_weighted(self, items: list[dict], weight_key: str = "weight") -> dict:
        """Gewichtete Zufallsauswahl."""
        weights = [item.get(weight_key, 1) for item in items]
        return random.choices(items, weights=weights, k=1)[0]


def load_data(filename: str) -> dict:
    """Lädt YAML-Daten aus dem data-Verzeichnis."""
    path = DATA_DIR / filename
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
