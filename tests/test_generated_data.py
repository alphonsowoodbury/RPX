import csv
import json
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GrandPrixDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / "data" / "grands_prix.csv").open(newline="", encoding="utf-8") as file:
            cls.rows = list(csv.DictReader(file))

    def test_has_world_championship_history(self):
        seasons = {int(row["season"]) for row in self.rows}
        self.assertEqual(min(seasons), 1950)
        self.assertGreaterEqual(max(seasons), 2026)
        self.assertGreater(len(self.rows), 1_100)

    def test_season_and_round_are_unique(self):
        keys = [(row["season"], row["round"]) for row in self.rows]
        self.assertEqual(len(keys), len(set(keys)))

    def test_required_values_and_types(self):
        required = ("raceName", "circuitId", "winnerDriver", "winnerConstructor")
        for row in self.rows:
            date.fromisoformat(row["date"])
            self.assertIn(row["poleWon"], {"True", "False"})
            self.assertTrue(all(row[field].strip() for field in required))


class CircuitArtifactTests(unittest.TestCase):
    def test_circuit_statistics_are_bounded(self):
        stats = json.loads((ROOT / "site" / "data" / "circuit_stats.json").read_text())
        self.assertGreater(len(stats), 70)
        for circuit in stats.values():
            self.assertGreater(circuit["races"], 0)
            self.assertGreaterEqual(circuit["poleWinRate"], 0)
            self.assertLessEqual(circuit["poleWinRate"], 1)

    def test_track_index_matches_track_files(self):
        track_dir = ROOT / "site" / "tracks" / "data"
        index = json.loads((track_dir / "index.json").read_text())
        ids = {item["id"] for item in index}
        files = {path.stem for path in track_dir.glob("*.json") if path.name != "index.json"}
        self.assertEqual(ids, files)


if __name__ == "__main__":
    unittest.main()
