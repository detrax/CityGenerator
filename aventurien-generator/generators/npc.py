from dataclasses import dataclass
from typing import Optional
from .base import Generator, load_data


@dataclass
class NPC:
    name: str
    geschlecht: str
    kultur: str
    profession: str
    alter: str
    persoenlichkeit: list
    besonderheit: Optional[str] = None


class NPCGenerator(Generator):
    def __init__(self, seed: Optional[int] = None, kultur: str = "Mittelländer"):
        super().__init__(seed)
        self.kultur = kultur
        self.namen = load_data("namen.yaml")
        self.npcs = load_data("npcs.yaml")

    def generiere(self) -> NPC:
        geschlecht = self.pick(["männlich", "weiblich"])
        return NPC(
            name=self._generiere_name(geschlecht),
            geschlecht=geschlecht,
            kultur=self.kultur,
            profession=self._waehle_profession(),
            alter=self._waehle_alter(),
            persoenlichkeit=self._waehle_eigenschaften(),
            besonderheit=self._waehle_besonderheit(),
        )

    def _generiere_name(self, geschlecht: str) -> str:
        kultur_namen = self.namen.get("personen", {}).get(self.kultur, {})
        if geschlecht == "männlich":
            vornamen = kultur_namen.get("maennlich", ["Alrik"])
        else:
            vornamen = kultur_namen.get("weiblich", ["Alrike"])
        nachnamen = kultur_namen.get("nachnamen", [""])
        vorname = self.pick(vornamen)
        nachname = self.pick(nachnamen)
        return f"{vorname} {nachname}".strip()

    def _waehle_profession(self) -> str:
        professionen = self.npcs.get("professionen", ["Bauer"])
        return self.pick(professionen)

    def _waehle_alter(self) -> str:
        alter = self.npcs.get("alter", [{"name": "erwachsen"}])
        return self.roll_from_options(alter).get("name", "erwachsen")

    def _waehle_eigenschaften(self) -> list:
        eigenschaften = self.npcs.get("eigenschaften", [])
        anzahl = random.randint(1, 3)
        return random.sample(eigenschaften, k=min(anzahl, len(eigenschaften)))

    def _waehle_besonderheit(self) -> Optional[str]:
        if self.roll() > 80:
            besonderheiten = self.npcs.get("besonderheiten", [])
            return self.pick(besonderheiten) if besonderheiten else None
        return None


import random
