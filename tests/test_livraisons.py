"""Tests unitaires. Lancement : python3 -m unittest discover tests"""

import itertools
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from camion import preparer_camion, sac_a_dos_dp, sac_a_dos_glouton  # noqa: E402
from colis import Colis  # noqa: E402
from donnees import exemple_enonce, generer  # noqa: E402
from gestion import GestionColis  # noqa: E402
from priorite import creer_utilite_priorite  # noqa: E402
from tri import tri_fusion  # noqa: E402


def force_brute(colis, capacite, utilite):
    """Teste les 2^n combinaisons : référence pour les petits n."""
    meilleur = 0
    for r in range(len(colis) + 1):
        for combi in itertools.combinations(colis, r):
            if sum(c.poids for c in combi) <= capacite:
                meilleur = max(meilleur, sum(utilite(c) for c in combi))
    return meilleur


class TestTri(unittest.TestCase):
    def test_tri_fusion_identique_a_sorted(self):
        rng = random.Random(1)
        for n in [0, 1, 2, 7, 100, 1001]:
            donnees = [rng.randint(0, 50) for _ in range(n)]
            self.assertEqual(tri_fusion(donnees), sorted(donnees))
            self.assertEqual(tri_fusion(donnees, decroissant=True), sorted(donnees, reverse=True))

    def test_tri_stable(self):
        colis = generer(500)
        attendu = sorted(colis, key=lambda c: c.priorite)  # sorted() est stable
        self.assertEqual(tri_fusion(colis, lambda c: c.priorite), attendu)


class TestGestion(unittest.TestCase):
    def setUp(self):
        self.g = GestionColis()
        self.g.ajouter_plusieurs(exemple_enonce())

    def test_recherche(self):
        self.assertEqual(self.g.rechercher(103).destination, "Lyon")
        self.assertIsNone(self.g.rechercher(999))

    def test_doublon_refuse(self):
        with self.assertRaises(ValueError):
            self.g.ajouter(Colis(101, 1, 1, 1, "Nice"))

    def test_tri_par_valeur_et_cache_invalide(self):
        self.assertEqual([c.id for c in self.g.trier_par("valeur")], [102, 105, 101, 104, 103])
        self.g.ajouter(Colis(106, 1, 1, 1, "Nice"))
        self.assertEqual(self.g.trier_par("valeur")[0].id, 106)

    def test_priorite_invalide(self):
        with self.assertRaises(ValueError):
            Colis(1, 1, 1, 9, "Paris")


class TestCamion(unittest.TestCase):
    def test_exemple_enonce(self):
        # A(8,20) B(6,25) C(5,18) D(4,14) ; capacité 15 -> B + C + D = 57
        colis = [Colis(1, 8, 20, 5, "A"), Colis(2, 6, 25, 1, "B"),
                 Colis(3, 5, 18, 4, "C"), Colis(4, 4, 14, 3, "D")]
        ch = sac_a_dos_dp(colis, 15)
        self.assertEqual(ch.valeur_totale, 57)
        self.assertEqual(sorted(c.id for c in ch.colis), [2, 3, 4])

    def test_dp_optimal_contre_force_brute(self):
        for graine in range(30):
            colis = generer(10, graine=graine, poids_max=15)
            for utilite in (lambda c: c.valeur, creer_utilite_priorite(1.0)):
                ch = sac_a_dos_dp(colis, 30, utilite)
                self.assertAlmostEqual(ch.utilite_totale, force_brute(colis, 30, utilite))
                self.assertLessEqual(ch.poids_total, 30)
                self.assertAlmostEqual(ch.utilite_totale, sum(utilite(c) for c in ch.colis))

    def test_glouton_non_optimal(self):
        # Le glouton prend A (meilleur ratio) et ne peut plus prendre B ni C.
        colis = [Colis(1, 1, 2, 1, "A"), Colis(2, 10, 10, 1, "B"), Colis(3, 10, 10, 1, "C")]
        self.assertEqual(sac_a_dos_glouton(colis, 20).valeur_totale, 12)
        self.assertEqual(sac_a_dos_dp(colis, 20).valeur_totale, 20)

    def test_glouton_respecte_capacite(self):
        colis = generer(1000)
        self.assertLessEqual(sac_a_dos_glouton(colis, 100).poids_total, 100)

    def test_bascule_glouton(self):
        self.assertFalse(preparer_camion(generer(100), 50, limite=10).optimal)
        self.assertTrue(preparer_camion(generer(100), 50).optimal)

    def test_priorite_change_selection(self):
        colis = [Colis(1, 10, 30, 1, "X"), Colis(2, 10, 25, 5, "Y")]
        self.assertEqual(sac_a_dos_dp(colis, 10).colis[0].id, 1)
        self.assertEqual(sac_a_dos_dp(colis, 10, creer_utilite_priorite(1.0)).colis[0].id, 2)


if __name__ == "__main__":
    unittest.main()
