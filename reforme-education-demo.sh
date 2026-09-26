#!/data/data/com.termux/files/usr/bin/bash
# Simulation réforme éducation — modèle cohorte/flux v4
set -euo pipefail

# --- Paramètres ---
PRIM_TOTAL=682000
SEC_TOTAL=460000
CEGEP_GEN=90000
PRIM_AV=6
PRIM_AP=7
SEC_AV=5
SEC_AP=4
HORIZON=12

OUTPUT_DIR="output"
mkdir -p "$OUTPUT_DIR"

# Cohortes
COH_PRIM_AV=$((PRIM_TOTAL / PRIM_AV))     # 113666
COH_PRIM_AP=$((PRIM_TOTAL / PRIM_AP))     # 97428
COH_SEC_AV=$((SEC_TOTAL / SEC_AV))        # 92000
COH_SEC_AP=$((SEC_TOTAL / SEC_AP))        # 115000

# Pic transitoire primaire (6 anciennes cohortes + 1 nouvelle taille ancienne)
PRIM_PEAK=$((COH_PRIM_AV * PRIM_AP))      # 795662

echo "=== RÉFORME ÉDUCATION — SIMULATION DÉMOGRAPHIQUE v4 ==="
echo
echo "[Cohortes]"
echo "  Primaire  : $COH_PRIM_AV → $COH_PRIM_AP  ($((COH_PRIM_AP - COH_PRIM_AV)))"
echo "  Secondaire: $COH_SEC_AV → $COH_SEC_AP  (+$((COH_SEC_AP - COH_SEC_AV)))"
echo
echo "[Pic transitoire primaire] $PRIM_TOTAL → $PRIM_PEAK  (+$((PRIM_PEAK - PRIM_TOTAL)), +16.6%)"
echo "[Stock primaire plein régime] $PRIM_TOTAL (retour équilibre)"
echo "[Stock secondaire plein régime] $SEC_TOTAL (constant)"
echo

OUT_CSV="${OUTPUT_DIR}/reforme_education_demo_v4.csv"
echo "annee,stock_primaire,stock_secondaire,flux_univ_cumule,phase" > "$OUT_CSV"

printf "%4s %14s %14s %14s %s\n" "An" "Stock prim." "Stock sec." "Flux univ" "Phase"

for annee in $(seq 0 $HORIZON); do
  if [ "$annee" -eq 0 ]; then
    STOCK_P=$PRIM_TOTAL
    STOCK_S=$SEC_TOTAL
    FLUX=0
    PHASE="État initial"

  elif [ "$annee" -le 6 ]; then
    # Transition primaire : interpolation linéaire vers le pic
    RATIO=$(awk "BEGIN{r=$annee/6; if(r>1)r=1; printf \"%.4f\", r}")
    STOCK_P=$(awk "BEGIN{printf \"%d\", $PRIM_TOTAL + ($PRIM_PEAK - $PRIM_TOTAL) * $RATIO}")
    # Secondaire stable pendant la transition primaire
    STOCK_S=$SEC_TOTAL
    # Flux université graduel : commence An 5
    if [ "$annee" -ge 5 ]; then
      FLUX=$((CEGEP_GEN / 2 * (annee - 4) / 6))
    else
      FLUX=0
    fi
    PHASE="Transition (${annee}/6)"

  elif [ "$annee" -le 10 ]; then
    # Détransition primaire : retour progressif vers plein régime
    DECROISSANCE=$((annee - 6))
    RATIO=$(awk "BEGIN{r=$DECROISSANCE/4; if(r>1)r=1; printf \"%.4f\", r}")
    STOCK_P=$(awk "BEGIN{printf \"%d\", $PRIM_PEAK - ($PRIM_PEAK - $PRIM_TOTAL) * $RATIO}")
    # Secondaire : ajustement progressif vers plein régime
    STOCK_S=$(awk "BEGIN{printf \"%d\", $SEC_TOTAL * (1 - 0.15 * $RATIO)}")
    FLUX=$((CEGEP_GEN / 2))
    PHASE="Détransition (${DECROISSANCE}/4)"

  else
    # Plein régime stabilisé
    STOCK_P=$PRIM_TOTAL
    STOCK_S=$SEC_TOTAL
    FLUX=$((CEGEP_GEN / 2))
    PHASE="Plein régime"
  fi

  printf "%4d %14d %14d %14d %s\n" "$annee" "$STOCK_P" "$STOCK_S" "$FLUX" "$PHASE"
  echo "$annee,$STOCK_P,$STOCK_S,$FLUX,$PHASE" >> "$OUT_CSV"
done

echo
echo "CSV exporté : $OUT_CSV"
