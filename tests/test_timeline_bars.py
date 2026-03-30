import pytest
from pathlib import Path
from scripts.charts.timeline_bars import create_mekko, create_timeline_bars, DEMO_DATA


def test_demo_data_has_required_keys():
    assert "periods" in DEMO_DATA
    for p in DEMO_DATA["periods"]:
        assert "start" in p
        assert "end" in p
        assert "value" in p
        assert p["end"] > p["start"]


def test_create_mekko_returns_figure():
    fig = create_mekko(DEMO_DATA, title="Test")
    assert fig is not None


def test_create_mekko_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_mekko(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
    assert Path(out).stat().st_size > 0


def test_backward_compat_alias():
    """create_timeline_bars is an alias for create_mekko."""
    assert create_timeline_bars is create_mekko
