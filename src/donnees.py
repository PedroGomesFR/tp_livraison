"""Jeux de données : exemple de l'énoncé, génération aléatoire, import/export CSV."""

import csv
import random

from colis import PRIORITE_MAX, PRIORITE_MIN, Colis

DESTINATIONS = ["Paris", "Lille", "Lyon", "Marseille", "Bordeaux",
                "Nantes", "Toulouse", "Strasbourg", "Nice", "Rennes"]


def exemple_enonce():
    return [
        Colis(101, 8, 20, 2, "Paris"),
        Colis(102, 3, 10, 5, "Lille"),
        Colis(103, 12, 40, 1, "Lyon"),
        Colis(104, 5, 25, 4, "Paris"),
        Colis(105, 2, 15, 3, "Lille"),
    ]


def generer(n, graine=42, id_depart=1, poids_max=30, valeur_max=100):
    """Génère n colis aléatoires (reproductibles grâce à la graine)."""
    rng = random.Random(graine)
    return [
        Colis(id_depart + i,
              rng.randint(1, poids_max),
              rng.randint(1, valeur_max),
              rng.randint(PRIORITE_MIN, PRIORITE_MAX),
              rng.choice(DESTINATIONS))
        for i in range(n)
    ]


def charger_csv(chemin):
    with open(chemin, newline="", encoding="utf-8") as f:
        return [Colis(int(l["id"]), int(l["poids"]), int(l["valeur"]),
                      int(l["priorite"]), l["destination"])
                for l in csv.DictReader(f)]


def sauver_csv(chemin, colis):
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "poids", "valeur", "priorite", "destination"])
        for c in colis:
            w.writerow([c.id, c.poids, c.valeur, c.priorite, c.destination])
