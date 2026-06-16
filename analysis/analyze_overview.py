#!/usr/bin/env python3
"""
Rees Performance — Grands Prix overview analysis (v1)
Reads /Volumes/F1/data/grands_prix.csv and writes a markdown report.
"""
from pathlib import Path
import pandas as pd

DATA = Path("/Volumes/F1/data/grands_prix.csv")
OUT = Path("/Volumes/F1/analysis/grands_prix_overview.md")

df = pd.read_csv(DATA)
df["decade"] = (df["season"] // 10) * 10

L = []  # report lines
def p(s=""): L.append(s)

p("# Grands Prix — Overview Analysis")
p()
p("*Rees Performance · RPX · built from `grands_prix.csv` (1950–%d)*" % df.season.max())
p()
n = len(df)
overall = df["poleWon"].dropna().mean()
p(f"**{n:,} Grands Prix** across **{df.season.nunique()} seasons** and "
  f"**{df.circuitId.nunique()} circuits**. Pole sitter won **{overall:.1%}** of all races.")
p()

# --- Pole -> win conversion by decade ---
p("## Pole → win conversion, by decade")
p()
p("| Decade | Races | Won from pole | Conversion |")
p("|---|---:|---:|---:|")
g = df.dropna(subset=["poleWon"]).groupby("decade")
for dec, grp in g:
    rate = grp["poleWon"].mean()
    p(f"| {int(dec)}s | {len(grp)} | {int(grp['poleWon'].sum())} | {rate:.1%} |")
p()
p("*Pole = qualifying P1 from 2003; grid P1 before that (see data README).*")
p()

# --- Most poles ---
p("## Most pole positions (qualifying / grid P1)")
p()
poles = df["poleDriver"].value_counts().head(15)
p("| # | Driver | Poles |")
p("|---:|---|---:|")
for i, (drv, c) in enumerate(poles.items(), 1):
    p(f"| {i} | {drv} | {c} |")
p()

# --- Most wins ---
p("## Most race wins")
p()
wins = df["winnerDriver"].value_counts().head(15)
p("| # | Driver | Wins |")
p("|---:|---|---:|")
for i, (drv, c) in enumerate(wins.items(), 1):
    p(f"| {i} | {drv} | {c} |")
p()

# --- Best pole-to-win converters (min 15 poles) ---
p("## Best front-runners — pole→win conversion (min 15 poles)")
p()
pol = df.groupby("poleDriver")
conv = pd.DataFrame({
    "poles": pol.size(),
    "won_from_pole": pol["poleWon"].sum(min_count=1),
})
conv["rate"] = conv["won_from_pole"] / conv["poles"]
conv = conv[conv["poles"] >= 15].sort_values("rate", ascending=False).head(15)
p("| Driver | Poles | Won from pole | Conversion |")
p("|---|---:|---:|---:|")
for drv, r in conv.iterrows():
    p(f"| {drv} | {int(r.poles)} | {int(r.won_from_pole)} | {r.rate:.1%} |")
p()

# --- Constructors ---
p("## Constructors — wins and poles")
p()
cw = df["winnerConstructor"].value_counts()
cp = df["poleConstructor"].value_counts()
con = pd.DataFrame({"wins": cw, "poles": cp}).fillna(0).astype(int)
con = con.sort_values("wins", ascending=False).head(15)
p("| Constructor | Wins | Poles |")
p("|---|---:|---:|")
for name, r in con.iterrows():
    p(f"| {name} | {r.wins} | {r.poles} |")
p()

# --- Circuits where pole matters most / least (min 15 races) ---
p("## Circuits where pole matters most (min 15 races)")
p()
cg = df.dropna(subset=["poleWon"]).groupby("circuitName")
circ = pd.DataFrame({
    "races": cg.size(),
    "pole_win_rate": cg["poleWon"].mean(),
})
circ = circ[circ["races"] >= 15]
top = circ.sort_values("pole_win_rate", ascending=False).head(10)
bot = circ.sort_values("pole_win_rate").head(10)
p("**Pole is gold here (highest conversion):**")
p()
p("| Circuit | Races | Pole→win |")
p("|---|---:|---:|")
for name, r in top.iterrows():
    p(f"| {name} | {int(r.races)} | {r.pole_win_rate:.1%} |")
p()
p("**Pole means least here (lowest conversion):**")
p()
p("| Circuit | Races | Pole→win |")
p("|---|---:|---:|")
for name, r in bot.iterrows():
    p(f"| {name} | {int(r.races)} | {r.pole_win_rate:.1%} |")
p()

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(L))
print(f"Report -> {OUT}\n")
print("\n".join(L))
