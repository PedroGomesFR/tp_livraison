"""Prise en compte de la priorité dans la sélection des colis.

Règle retenue : on transforme la valeur en une « utilité » pondérée par la
priorité, puis on réutilise le même algorithme de sac à dos (optimal) :

    utilite = valeur * (1 + alpha * (priorite - 1) / (PRIORITE_MAX - 1))

- priorité 1 -> utilité = valeur                (aucun bonus)
- priorité 5 -> utilité = valeur * (1 + alpha)  (bonus maximal)

Avec alpha = 1 (valeur par défaut), un colis de priorité 5 « vaut » deux fois
sa valeur. alpha = 0 revient au problème sans priorité ; un alpha très grand
fait passer la priorité avant tout le reste.

Pourquoi un bonus multiplicatif plutôt qu'additif ?
- il reste proportionnel à la valeur (un colis sans valeur ne devient pas
  intéressant juste parce qu'il est prioritaire) ;
- il ne dépend pas de l'échelle des valeurs (euros, centimes...) ;
- le poids reste géré par la contrainte de capacité, donc pas besoin de
  l'intégrer dans la formule.
"""

from colis import PRIORITE_MAX, PRIORITE_MIN

ALPHA_DEFAUT = 1.0


def creer_utilite_priorite(alpha=ALPHA_DEFAUT):
    if alpha < 0:
        raise ValueError("alpha doit être positif.")
    etendue = PRIORITE_MAX - PRIORITE_MIN

    def utilite(c):
        return c.valeur * (1 + alpha * (c.priorite - PRIORITE_MIN) / etendue)

    return utilite
