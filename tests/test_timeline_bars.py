import pytest
from pathlib import Path
from scripts.charts.timeline_bars import create_timeline_bars, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "periods" in DEMO_DATA
    for p in DEMO_DATA["periods"]:
        assert "year" in p
        assert "label" in p
        assert "value" in p

def test_create_timeline_bars_returns_figure():
    fig = create_timeline_bars(DEMO_DATA, title="Test")
    assert fig is not None
    assert len(fig.data) > 0

def test_create_timeline_bars_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    fig = create_timeline_bars(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
    assert Path(out).stat().st_size > 0
