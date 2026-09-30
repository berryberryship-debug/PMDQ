#!/bin/bash
echo "=== AUDIT VISUEL ==="
python audit_visuel.py
echo ""
echo "=== EMPREINTE ==="
python -c "import json; e=json.load(open('data/empreinte_pmdq.json')); print('Version :', e['version']); print('Ratio D moyen :', e['invariants_numeriques']['ratio_D_moyen']); print('Decaisse :', e['invariants_numeriques']['decaisse_total_G'], 'G\$'); print('Ruptures doc. :', len(e['ruptures_documentees']))"
echo ""
echo "=== ARCHIVE ==="
ls _archive_20260930/ | wc -l
echo "fichiers archives"
