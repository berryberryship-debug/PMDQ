#!/usr/bin/env python3
"""audit_visuel.py -- Detecte les anomalies visuelles dans les .html."""
import re
from pathlib import Path

RACINE = Path(__file__).parent

PROBLEMES = {
    "no_viewport": "Balise <meta viewport> absente (mobile casse)",
    "no_charset": "Charset UTF-8 non declare",
    "no_title": "Balise <title> absente ou vide",
    "no_lang": "Attribut lang absent sur <html>",
    "short_page": "Page tres courte (< 500 octets)",
    "broken_href": "Lien local casse",
    "broken_css": "Fichier CSS reference introuvable",
    "dup_id": "ID HTML duplique",
    "mojibake": "Encodage suspect (caracteres casses)",
    "broken_img": "Image referencee introuvable",
    "no_alt": "Attribut alt manquant sur <img>",
    "suspect_url": "URL externe suspecte (typo probable)",
    "unclosed_tag": "Balise HTML probablement non fermee",
}

PROTO_OK = ("http://", "https://", "mailto:", "tel:", "//",
            "javascript:", "data:", "#")


def est_fragment(contenu, taille):
    if taille >= 500:
        return False
    return not re.search(r"<(html|body|head)\b", contenu, re.I)


def liste_html():
    return sorted(RACINE.glob("*.html"))


def analyse_page(f, contenu, taille, fragment):
    anomalies = []
    if not fragment and taille < 500:
        anomalies.append(("short_page", str(taille) + " octets"))
    if not fragment:
        if "charset" not in contenu.lower():
            anomalies.append(("no_charset", ""))
        if 'name="viewport"' not in contenu.lower():
            anomalies.append(("no_viewport", ""))
        m = re.search(r"<title[^>]*>(.*?)</title>", contenu, re.I | re.S)
        if not m or not m.group(1).strip():
            anomalies.append(("no_title", ""))
        if not re.search(r"<html[^>]*\blang=", contenu, re.I):
            anomalies.append(("no_lang", ""))
    return anomalies


def analyse_liens(f, contenu):
    anomalies = []
    for m in re.finditer(r'href=["\']([^"\']*)["\']', contenu, re.I):
        cible = m.group(1)
        if not cible or cible.startswith(PROTO_OK):
            continue
        chemin = (f.parent / cible.split("#")[0].split("?")[0]).resolve()
        if not chemin.exists():
            anomalies.append(("broken_href", cible))
    return anomalies


def analyse_css(f, contenu):
    anomalies = []
    for m in re.finditer(r'<link[^>]*href=["\']([^"\']+\.css)["\']', contenu, re.I):
        cible = m.group(1)
        if cible.startswith(("http://", "https://", "//")):
            continue
        chemin = (f.parent / cible).resolve()
        if not chemin.exists():
            anomalies.append(("broken_css", cible))
    return anomalies


def analyse_ids(contenu):
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', contenu, re.I)
    vus = set()
    anomalies = []
    for i in ids:
        if i in vus:
            anomalies.append(("dup_id", i))
        vus.add(i)
    return anomalies


def analyse_images(f, contenu):
    """Detecte : images referencees mais absentes + <img> sans alt."""
    anomalies = []
    for m in re.finditer(r'<img\b([^>]*)>', contenu, re.I):
        attrs = m.group(1)
        # alt manquant
        if not re.search(r'\balt\s*=', attrs, re.I):
            src_m = re.search(r'\bsrc=["\']([^"\']+)["\']', attrs, re.I)
            cible = src_m.group(1) if src_m else "(sans src)"
            anomalies.append(("no_alt", cible))
        # src casse
        src_m = re.search(r'\bsrc=["\']([^"\']+)["\']', attrs, re.I)
        if src_m:
            cible = src_m.group(1)
            if cible.startswith(PROTO_OK):
                continue
            chemin = (f.parent / cible.split("?")[0]).resolve()
            if not chemin.exists():
                anomalies.append(("broken_img", cible))
    return anomalies


def analyse_urls_externes(contenu):
    """Detecte les typos probables dans les URLs externes."""
    anomalies = []
    # http:/ au lieu de http://
    for m in re.finditer(r'https?:/(?!/)', contenu, re.I):
        extrait = contenu[max(0, m.start() - 10):m.end() + 30].strip()
        anomalies.append(("suspect_url", extrait))
    # ww. au lieu de www.
    for m in re.finditer(r'["\']https?://ww\.(?!ww)', contenu, re.I):
        extrait = contenu[m.start():m.end() + 30].strip()
        anomalies.append(("suspect_url", extrait))
    return anomalies


def analyse_tags(contenu):
    """Detecte les balises HTML probablement non fermees (heuristique)."""
    anomalies = []
    paires = ["div", "section", "article", "main", "aside", "header", "footer", "nav"]
    texte = re.sub(r"<script[^>]*>.*?</script>", "", contenu, flags=re.I | re.S)
    texte = re.sub(r"<style[^>]*>.*?</style>", "", texte, flags=re.I | re.S)
    texte = re.sub(r"<!--.*?-->", "", texte, flags=re.S)
    for tag in paires:
        ouvrants = len(re.findall(r"<" + tag + r"\b[^>]*>", texte, re.I))
        fermants = len(re.findall(r"</" + tag + r"\s*>", texte, re.I))
        if ouvrants != fermants:
            anomalies.append(("unclosed_tag", tag + " : " + str(ouvrants) + " ouverts / " + str(fermants) + " fermes"))
    return anomalies


def main():
    fichiers = liste_html()
    print("=" * 72)
    print("AUDIT VISUEL -- " + str(len(fichiers)) + " fichiers HTML")
    print("=" * 72)

    total = 0
    ok = []
    fragments = []
    ko = []

    for f in fichiers:
        try:
            contenu = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            ko.append((f.name, [("mojibake", "Lecture echouee")]))
            continue
        taille = len(contenu)
        frag = est_fragment(contenu, taille)
        if frag:
            fragments.append(f.name)
            continue
        anomalies = []
        anomalies.extend(analyse_page(f, contenu, taille, frag))
        anomalies.extend(analyse_liens(f, contenu))
        anomalies.extend(analyse_css(f, contenu))
        anomalies.extend(analyse_ids(contenu))
        anomalies.extend(analyse_images(f, contenu))
        anomalies.extend(analyse_urls_externes(contenu))
        anomalies.extend(analyse_tags(contenu))
        if anomalies:
            ko.append((f.name, anomalies))
            total += len(anomalies)
        else:
            ok.append(f.name)

    for nom, anomalies in ko:
        print("\n[" + nom + "]")
        par_type = {}
        for code, detail in anomalies:
            par_type.setdefault(code, []).append(detail)
        for code, details in par_type.items():
            print("  - " + PROBLEMES.get(code, code))
            for d in details[:3]:
                if d:
                    print("      " + d)
            if len(details) > 3:
                print("      ... +" + str(len(details) - 3) + " autres")

    print("\n" + "=" * 72)
    print("RESUME")
    print("=" * 72)
    print("Pages sans probleme  : " + str(len(ok)))
    print("Fragments ignores    : " + str(len(fragments)))
    print("Pages avec anomalies : " + str(len(ko)))
    print("Total anomalies      : " + str(total))
    print("=" * 72)


if __name__ == "__main__":
    main()
