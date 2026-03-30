import json
import pytest
from pathlib import Path

from scripts.charts.stacked_bar import create_stacked_bar, DEMO_DATA


def test_demo_data_has_required_keys():
    assert "categories" in DEMO_DATA
    assert "segments" in DEMO_DATA
    assert "values" in DEMO_DATA
    assert len(DEMO_DATA["values"]) == len(DEMO_DATA["segments"])
    for row in DEMO_DATA["values"]:
        assert len(row) == len(DEMO_DATA["categories"])


def test_create_stacked_bar_returns_figure():
    fig = create_stacked_bar(DEMO_DATA, title="Test Chart")
    assert fig is not None
    assert len(fig.data) == len(DEMO_DATA["segments"])


def test_create_stacked_bar_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    fig = create_stacked_bar(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
    assert Path(out).stat().st_size > 0
