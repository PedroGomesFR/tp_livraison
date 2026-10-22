"""Préparation du chargement d'un camion : problème du sac à dos 0/1.

Deux stratégies :

1. Programmation dynamique (exacte, optimale)
   best[w] = meilleure utilité atteignable avec une capacité w.
   Pour chaque colis (poids p, utilité u), on parcourt w de W à p :
       best[w] = max(best[w], best[w - p] + u)
   Parcourir w en décroissant garantit qu'un colis n'est pris qu'une fois.
   Temps  : O(n * W)
   Espace : O(W) pour les valeurs + O(n * W) octets pour reconstruire
            la sélection (une table de décisions "pris / pas pris").

2. Glouton par ratio utilité / poids (approché, rapide)
   Temps : O(n log n) (tri), Espace : O(n).
   Pas toujours optimal ; on le complète en comparant avec le meilleur colis
   seul, ce qui garantit au moins 50 % de la valeur optimale.

`preparer_camion` choisit automatiquement la programmation dynamique tant que
n * W reste raisonnable, et bascule sur le glouton sinon.
"""

from dataclasses import dataclass, field

from tri import tri_fusion

# Au-delà de ce nombre de cellules (n * (W + 1)), la DP devient trop coûteuse.
LIMITE_CELLULES_DP = 20_000_000


@dataclass
class Chargement:
    capacite: int
    methode: str
    optimal: bool
    colis: list = field(default_factory=list)
    utilite_totale: float = 0.0

    @property
    def poids_total(self):
        return sum(c.poids for c in self.colis)

    @property
    def valeur_totale(self):
        return sum(c.valeur for c in self.colis)


def utilite_valeur(c):
    """Critère de base : on maximise uniquement la valeur."""
    return c.valeur


def sac_a_dos_dp(colis, capacite, utilite=utilite_valeur):
    """Solution optimale du sac à dos 0/1. Les poids doivent être des entiers."""
    if capacite < 0:
        raise ValueError("La capacité doit être positive.")
    candidats = [c for c in colis if c.poids <= capacite]
    best = [0.0] * (capacite + 1)
    decisions = []  # decisions[i][w] == 1 si le colis i est pris pour la capacité w

    for c in candidats:
        p, u = c.poids, utilite(c)
        pris = bytearray(capacite + 1)
        for w in range(capacite, p - 1, -1):
            candidat = best[w - p] + u
            if candidat > best[w]:
                best[w] = candidat
                pris[w] = 1
        decisions.append(pris)

    # Reconstruction : on remonte les décisions du dernier colis au premier.
    selection = []
    w = capacite
    for i in range(len(candidats) - 1, -1, -1):
        if decisions[i][w]:
            selection.append(candidats[i])
            w -= candidats[i].poids
    selection.reverse()

    return Chargement(capacite, "programmation dynamique", True, selection, best[capacite])


def sac_a_dos_glouton(colis, capacite, utilite=utilite_valeur):
    """Heuristique gloutonne : meilleurs ratios utilité/poids d'abord."""
    candidats = [c for c in colis if c.poids <= capacite]

    def ratio(c):
        return float("inf") if c.poids == 0 else utilite(c) / c.poids

    selection, poids, total = [], 0, 0.0
    for c in tri_fusion(candidats, ratio, decroissant=True):
        if poids + c.poids <= capacite:
            selection.append(c)
            poids += c.poids
            total += utilite(c)

    # Garde-fou : un seul gros colis très utile peut battre le glouton.
    if candidats:
        meilleur_seul = max(candidats, key=utilite)
        if utilite(meilleur_seul) > total:
            selection, total = [meilleur_seul], utilite(meilleur_seul)

    return Chargement(capacite, "glouton (ratio utilité/poids)", False, selection, total)


def preparer_camion(colis, capacite, utilite=utilite_valeur, limite=LIMITE_CELLULES_DP):
    """Choisit la stratégie adaptée à la taille du problème."""
    n = sum(1 for c in colis if c.poids <= capacite)
    if n * (capacite + 1) <= limite:
        return sac_a_dos_dp(colis, capacite, utilite)
    return sac_a_dos_glouton(colis, capacite, utilite)
