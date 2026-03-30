import pytest
from pathlib import Path
from scripts.charts.harvey_balls import create_harvey_balls, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "rows" in DEMO_DATA
    assert "columns" in DEMO_DATA
    assert "scores" in DEMO_DATA
    assert len(DEMO_DATA["scores"]) == len(DEMO_DATA["rows"])
    for row in DEMO_DATA["scores"]:
        assert len(row) == len(DEMO_DATA["columns"])
        for score in row:
            assert 0 <= score <= 4

def test_create_harvey_balls_returns_figure():
    fig = create_harvey_balls(DEMO_DATA, title="Test")
    assert fig is not None

def test_create_harvey_balls_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_harvey_balls(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
