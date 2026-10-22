"""Programme principal : menu de gestion des livraisons.

Lancement : python3 src/main.py
"""

import time

from camion import preparer_camion, utilite_valeur
from colis import ENTETE, PRIORITE_MAX, PRIORITE_MIN, Colis
from donnees import charger_csv, exemple_enonce, generer
from gestion import GestionColis
from priorite import ALPHA_DEFAUT, creer_utilite_priorite

AFFICHAGE_MAX = 30  # au-delà, on n'affiche que les premières lignes

MENU = """
===== GESTION DES LIVRAISONS =====
1. Afficher les colis
2. Ajouter un colis
3. Rechercher un colis
4. Organiser les colis (trier)
5. Préparer un camion
6. Afficher le chargement
7. Afficher les statistiques
8. Charger un jeu de données
0. Quitter"""


def lire_entier(message, minimum=None, maximum=None, defaut=None):
    while True:
        saisie = input(message).strip()
        if not saisie and defaut is not None:
            return defaut
        try:
            valeur = int(saisie)
        except ValueError:
            print("  -> Veuillez saisir un nombre entier.")
            continue
        if (minimum is not None and valeur < minimum) or (maximum is not None and valeur > maximum):
            print(f"  -> Valeur attendue entre {minimum} et {maximum}.")
            continue
        return valeur


def lire_reel(message, defaut):
    saisie = input(message).strip()
    try:
        return float(saisie) if saisie else defaut
    except ValueError:
        print(f"  -> Saisie invalide, valeur par défaut utilisée ({defaut}).")
        return defaut


def afficher_liste(colis):
    print(ENTETE)
    print("-" * len(ENTETE))
    for c in colis[:AFFICHAGE_MAX]:
        print(c)
    if len(colis) > AFFICHAGE_MAX:
        print(f"... ({len(colis) - AFFICHAGE_MAX} colis supplémentaires non affichés)")
    print(f"Total : {len(colis)} colis")


def menu_ajouter(gestion):
    try:
        c = Colis(
            lire_entier("Identifiant : "),
            lire_entier("Poids (kg, entier) : ", 0),
            lire_entier("Valeur : ", 0),
            lire_entier(f"Priorité ({PRIORITE_MIN}-{PRIORITE_MAX}) : ", PRIORITE_MIN, PRIORITE_MAX),
            input("Destination : ").strip() or "Inconnue",
        )
        gestion.ajouter(c)
        print("Colis ajouté.")
    except ValueError as e:
        print(f"Erreur : {e}")


def menu_rechercher(gestion):
    c = gestion.rechercher(lire_entier("Identifiant recherché : "))
    if c is None:
        print("Aucun colis avec cet identifiant.")
    else:
        print(ENTETE)
        print(c)


def menu_organiser(gestion):
    print("Trier par : 1. Poids  2. Valeur  3. Priorité")
    critere = {1: "poids", 2: "valeur", 3: "priorite"}[lire_entier("Choix : ", 1, 3)]
    ordre = lire_entier("Ordre : 1. Croissant  2. Décroissant [1] : ", 1, 2, defaut=1)
    debut = time.perf_counter()
    tries = gestion.trier_par(critere, decroissant=(ordre == 2))
    duree = (time.perf_counter() - debut) * 1000
    afficher_liste(tries)
    print(f"(tri effectué en {duree:.2f} ms)")


def menu_camion(gestion):
    if len(gestion) == 0:
        print("Aucun colis à charger.")
        return None
    capacite = lire_entier("Capacité maximale du camion (kg) [50] : ", 0, defaut=50)
    mode = lire_entier("Critère : 1. Valeur seule  2. Valeur + priorité [2] : ", 1, 2, defaut=2)
    if mode == 2:
        alpha = lire_reel(f"Poids de la priorité alpha [{ALPHA_DEFAUT}] : ", ALPHA_DEFAUT)
        utilite = creer_utilite_priorite(alpha)
    else:
        utilite = utilite_valeur
    debut = time.perf_counter()
    chargement = preparer_camion(gestion.tous(), capacite, utilite)
    duree = (time.perf_counter() - debut) * 1000
    print(f"Chargement calculé en {duree:.1f} ms.")
    afficher_chargement(chargement)
    return chargement


def afficher_chargement(chargement):
    if chargement is None:
        print("Aucun chargement préparé (utilisez l'option 5).")
        return
    print(f"Méthode : {chargement.methode} "
          f"({'solution optimale' if chargement.optimal else 'solution approchée'})")
    afficher_liste(chargement.colis)
    print(f"Poids total  : {chargement.poids_total} / {chargement.capacite} kg")
    print(f"Valeur totale: {chargement.valeur_totale}")
    print(f"Utilité      : {chargement.utilite_totale:.2f}")


def afficher_statistiques(gestion):
    s = gestion.statistiques()
    if s["nombre"] == 0:
        print("Aucun colis.")
        return
    print(f"Nombre de colis : {s['nombre']}")
    print(f"Poids total     : {s['poids_total']} kg (moyenne {s['poids_moyen']:.2f})")
    print(f"Valeur totale   : {s['valeur_totale']} (moyenne {s['valeur_moyenne']:.2f})")
    print("Par priorité    : " + ", ".join(f"{p}: {n}" for p, n in s["par_priorite"].items()))
    print("Par destination : " + ", ".join(f"{d}: {n}" for d, n in s["par_destination"].items()))


def menu_charger(gestion):
    print("1. Exemple de l'énoncé  2. Colis aléatoires  3. Fichier CSV")
    choix = lire_entier("Choix : ", 1, 3)
    nouveaux = GestionColis()
    try:
        if choix == 1:
            nouveaux.ajouter_plusieurs(exemple_enonce())
        elif choix == 2:
            n = lire_entier("Nombre de colis : ", 1)
            nouveaux.ajouter_plusieurs(generer(n, graine=lire_entier("Graine [42] : ", defaut=42)))
        else:
            nouveaux.ajouter_plusieurs(charger_csv(input("Chemin du fichier : ").strip()))
    except (OSError, ValueError, KeyError) as e:
        print(f"Erreur de chargement : {e}")
        return gestion
    print(f"{len(nouveaux)} colis chargés.")
    return nouveaux


def main():
    gestion = GestionColis()
    gestion.ajouter_plusieurs(exemple_enonce())
    chargement = None

    while True:
        print(MENU)
        choix = input("Choix : ").strip()
        if choix == "1":
            afficher_liste(gestion.tous())
        elif choix == "2":
            menu_ajouter(gestion)
        elif choix == "3":
            menu_rechercher(gestion)
        elif choix == "4":
            menu_organiser(gestion)
        elif choix == "5":
            chargement = menu_camion(gestion) or chargement
        elif choix == "6":
            afficher_chargement(chargement)
        elif choix == "7":
            afficher_statistiques(gestion)
        elif choix == "8":
            gestion = menu_charger(gestion)
            chargement = None
        elif choix == "0":
            print("Au revoir.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nAu revoir.")
