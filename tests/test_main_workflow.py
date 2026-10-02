import json

import Main


def test_main_creates_unique_output(monkeypatch, tmp_path):
    monkeypatch.setattr(Main, "ROOT", tmp_path)
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "default.json").write_text(
        json.dumps({
            "seed": 1, "n": 4, "f": 1, "round": 1, "values": ["A", "B", "C"],
            "abstractions": ["L0", "L1", "L2"], "output_root": "output",
            "run_finite_resilience_sweep": True, "sweep_max_n": 4, "generate_plot": False,
        }), encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    first = Main.run()
    second = Main.run()
    assert first.name == "test1"
    assert second.name == "test2"
    assert (first / "manifest.json").exists()
    assert (second / "resilience_sweep.csv").exists()
