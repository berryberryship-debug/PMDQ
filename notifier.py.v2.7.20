#!/usr/bin/env python3
"""
notifier.py — Envoi d'alertes PMDQ
v2.7.20

Trois canaux, tous optionnels :
    - Journal local : sources/alertes.log (toujours actif)
    - Discord webhook : env PMDQ_NOTIF_DISCORD_URL
    - Telegram bot   : env PMDQ_NOTIF_TELEGRAM_TOKEN + PMDQ_NOTIF_TELEGRAM_CHAT

Usage :
    python3 notifier.py --titre "SOCLE KO" --message "3 moteurs en echec"
    echo "details" | python3 notifier.py --titre "..." --stdin
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path


JOURNAL = Path("sources/alertes.log")


def journal_local(titre, message, niveau="ALERTE"):
    """Ajoute une entree horodatee au journal local."""
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    ligne = f"[{datetime.now().isoformat(timespec='seconds')}] {niveau} | {titre}\n"
    if message:
        for l in message.split("\n"):
            if l.strip():
                ligne += f"    {l}\n"
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(ligne + "\n")
    return True


def envoyer_discord(url, titre, message, niveau):
    """Envoie un message vers un webhook Discord."""
    couleur = 15548997 if niveau == "ALERTE" else 3066993
    payload = {
        "embeds": [{
            "title": titre[:250],
            "description": (message or "(vide)")[:4000],
            "color": couleur,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "footer": {"text": "PMDQ socle"},
        }]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "User-Agent": "PMDQ/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return 200 <= r.status < 300
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return False


def envoyer_telegram(token, chat_id, titre, message):
    """Envoie un message via un bot Telegram."""
    texte = f"*{titre}*\n\n{message}" if message else f"*{titre}*"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": texte,
        "parse_mode": "Markdown",
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "PMDQ/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return 200 <= r.status < 300
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Notifier PMDQ")
    parser.add_argument("--titre", type=str, required=True)
    parser.add_argument("--message", type=str, default="")
    parser.add_argument("--niveau", type=str, default="ALERTE",
                        choices=["ALERTE", "INFO"])
    parser.add_argument("--stdin", action="store_true",
                        help="Lit le message depuis stdin")
    args = parser.parse_args()

    message = args.message
    if args.stdin:
        message = sys.stdin.read().strip()

    resultats = []

    # 1. Journal local (toujours)
    journal_local(args.titre, message, args.niveau)
    resultats.append(("journal", True))

    # 2. Discord (optionnel)
    url_discord = os.environ.get("PMDQ_NOTIF_DISCORD_URL")
    if url_discord:
        ok = envoyer_discord(url_discord, args.titre, message, args.niveau)
        resultats.append(("discord", ok))

    # 3. Telegram (optionnel)
    token = os.environ.get("PMDQ_NOTIF_TELEGRAM_TOKEN")
    chat = os.environ.get("PMDQ_NOTIF_TELEGRAM_CHAT")
    if token and chat:
        ok = envoyer_telegram(token, chat, args.titre, message)
        resultats.append(("telegram", ok))

    # 4. Resume
    echecs = [c for c, ok in resultats if not ok]
    for canal, ok in resultats:
        marque = "OK" if ok else "ECHEC"
        print(f"  notifier.{canal:<10} {marque}")
    if echecs:
        print(f"Canaux en echec : {', '.join(echecs)}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
