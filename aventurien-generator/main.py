#!/usr/bin/env python3
"""Aventurien Stadt-Generator für DSA5."""

import argparse
import json
from generators import StadtGenerator, NPCGenerator


def main():
    parser = argparse.ArgumentParser(description="Aventurien Stadt-Generator")
    parser.add_argument("--seed", type=int, help="Seed für Reproduzierbarkeit")
    parser.add_argument("--region", type=str, help="Region (z.B. Mittelreich, Thorwal)")
    parser.add_argument("--npcs", type=int, default=5, help="Anzahl zu generierender NPCs")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")
    args = parser.parse_args()

    stadt_gen = StadtGenerator(seed=args.seed, region=args.region)
    stadt = stadt_gen.generiere()

    npc_gen = NPCGenerator(seed=stadt.seed + 1, kultur=stadt.kultur)
    npcs = [npc_gen.generiere() for _ in range(args.npcs)]
    stadt.npcs = npcs

    if args.json:
        print(json.dumps(to_dict(stadt), indent=2, ensure_ascii=False))
    else:
        print_stadt(stadt)


def to_dict(obj) -> dict:
    """Konvertiert Dataclass zu Dict."""
    from dataclasses import asdict
    return asdict(obj)


def print_stadt(stadt):
    """Gibt die Stadt formatiert aus."""
    print(f"\n{'='*60}")
    print(f"  {stadt.name}")
    print(f"  Seed: {stadt.seed}")
    print(f"{'='*60}\n")

    print(f"Region:     {stadt.region}")
    print(f"Kultur:     {stadt.kultur}")
    print(f"Größe:      {stadt.groesse}")
    print(f"Einwohner:  ca. {stadt.einwohner:,}".replace(",", "."))
    print()

    print(f"Regierung:  {stadt.regierung.get('form', 'unbekannt')}")
    print(f"            Titel: {stadt.regierung.get('titel', 'unbekannt')}")
    print()

    print(f"Wirtschaft: {stadt.wirtschaft.get('hauptressource', '-')}")
    print(f"            Wohlstand: {stadt.wirtschaft.get('wohlstand', '-')}")
    print()

    if stadt.tempel:
        print("Tempel:")
        for t in stadt.tempel:
            name = t.get("name") if isinstance(t, dict) else t
            print(f"  - {name}")
        print()

    if stadt.gilden:
        print("Gilden:")
        for g in stadt.gilden:
            print(f"  - {g}")
        print()

    if stadt.besonderheiten:
        print("Besonderheiten:")
        for b in stadt.besonderheiten:
            print(f"  - {b}")
        print()

    if stadt.npcs:
        print(f"\nWichtige Persönlichkeiten:")
        print("-" * 40)
        for npc in stadt.npcs:
            props = ", ".join(npc.persoenlichkeit) if npc.persoenlichkeit else ""
            print(f"  {npc.name}")
            print(f"    {npc.alter}er {npc.geschlecht}er {npc.profession}")
            if props:
                print(f"    Eigenschaften: {props}")
            if npc.besonderheit:
                print(f"    Besonderheit: {npc.besonderheit}")
            print()


if __name__ == "__main__":
    main()
