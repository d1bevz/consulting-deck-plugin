import pytest
from pathlib import Path
from scripts.charts.waterfall_flow import create_waterfall_flow, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "items" in DEMO_DATA
    for item in DEMO_DATA["items"]:
        assert "name" in item
        assert "value" in item
        assert "measure" in item  # "relative", "total", or "absolute"

def test_create_waterfall_flow_returns_figure():
    fig = create_waterfall_flow(DEMO_DATA, title="Test")
    assert fig is not None

def test_create_waterfall_flow_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_waterfall_flow(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
    assert Path(out).stat().st_size > 0
