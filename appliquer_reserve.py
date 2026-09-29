#!/usr/bin/env python3
"""
Ajoute la mention de reserve aux pages HTML autonomes.
Ignore : chapitres de livres, fragments structurels, pages deja conformes.
"""
from pathlib import Path

RACINE = Path(".")

# Pages a ignorer (fragments structurels ou chapitres)
IGNORES = {
    "logo.html", "bloc_dashboard.html", "section_corrigee.html",
    "encart_section14.html", "index.html",  # index traite separement
}

# Chapitres de livres (commencent par un chiffre + _livre)
def est_chapitre(nom):
    return nom[:2].isdigit() and "_livre" in nom.lower()

# Pages deja conformes
def a_deja_mention(contenu):
    return "non opposable" in contenu or "non adopté" in contenu

MENTION = '''
<footer class="reserve-juridique">
  <p><strong>Réserve juridique :</strong> Ce dossier demeure
  <strong>non adopté</strong>, <strong>non opérationnel</strong> et
  <strong>non opposable</strong>. Les corrections documentées sont des
  corrections internes, sans engagement de tiers.</p>
</footer>
'''

def injecter(chemin):
    contenu = chemin.read_text(encoding="utf-8")
    if a_deja_mention(contenu):
        return False
    # Inserer avant </body>
    if "</body>" in contenu:
        contenu = contenu.replace("</body>", MENTION + "</body>", 1)
        chemin.write_text(contenu, encoding="utf-8")
        return True
    return False

modifies = []
for f in sorted(RACINE.glob("*.html")):
    if f.name in IGNORES or est_chapitre(f.name):
        continue
    try:
        if injecter(f):
            modifies.append(f.name)
    except Exception as e:
        print(f"  Erreur {f.name} : {e}")

print(f"Pages modifiees : {len(modifies)}")
for m in modifies:
    print(f"  + {m}")
