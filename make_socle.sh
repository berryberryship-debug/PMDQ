#!/bin/bash
# make_socle.sh — Regenere etat_variables.json et verifie les moteurs.
set -u
cd "$(dirname "$0")"

echo "=== 1. Regeneration de l'etat des variables ==="
python3 ecrire_etat.py || { echo "ECHEC ecrire_etat.py"; exit 1; }

echo
echo "=== 2. Resume de l'etat ==="
python3 - <<'PY'
import json
etat = json.loads(open("sources/etat_variables.json", encoding="utf-8").read())
r = etat["resume"]
print(f"  Total     : {r['total']}")
print(f"  A jour    : {r['a_jour']}")
print(f"  En retard : {r['en_retard']}")
print(f"  A revoir  : {r['a_revoir']}")
print(f"  Absentes  : {r['section_absente']}")
PY

echo
echo "=== 3. Verification des moteurs ==="
moteurs=(
    "moteur_variables.py:"
    "moteur_domar.py:"
    "moteur_fiscal.py:"
    "moteur_dgeq.py:--demo"
    "moteur_etancheite.py:"
    "moteur_provisionnement.py:"
    "moteur_rendement.py:"
    "moteur_vehicule.py:"
)

ok=0
ko=0
for entree in "${moteurs[@]}"; do
    nom="${entree%%:*}"
    args="${entree#*:}"
    if python3 "$nom" $args > /dev/null 2>&1; then
        printf "  OK    %s\n" "$nom"
        ok=$((ok+1))
    else
        code=$?
        printf "  ECHEC %s (code %d)\n" "$nom" "$code"
        ko=$((ko+1))
    fi
done

echo
echo "  Bilan : $ok OK, $ko ECHEC"
exit $ko
