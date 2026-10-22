"""Tri fusion (merge sort) implémenté à la main.

- Temps : O(n log n) dans tous les cas (meilleur, moyen, pire).
- Espace : O(n) pour les tableaux auxiliaires.
- Stable : deux colis de même clé gardent leur ordre relatif, ce qui permet
  d'enchaîner des tris (ex. par destination puis par poids).

Version itérative (bottom-up) : pas de récursion, donc pas de risque de
dépasser la limite de pile de Python avec 100 000+ éléments.
"""


def tri_fusion(elements, cle=lambda x: x, decroissant=False):
    """Retourne une nouvelle liste triée selon `cle` (la liste d'origine est intacte)."""
    n = len(elements)
    if n <= 1:
        return list(elements)

    # On calcule la clé une seule fois par élément : n appels au lieu de n log n.
    source = [(cle(e), e) for e in elements]
    dest = [None] * n

    largeur = 1
    while largeur < n:
        for debut in range(0, n, 2 * largeur):
            milieu = min(debut + largeur, n)
            fin = min(debut + 2 * largeur, n)
            _fusionner(source, dest, debut, milieu, fin, decroissant)
        source, dest = dest, source
        largeur *= 2

    return [e for _, e in source]


def _fusionner(src, dst, debut, milieu, fin, decroissant):
    """Fusionne src[debut:milieu] et src[milieu:fin] (déjà triés) dans dst."""
    i, j, k = debut, milieu, debut
    while i < milieu and j < fin:
        # "<=" (ou ">=") garantit la stabilité : à égalité on prend la partie gauche.
        if (src[i][0] >= src[j][0]) if decroissant else (src[i][0] <= src[j][0]):
            dst[k] = src[i]
            i += 1
        else:
            dst[k] = src[j]
            j += 1
        k += 1
    while i < milieu:
        dst[k] = src[i]
        i += 1
        k += 1
    while j < fin:
        dst[k] = src[j]
        j += 1
        k += 1
