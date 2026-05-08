from dataclasses import dataclass, field
from typing import Optional
from .base import Generator, load_data


@dataclass
class Stadt:
    name: str
    seed: int
    groesse: str
    einwohner: int
    region: str
    kultur: str
    beschreibung: str = ""
    regierung: dict = field(default_factory=dict)
    tempel: list = field(default_factory=list)
    gilden: list = field(default_factory=list)
    wirtschaft: dict = field(default_factory=dict)
    besonderheiten: list = field(default_factory=list)
    npcs: list = field(default_factory=list)


class StadtGenerator(Generator):
    def __init__(self, seed: Optional[int] = None, region: Optional[str] = None):
        super().__init__(seed)
        self.data = load_data("staedte.yaml")
        self.regionen = load_data("regionen.yaml")
        self.namen = load_data("namen.yaml")
        self.region_vorgabe = region

    def generiere(self) -> Stadt:
        region = self._waehle_region()
        kultur = self._kultur_fuer_region(region)
        groesse_data = self.roll_from_options(self.data.get("groessen", []))

        return Stadt(
            name=self._generiere_name(kultur),
            seed=self.seed,
            groesse=groesse_data.get("name", "Dorf"),
            einwohner=self._berechne_einwohner(groesse_data),
            region=region,
            kultur=kultur,
            regierung=self._generiere_regierung(groesse_data),
            tempel=self._generiere_tempel(groesse_data),
            gilden=self._generiere_gilden(groesse_data),
            wirtschaft=self._generiere_wirtschaft(region),
            besonderheiten=self._generiere_besonderheiten(),
        )

    def _waehle_region(self) -> str:
        if self.region_vorgabe:
            return self.region_vorgabe
        regionen = list(self.regionen.get("regionen", {}).keys())
        return self.pick(regionen) if regionen else "Mittelreich"

    def _kultur_fuer_region(self, region: str) -> str:
        region_data = self.regionen.get("regionen", {}).get(region, {})
        kulturen = region_data.get("kulturen", ["Mittelländer"])
        return self.pick(kulturen)

    def _generiere_name(self, kultur: str) -> str:
        kultur_namen = self.namen.get("staedte", {}).get(kultur, {})
        praefixe = kultur_namen.get("praefixe", ["Neu"])
        suffixe = kultur_namen.get("suffixe", ["dorf"])
        return self.pick(praefixe) + self.pick(suffixe)

    def _berechne_einwohner(self, groesse: dict) -> int:
        min_pop = groesse.get("min_einwohner", 50)
        max_pop = groesse.get("max_einwohner", 200)
        return random.randint(min_pop, max_pop)

    def _generiere_regierung(self, groesse: dict) -> dict:
        formen = self.data.get("regierungsformen", [])
        if not formen:
            return {"form": "Vogt", "titel": "Vogt"}
        form = self.pick_weighted(formen)
        return {"form": form.get("name"), "titel": form.get("titel", "Bürgermeister")}

    def _generiere_tempel(self, groesse: dict) -> list:
        goetter = load_data("goetter.yaml").get("zwoelfgoetter", [])
        anzahl = min(groesse.get("max_tempel", 1), len(goetter))
        return random.sample(goetter, k=anzahl) if goetter else []

    def _generiere_gilden(self, groesse: dict) -> list:
        gilden = self.data.get("gilden", [])
        anzahl = min(groesse.get("max_gilden", 0), len(gilden))
        return random.sample(gilden, k=anzahl) if gilden else []

    def _generiere_wirtschaft(self, region: str) -> dict:
        region_data = self.regionen.get("regionen", {}).get(region, {})
        ressourcen = region_data.get("ressourcen", ["Landwirtschaft"])
        return {
            "hauptressource": self.pick(ressourcen),
            "wohlstand": self.roll_from_options(
                self.data.get("wohlstand", [{"name": "bescheiden"}])
            ).get("name", "bescheiden"),
        }

    def _generiere_besonderheiten(self) -> list:
        besonderheiten = self.data.get("besonderheiten", [])
        if not besonderheiten:
            return []
        anzahl = random.randint(0, 2)
        return random.sample(besonderheiten, k=min(anzahl, len(besonderheiten)))


import random
