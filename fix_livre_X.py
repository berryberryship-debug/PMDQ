#!/usr/bin/env python3
"""Retire les 2 </div> orphelins de livre_X_justice.html."""
from pathlib import Path

FICHIER = Path("livre_X_justice.html")
lignes = FICHIER.read_text(encoding="utf-8").splitlines(keepends=True)

Path("livre_X_justice.html.bak_20260930").write_text(
    "".join(lignes), encoding="utf-8"
)
print("[OK] Sauvegarde : livre_X_justice.html.bak_20260930")


trouve = False
for i in range(len(lignes) - 3):
    if (lignes[i].strip() == "</div>"
            and lignes[i + 1].strip() == "</div>"
            and lignes[i + 2].strip() == "</main>"):
        del lignes[i + 1]
        del lignes[i]
        FICHIER.write_text("".join(lignes), encoding="utf-8")
        print("[OK] 2 </div> orphelins retires (lignes " + str(i + 1) + " et " + str(i + 2) + ")")
        trouve = True
        break

if not trouve:
    print("[ATTENTION] Motif </div></div></main> non trouve")
    print("Verifie manuellement les lignes 120-130")
