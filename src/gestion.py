"""Gestion de la collection de colis."""

from colis import Colis
from tri import tri_fusion

CRITERES = {
    "poids": lambda c: c.poids,
    "valeur": lambda c: c.valeur,
    "priorite": lambda c: c.priorite,
}


class GestionColis:
    """Stocke les colis dans deux structures complémentaires :

    - une liste (ordre d'insertion, parcours séquentiel pour l'affichage) ;
    - une table de hachage (dict) id -> colis pour la recherche en O(1) moyen.

    Les vues triées sont mises en cache et invalidées à chaque ajout :
    trier une fois coûte O(n log n), réafficher ensuite coûte O(n).
    """

    def __init__(self):
        self._liste = []
        self._par_id = {}
        self._cache_tris = {}

    def __len__(self):
        return len(self._liste)

    # --- Ajout --------------------------------------------------------------
    def ajouter(self, colis: Colis):
        """O(1) amorti (append + insertion dans le dict)."""
        if colis.id in self._par_id:
            raise ValueError(f"Un colis avec l'identifiant {colis.id} existe déjà.")
        self._liste.append(colis)
        self._par_id[colis.id] = colis
        self._cache_tris.clear()

    def ajouter_plusieurs(self, colis_iterable):
        for c in colis_iterable:
            self.ajouter(c)

    # --- Consultation -------------------------------------------------------
    def tous(self):
        """Colis dans l'ordre d'insertion. O(1) (pas de copie)."""
        return self._liste

    def rechercher(self, identifiant):
        """Recherche par identifiant via le dict : O(1) en moyenne."""
        return self._par_id.get(identifiant)

    def rechercher_lineaire(self, identifiant):
        """Version naïve O(n), conservée uniquement pour les comparaisons."""
        for c in self._liste:
            if c.id == identifiant:
                return c
        return None

    def trier_par(self, critere, decroissant=False):
        """Colis triés selon 'poids', 'valeur' ou 'priorite' (tri fusion, O(n log n))."""
        if critere not in CRITERES:
            raise ValueError(f"Critère inconnu : {critere}")
        cle_cache = (critere, decroissant)
        if cle_cache not in self._cache_tris:
            self._cache_tris[cle_cache] = tri_fusion(self._liste, CRITERES[critere], decroissant)
        return self._cache_tris[cle_cache]

    # --- Statistiques -------------------------------------------------------
    def statistiques(self):
        """Un seul parcours : O(n) en temps, O(d) en espace (d = nb de destinations)."""
        n = len(self._liste)
        if n == 0:
            return {"nombre": 0}
        poids_total = valeur_totale = 0
        par_priorite = {}
        par_destination = {}
        for c in self._liste:
            poids_total += c.poids
            valeur_totale += c.valeur
            par_priorite[c.priorite] = par_priorite.get(c.priorite, 0) + 1
            par_destination[c.destination] = par_destination.get(c.destination, 0) + 1
        return {
            "nombre": n,
            "poids_total": poids_total,
            "valeur_totale": valeur_totale,
            "poids_moyen": poids_total / n,
            "valeur_moyenne": valeur_totale / n,
            "par_priorite": dict(sorted(par_priorite.items())),
            "par_destination": dict(sorted(par_destination.items())),
        }
