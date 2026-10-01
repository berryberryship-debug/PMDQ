#!/usr/bin/env python3
"""Couche unifiée BoC + FRED + yfinance. Lecture par cache local CSV."""
import json
import os
from pathlib import Path

import pandas as pd

CACHE_DIR = Path("/data/data/com.termux/files/home/pmdq_data/cache_pmdq")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class MarketData:
    def __init__(self, cache_dir=CACHE_DIR):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _load(self, key):
        data_path = self.cache_dir / f"{key}.csv"
        meta_path = self.cache_dir / f"{key}_meta.json"
        if not data_path.exists():
            raise FileNotFoundError(
                f"'{key}' absent du cache.\n"
                f"Lancer : python boc_extractor.py --only {key}"
            )
        df = pd.read_csv(data_path, parse_dates=["date"])
        meta = {}
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return df, meta

    def get_value(self, key, as_of=None, return_meta=False):
        df, meta = self._load(key)
        if as_of:
            df = df[df["date"] <= pd.Timestamp(as_of)]
        if df.empty:
            raise ValueError(f"Aucune observation pour {key}")
        value = float(df["value"].iloc[-1])
        if return_meta:
            meta = dict(meta)
            meta["value_date"] = str(df["date"].iloc[-1].date())
            meta["value"] = value
            return value, meta
        return value

    def get_series(self, key, start=None, end=None):
        df, _ = self._load(key)
        if start:
            df = df[df["date"] >= pd.Timestamp(start)]
        if end:
            df = df[df["date"] <= pd.Timestamp(end)]
        return df.reset_index(drop=True)

    def get_meta(self, key):
        _, meta = self._load(key)
        return meta

    def list_available(self):
        return sorted(p.stem for p in self.cache_dir.glob("*.csv"))

    def summary(self):
        rows = []
        for key in self.list_available():
            try:
                meta = self.get_meta(key)
                rows.append({
                    "variable": key,
                    "last_value": meta.get("last_value"),
                    "last_date": meta.get("last_date"),
                    "unit": meta.get("unit"),
                    "source": meta.get("source"),
                })
            except Exception as e:
                rows.append({"variable": key, "error": str(e)})
        return pd.DataFrame(rows)

    def update_boc(self, key, recent=90):
        from boc_extractor import update_one
        return update_one(key, recent=recent)



    def update_statcan(self, key, latest_n=24):
        """Déclenche la mise à jour d'une série StatCan."""
        from statcan_extractor import update_one
        return update_one(key, latest_n=latest_n)

if __name__ == "__main__":
    md = MarketData()
    print("Variables en cache :", md.list_available() or "aucune")
    for key in md.list_available():
        try:
            v, meta = md.get_value(key, return_meta=True)
            print(f"  {key:28s} : {v:>8.3f} {meta.get('unit', '')}  ({meta.get('value_date')})")
        except Exception as e:
            print(f"  {key:28s} : ERREUR - {e}")
