"""Représentation d'un colis."""

from dataclasses import dataclass

# Convention : la priorité va de 1 (faible) à 5 (très urgente).
PRIORITE_MIN = 1
PRIORITE_MAX = 5


@dataclass
class Colis:
    id: int
    poids: int        # en kg (entier, nécessaire pour la programmation dynamique)
    valeur: int
    priorite: int
    destination: str

    def __post_init__(self):
        if self.poids < 0:
            raise ValueError("Le poids doit être positif.")
        if self.valeur < 0:
            raise ValueError("La valeur doit être positive.")
        if not PRIORITE_MIN <= self.priorite <= PRIORITE_MAX:
            raise ValueError(f"La priorité doit être entre {PRIORITE_MIN} et {PRIORITE_MAX}.")

    def __str__(self):
        return (f"{self.id:>7} | {self.poids:>6} | {self.valeur:>6} | "
                f"{self.priorite:>8} | {self.destination}")


ENTETE = f"{'ID':>7} | {'Poids':>6} | {'Valeur':>6} | {'Priorité':>8} | Destination"
