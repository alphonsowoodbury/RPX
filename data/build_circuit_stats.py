#!/usr/bin/env python3
"""
Rees Performance — per-circuit pole→win stats for the Race Hub.
Keyed by Jolpica circuitId so the site can look up the upcoming circuit.
"""
import json
from pathlib import Path
import pandas as pd

df = pd.read_csv("/Volumes/F1/data/grands_prix.csv")
OUT = Path("/Volumes/F1/site/data/circuit_stats.json")

# map circuitId -> our 3D track slug, where we have a model
TRACK_SLUG = {
    "silverstone": "silverstone", "suzuka": "suzuka", "monza": "monza",
    "spa": "spa", "monaco": "monaco", "red_bull_ring": "redbullring",
}

out = {}
for (cid, cname), grp in df.groupby(["circuitId", "circuitName"]):
    pw = grp["poleWon"].dropna()
    out[cid] = {
        "name": cname,
        "races": int(len(grp)),
        "poleWinRate": round(float(pw.mean()), 4) if len(pw) else None,
        "firstSeason": int(grp.season.min()),
        "lastSeason": int(grp.season.max()),
        "track3d": TRACK_SLUG.get(cid),
    }

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(out))
print(f"{len(out)} circuits -> {OUT}")
print("red_bull_ring:", out.get("red_bull_ring"))
