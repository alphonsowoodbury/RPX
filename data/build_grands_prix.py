#!/usr/bin/env python3
"""
Rees — F1 Grands Prix dataset builder (v1)

Builds the foundational dataset: every Formula 1 World Championship Grand Prix
(1950 -> present), with race winner and pole position / qualifying P1.

Source: Jolpica F1 API (Ergast-compatible successor). https://api.jolpi.ca/

Strategy (rate-limit friendly, ~30-40 requests total):
  1. /results/1        -> every race WINNER across all history (defines race universe)
  2. /grid/1/results   -> every FRONT-ROW STARTER (grid P1) across all history  -> pole proxy
  3. /qualifying/1     -> true QUALIFYING P1 (pole), reliable from 2003 onward   -> preferred pole

Pole resolution: use qualifying P1 where available (2003+), else grid P1.
Outputs CSV + SQLite to /Volumes/F1/data/.
"""
import json
import time
import sqlite3
import urllib.request
from pathlib import Path

import pandas as pd

BASE = "https://api.jolpi.ca/ergast/f1"
OUT = Path("/Volumes/F1/data")
RAW = OUT / "raw"
PAGE = 100          # Jolpica max page size
SLEEP = 0.4         # be polite to the API


def fetch_all(path: str) -> list:
    """Paginate an Ergast-style endpoint, returning the full Races[] list."""
    races, offset, total = [], 0, None
    while True:
        url = f"{BASE}/{path}.json?limit={PAGE}&offset={offset}"
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=30) as r:
                    data = json.load(r)
                break
            except Exception as e:  # transient network / rate limit
                if attempt == 3:
                    raise
                print(f"   retry {attempt+1} ({e})")
                time.sleep(2 * (attempt + 1))
        mr = data["MRData"]
        total = int(mr["total"])
        batch = mr["RaceTable"]["Races"]
        races.extend(batch)
        offset += PAGE
        print(f"   {path}: {len(races)}/{total}")
        if offset >= total:
            break
        time.sleep(SLEEP)
    return races


def load_or_fetch(path: str, cache: str) -> list:
    """Use cached raw JSON if present, else fetch and cache it."""
    f = RAW / cache
    if f.exists():
        print(f"   (cache) {cache}")
        return json.loads(f.read_text())
    data = fetch_all(path)
    f.write_text(json.dumps(data))
    return data


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    print("[1/3] Race winners (position 1, all seasons)...")
    winners_raw = load_or_fetch("results/1", "winners.json")

    print("[2/3] Front-row starters (grid 1, all seasons)...")
    grid_raw = load_or_fetch("grid/1/results", "grid1.json")

    print("[3/3] Qualifying P1 (pole, 2003+ reliable)...")
    quali_raw = load_or_fetch("qualifying/1", "qualifying1.json")

    # ---- Build master table from winners (defines the race universe) ----
    def driver_name(d):
        return f"{d['givenName']} {d['familyName']}".strip()

    rows = []
    for race in winners_raw:
        res = race["Results"][0]
        drv, con = res["Driver"], res["Constructor"]
        circ = race["Circuit"]
        loc = circ["Location"]
        rows.append({
            "season": int(race["season"]),
            "round": int(race["round"]),
            "date": race.get("date"),
            "raceName": race["raceName"],
            "circuitId": circ["circuitId"],
            "circuitName": circ["circuitName"],
            "country": loc.get("country"),
            "locality": loc.get("locality"),
            "lat": loc.get("lat"),
            "long": loc.get("long"),
            "winnerDriverId": drv["driverId"],
            "winnerDriver": driver_name(drv),
            "winnerNationality": drv.get("nationality"),
            "winnerConstructorId": con["constructorId"],
            "winnerConstructor": con["name"],
            "winnerGrid": int(res["grid"]) if res.get("grid") else None,
        })
    df = pd.DataFrame(rows).sort_values(["season", "round"]).reset_index(drop=True)

    # ---- Pole from grid==1 (all years) ----
    grid_pole = {}
    for race in grid_raw:
        res = race["Results"][0]
        grid_pole[(int(race["season"]), int(race["round"]))] = {
            "poleDriverId": res["Driver"]["driverId"],
            "poleDriver": driver_name(res["Driver"]),
            "poleConstructor": res["Constructor"]["name"],
            "poleSource": "grid",
        }

    # ---- Pole from qualifying==1 (preferred, 2003+) ----
    quali_pole = {}
    for race in quali_raw:
        q = race["QualifyingResults"][0]
        quali_pole[(int(race["season"]), int(race["round"]))] = {
            "poleDriverId": q["Driver"]["driverId"],
            "poleDriver": driver_name(q["Driver"]),
            "poleConstructor": q["Constructor"]["name"],
            "poleSource": "qualifying",
        }

    def resolve_pole(row):
        key = (row["season"], row["round"])
        p = quali_pole.get(key) or grid_pole.get(key) or {
            "poleDriverId": None, "poleDriver": None,
            "poleConstructor": None, "poleSource": None,
        }
        return pd.Series(p)

    df = pd.concat([df, df.apply(resolve_pole, axis=1)], axis=1)
    df["poleWon"] = (df["winnerDriverId"] == df["poleDriverId"]).astype("boolean")
    df.loc[df["poleDriverId"].isna(), "poleWon"] = pd.NA

    # ---- Write outputs ----
    csv_path = OUT / "grands_prix.csv"
    df.to_csv(csv_path, index=False)

    db_path = OUT / "f1.sqlite"
    with sqlite3.connect(db_path) as con:
        df.to_sql("grands_prix", con, if_exists="replace", index=False)

    # ---- Summary ----
    n = len(df)
    seasons = f"{df.season.min()}-{df.season.max()}"
    pole_known = df["poleDriver"].notna().sum()
    pole_win_rate = df["poleWon"].dropna().mean()
    print("\n=== BUILD COMPLETE ===")
    print(f"Grands Prix : {n}  ({seasons}, {df.season.nunique()} seasons)")
    print(f"Pole known  : {pole_known}/{n} "
          f"(qualifying={ (df.poleSource=='qualifying').sum() }, "
          f"grid={ (df.poleSource=='grid').sum() })")
    print(f"Pole->Win   : {pole_win_rate:.1%} of races won from pole")
    print(f"CSV    -> {csv_path}")
    print(f"SQLite -> {db_path}")
    print("\nMost recent 5 races:")
    cols = ["season", "round", "raceName", "winnerDriver", "poleDriver", "poleWon"]
    print(df[cols].tail(5).to_string(index=False))


if __name__ == "__main__":
    main()
