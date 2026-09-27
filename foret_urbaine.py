import numpy as np
import pandas as pd

def simuler_foret_nourriciere_urbaine(
    annees=10,
    n_tilleuls=10,
    n_amelanchiers=10,
    prix_kwh=0.10,
    pct_efficacite_batiment=0.15,
    jours_chaleur=100
):
    """
    Simule la valeur thermodynamique et la production biologique d'un bloc d'arbres
    sur une période de maturation (0 à 100% de maturitée sur N ans).
    """
    # Vecteur des années
    ans = np.arange(1, annees + 1)
    
    # Sigmoïde de maturation (croissance biologique lente au début, rapide, puis plateau)
    # À l'année 1: ~10% de maturité; à l'année 10: 100% de maturité
    taux_maturation = 1 / (1 + np.exp(-0.8 * (ans - 5)))
    
    # -------------------------------------------------------------------------
    # 1. PARAMÈTRES PHYSIQUES ET ÉCONOMIQUES (Maturité à 100%)
    # -------------------------------------------------------------------------
    # Constante physique : Chaleur latente de vaporisation (MJ/L)
    delta_H_v = 2.45
    cop_climatiseur = 3.0
    
    # Tilleuls (haute canopée)
    evap_tilleul_max = 400.0          # Litres / jour / arbre mature
    rendement_tilleul_max = 1.5       # kg fleurs séchées / an / arbre mature
    prix_tilleul_kg = 120.0           # $/kg
    
    # Amélanchiers (sous-étage)
    evap_amelanchier_max = 100.0      # Litres / jour / arbre mature
    rendement_amelanchier_max = 8.0   # kg baies / an / arbre mature
    prix_amelanchier_kg = 15.0        # $/kg
    
    # -------------------------------------------------------------------------
    # 2. CALCULS VECTORIELS DYNAMIQUES (Sur N ans)
    # -------------------------------------------------------------------------
    # Évapotranspiration totale annuelle (Litres)
    evap_totale_tilleuls = n_tilleuls * (evap_tilleul_max * jours_chaleur) * taux_maturation
    evap_totale_amelanchiers = n_amelanchiers * (evap_amelanchier_max * jours_chaleur) * taux_maturation
    
    # Conversion thermodynamique -> Équivalent électrique évité (kWh)
    # (Evap * Delta_Hv) / (3.6 MJ par kWh * COP)
    kwh_evites_tilleuls = (evap_totale_tilleuls * delta_H_v) / (3.6 * cop_climatiseur)
    kwh_evites_amelanchiers = (evap_totale_amelanchiers * delta_H_v) / (3.6 * cop_climatiseur)
    
    # Valeur monétaire de la climatisation passive ($)
    valeur_clim_tilleuls = kwh_evites_tilleuls * pct_efficacite_batiment * prix_kwh
    valeur_clim_amelanchiers = kwh_evites_amelanchiers * pct_efficacite_batiment * prix_kwh
    valeur_clim_totale = valeur_clim_tilleuls + valeur_clim_amelanchiers
    
    # Production biologique (kg)
    recolte_tilleuls_kg = n_tilleuls * rendement_tilleul_max * taux_maturation
    recolte_amelanchiers_kg = n_amelanchiers * rendement_amelanchier_max * taux_maturation
    
    # Valeur monétaire de l'usufruit ($)
    valeur_usufruit_tilleuls = recolte_tilleuls_kg * prix_tilleul_kg
    valeur_usufruit_amelanchiers = recolte_amelanchiers_kg * prix_amelanchier_kg
    valeur_usufruit_totale = valeur_usufruit_tilleuls + valeur_usufruit_amelanchiers
    
    # -------------------------------------------------------------------------
    # 3. CONSTRUCTIONS DE LA MATRICE PANDAS
    # -------------------------------------------------------------------------
    df = pd.DataFrame({
        'Année': ans,
        'Maturation (%)': np.round(taux_maturation * 100, 1),
        'Fleurs Tilleul (kg)': np.round(recolte_tilleuls_kg, 2),
        'Baies Amélanchier (kg)': np.round(recolte_amelanchiers_kg, 2),
        'Valeur Usufruit ($)': np.round(valeur_usufruit_totale, 2),
        'kWh Électriques Évités': np.round(kwh_evites_tilleuls + kwh_evites_amelanchiers, 0),
        'Valeur Climatisation ($)': np.round(valeur_clim_totale, 2),
        'Valeur Totale Annuelle ($)': np.round(valeur_usufruit_totale + valeur_clim_totale, 2)
    })
    
    # Cumulatif économique
    df['Valeur Cumulée ($)'] = np.round(df['Valeur Totale Annuelle ($)'].cumsum(), 2)
    
    return df

# Exécution de la simulation
if __name__ == "__main__":
    resultats = simuler_foret_nourriciere_urbaine(
        annees=10,
        n_tilleuls=10,
        n_amelanchiers=10,
        prix_kwh=0.10,
        pct_efficacite_batiment=0.15,
        jours_chaleur=100
    )
    
    # Affichage de la matrice tabulaire
    print(resultats.to_string(index=False))
