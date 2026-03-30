import pytest
from pathlib import Path
from scripts.charts.spider_radar import create_spider_radar, DEMO_DATA


def test_demo_data_has_required_keys():
    assert "axes" in DEMO_DATA
    assert "profiles" in DEMO_DATA
    for profile in DEMO_DATA["profiles"]:
        assert "name" in profile
        assert "values" in profile
        assert len(profile["values"]) == len(DEMO_DATA["axes"])


def test_create_spider_radar_returns_figure():
    fig = create_spider_radar(DEMO_DATA, title="Test")
    assert fig is not None
    assert len(fig.data) == len(DEMO_DATA["profiles"])


def test_create_spider_radar_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_spider_radar(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
