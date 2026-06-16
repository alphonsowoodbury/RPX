#!/usr/bin/env python3
"""
Rees Performance — circuit geometry prep for the 3D track explorer (POC).

Fetches real circuit centerlines (GeoJSON, WGS84 lon/lat) from the open
f1-circuits dataset, projects them to local meters centered at the origin,
and writes compact JSON the Three.js page can load directly.

Source: github.com/bacinger/f1-circuits
"""
import json
import math
import urllib.request
from pathlib import Path

RAW = "https://raw.githubusercontent.com/bacinger/f1-circuits/master/circuits/{}.geojson"
OUT = Path("/Volumes/F1/site/tracks/data")

# id -> friendly slug (file name on the geojson repo)
CIRCUITS = {
    "silverstone": "gb-1948",
    "suzuka":      "jp-1962",
    "monza":       "it-1922",
    "spa":         "be-1925",
    "monaco":      "mc-1929",
    "redbullring": "at-1969",   # Austrian GP — next race
}


def fetch(name):
    with urllib.request.urlopen(RAW.format(name), timeout=30) as r:
        return json.load(r)


def line_coords(geom):
    """Return the longest line of coordinates from a (Multi)LineString."""
    if geom["type"] == "LineString":
        return geom["coordinates"]
    if geom["type"] == "MultiLineString":
        return max(geom["coordinates"], key=len)
    raise ValueError("unexpected geometry: " + geom["type"])


def build(slug, file):
    gj = fetch(file)
    feat = gj["features"][0]
    props = feat["properties"]
    coords = line_coords(feat["geometry"])

    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    lon0 = sum(lons) / len(lons)
    lat0 = sum(lats) / len(lats)
    m_per_lat = 111320.0
    m_per_lon = 111320.0 * math.cos(math.radians(lat0))

    pts = [[round((c[0] - lon0) * m_per_lon, 2),
            round((c[1] - lat0) * m_per_lat, 2)] for c in coords]

    xs = [p[0] for p in pts]
    zs = [p[1] for p in pts]
    max_dim = max(max(xs) - min(xs), max(zs) - min(zs))

    # closed if first and last points are within 60 m
    dx, dz = pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]
    closed = math.hypot(dx, dz) < 60

    return {
        "id": slug,
        "name": props.get("Name"),
        "location": props.get("Location"),
        "length_m": props.get("length"),
        "opened": props.get("opened"),
        "firstgp": props.get("firstgp"),
        "altitude_m": props.get("altitude"),
        "points": pts,
        "closed": closed,
        "bounds": {
            "minX": round(min(xs), 1), "maxX": round(max(xs), 1),
            "minZ": round(min(zs), 1), "maxZ": round(max(zs), 1),
            "maxDim": round(max_dim, 1),
        },
        "source": "github.com/bacinger/f1-circuits",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for slug, file in CIRCUITS.items():
        try:
            data = build(slug, file)
        except Exception as e:
            print(f"  ! {slug}: {e}")
            continue
        (OUT / f"{slug}.json").write_text(json.dumps(data))
        index.append({"id": slug, "name": data["name"],
                      "location": data["location"], "length_m": data["length_m"]})
        print(f"  ✓ {slug:12s} {data['name']:34s} {len(data['points']):3d} pts  "
              f"{data['bounds']['maxDim']:.0f} m  closed={data['closed']}")
    (OUT / "index.json").write_text(json.dumps(index))
    print(f"\nWrote {len(index)} circuits -> {OUT}")


if __name__ == "__main__":
    main()
