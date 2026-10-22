"""Mesures de performances pour différentes tailles de données.

Lancement : python3 src/benchmark.py
"""

import random
import time

from camion import sac_a_dos_dp, sac_a_dos_glouton
from donnees import generer
from gestion import GestionColis
from priorite import creer_utilite_priorite
from tri import tri_fusion

TAILLES = [100, 1_000, 10_000, 100_000]
NB_RECHERCHES = 1_000
CAPACITE = 50


def chrono(fonction, *args, **kwargs):
    debut = time.perf_counter()
    resultat = fonction(*args, **kwargs)
    return (time.perf_counter() - debut) * 1000, resultat


def ligne(*cellules):
    print(" | ".join(f"{c:>14}" for c in cellules))


def main():
    print(f"Recherches : {NB_RECHERCHES} identifiants tirés au hasard. Capacité camion : {CAPACITE} kg.")
    print("Temps en millisecondes.\n")
    ligne("n", "ajout total", "rech. dict", "rech. linéaire", "tri fusion", "sorted()",
          "sac DP", "sac glouton", "val. DP", "val. glouton")

    utilite = creer_utilite_priorite()
    for n in TAILLES:
        colis = generer(n)
        gestion = GestionColis()
        t_ajout, _ = chrono(gestion.ajouter_plusieurs, colis)

        rng = random.Random(0)
        ids = [rng.randint(1, n) for _ in range(NB_RECHERCHES)]
        t_dict, _ = chrono(lambda: [gestion.rechercher(i) for i in ids])
        # La recherche linéaire est très lente pour 100 000 colis : on extrapole
        # à partir de 100 recherches pour garder un benchmark court.
        nb_lin = min(NB_RECHERCHES, 100)
        t_lin, _ = chrono(lambda: [gestion.rechercher_lineaire(i) for i in ids[:nb_lin]])
        t_lin *= NB_RECHERCHES / nb_lin

        t_tri, _ = chrono(tri_fusion, colis, lambda c: c.poids)
        t_sorted, _ = chrono(sorted, colis, key=lambda c: c.poids)

        t_dp, dp = chrono(sac_a_dos_dp, colis, CAPACITE, utilite)
        t_gl, gl = chrono(sac_a_dos_glouton, colis, CAPACITE, utilite)

        ligne(n, f"{t_ajout:.2f}", f"{t_dict:.2f}", f"{t_lin:.1f}", f"{t_tri:.2f}",
              f"{t_sorted:.2f}", f"{t_dp:.1f}", f"{t_gl:.2f}",
              f"{dp.utilite_totale:.1f}", f"{gl.utilite_totale:.1f}")

    print("\nInfluence de la capacité W sur le sac à dos (n = 1 000) :")
    ligne("W", "sac DP", "sac glouton", "val. DP", "val. glouton", "écart %")
    colis = generer(1_000, graine=7)
    for w in [50, 500, 5_000]:
        t_dp, dp = chrono(sac_a_dos_dp, colis, w, utilite)
        t_gl, gl = chrono(sac_a_dos_glouton, colis, w, utilite)
        ecart = 100 * (dp.utilite_totale - gl.utilite_totale) / dp.utilite_totale
        ligne(w, f"{t_dp:.1f}", f"{t_gl:.2f}", f"{dp.utilite_totale:.1f}",
              f"{gl.utilite_totale:.1f}", f"{ecart:.2f}")


if __name__ == "__main__":
    main()
