#!/usr/bin/env python3
"""
Gold Card NARP — Moteur computationnel comptable.

Distinction stricte entre :
- cash encaissé (trésorerie)
- produit constaté d'avance (passif)
- revenu comptable reconnu (à mesure de la prestation)
- gain sur impayés évités (économie, PAS une recette)
- capacité d'examens consommée
- résultat économique net
"""
from dataclasses import dataclass
from enum import Enum


class Statut(str, Enum):
    P = "PROPOSE"
    P_VERIFIE = "VERIFIE"
    C = "CALCULE"
    M = "MODELE"


@dataclass(frozen=True)
class ScenarioGoldCard:
    nom: str
    taux_conversion: float
    impayes_evites: float


@dataclass(frozen=True)
class ParametresGoldCard:
    prix_card: float = 5_000.0
    examens_par_card: int = 4
    prospects_par_grappe: int = 500
    nombre_grappes: int = 10
    enveloppe_marketing: float = 0.0
    # Taux de reconnaissance du revenu en an 1
    # (le reste est produit constaté d'avance, reconnu en N+1)
    taux_reconnaissance_an1: float = 0.70


class GoldCardEngine:
    def __init__(self, params, scenarios):
        self.p = params
        self.scenarios = scenarios

    def calcul_grappe(self, scenario):
        cartes = round(self.p.prospects_par_grappe * scenario.taux_conversion)
        examens = cartes * self.p.examens_par_card
        cash = cartes * self.p.prix_card
        gain_impayes = cash * scenario.impayes_evites

        # Comptabilité : distinction cash / produit constaté d'avance / revenu reconnu
        cash_encaisse = cash
        revenu_reconnu_an1 = cash * self.p.taux_reconnaissance_an1
        produit_constate_avance = cash - revenu_recondu_an1 if False else cash - revenu_reconnu_an1

        return {
            "scenario": scenario.nom,
            "prospects": self.p.prospects_par_grappe,
            "cartes": cartes,
            "examens_inclus": examens,
            "cash_encaisse_avance": cash_encaisse,
            "revenu_reconnu_an1": revenu_reconnu_an1,
            "produit_constate_avance": produit_constate_avance,
            "gain_impayes_evites": gain_impayes,
            "revenu_economique_securise": revenu_reconnu_an1 + gain_impayes,
            "statut": Statut.C.value,
        }

    def calcul_reseau(self, scenario):
        g = self.calcul_grappe(scenario)
        total = dict(g)
        for key in [
            "prospects", "cartes", "examens_inclus",
            "cash_encaisse_avance", "revenu_reconnu_an1",
            "produit_constate_avance", "gain_impayes_evites",
            "revenu_economique_securise",
        ]:
            total[key] *= self.p.nombre_grappes

        total["enveloppe_marketing"] = self.p.enveloppe_marketing
        total["impact_economique_net"] = (
            total["revenu_economique_securise"] - self.p.enveloppe_marketing
        )
        return total

    def prix_unitaire_examen(self):
        return self.p.prix_card / self.p.examens_par_card

    def tableau(self):
        return [self.calcul_reseau(s) for s in self.scenarios]


if __name__ == "__main__":
    scenarios = [
        ScenarioGoldCard("Pessimiste", 0.30, 0.08),
        ScenarioGoldCard("Central", 0.60, 0.10),
        ScenarioGoldCard("Optimiste", 0.85, 0.12),
    ]
    params = ParametresGoldCard(
        prix_card=5_000, examens_par_card=4,
        prospects_par_grappe=500, nombre_grappes=10,
        enveloppe_marketing=0.0, taux_reconnaissance_an1=0.70,
    )
    engine = GoldCardEngine(params, scenarios)

    print(f"Prix unitaire / examen : {engine.prix_unitaire_examen():,.0f} $")
    print()
    for ligne in engine.tableau():
        print(f"=== Scénario {ligne['scenario']} (10 grappes) ===")
        print(f"  Cartes vendues          : {ligne['cartes']:,}")
        print(f"  Examens inclus          : {ligne['examens_inclus']:,}")
        print(f"  Cash encaissé (J0)      : {ligne['cash_encaisse_avance']:,.0f} $")
        print(f"  Revenu reconnu an 1     : {ligne['revenu_reconnu_an1']:,.0f} $")
        print(f"  Produit constaté avance : {ligne['produit_constate_avance']:,.0f} $")
        print(f"  Gain impayés évités     : {ligne['gain_impayes_evites']:,.0f} $")
        print(f"  Revenu éco. sécurisé    : {ligne['revenu_economique_securise']:,.0f} $")
        print(f"  Impact net              : {ligne['impact_economique_net']:,.0f} $")
        print()
