# TP – Optimisation d'un système de préparation de livraisons

## Langage : Python 3

Python a été choisi pour sa lisibilité : le code reste proche du pseudo-code, ce qui permet de se concentrer sur les choix algorithmiques et leur justification. Ses structures natives (listes dynamiques, tables de hachage `dict`) correspondent exactement aux structures dont on a besoin. Contrepartie : Python est plus lent que C (facteur ~10 à 50 sur les boucles), ce qui est visible sur le sac à dos et le tri fusion écrit à la main, mais les ordres de grandeur (complexités) restent identiques.

Aucune bibliothèque externe n'est utilisée : uniquement la bibliothèque standard.

## Structure

```
projet/
├── src/
│   ├── colis.py       # classe Colis (id, poids, valeur, priorité 1..5, destination)
│   ├── tri.py         # tri fusion itératif écrit à la main (O(n log n), stable)
│   ├── gestion.py     # GestionColis : liste + dict id -> colis + cache des tris
│   ├── camion.py      # sac à dos 0/1 : programmation dynamique + glouton
│   ├── priorite.py    # règle de prise en compte de la priorité
│   ├── donnees.py     # exemple de l'énoncé, génération aléatoire, CSV
│   ├── benchmark.py   # mesures de performances (100 à 100 000 colis)
│   └── main.py        # menu interactif
├── README.md
└── rapport.pdf
```

## Utilisation

```bash
python3 src/main.py                       # menu interactif (démarre avec l'exemple de l'énoncé)
python3 src/benchmark.py                  # mesures de performances
```

Format CSV accepté : `id,poids,valeur,priorite,destination` (poids entiers, priorité de 1 = faible à 5 = très urgente).

## Choix algorithmiques (résumé)

| Opération | Stratégie | Temps | Espace |
|---|---|---|---|
| Ajouter un colis | `append` dans une liste + insertion dans un `dict` | O(1) amorti | O(1) |
| Rechercher par id | table de hachage (`dict`) | O(1) moyen, O(n) pire cas | O(n) pour l'index |
| Trier (poids / valeur / priorité) | tri fusion itératif + cache invalidé à l'ajout | O(n log n), puis O(1) si en cache | O(n) |
| Préparer le camion | sac à dos 0/1 par programmation dynamique (optimal) | O(n·W) | O(n·W) octets |
| Camion, très grandes instances | glouton par ratio utilité/poids (approché) | O(n log n) | O(n) |
| Priorité | utilité = valeur × (1 + α·(priorité−1)/4), puis même sac à dos | — | — |

Le détail (alternatives, justifications, mesures, questions de synthèse) est dans `rapport.pdf`.
