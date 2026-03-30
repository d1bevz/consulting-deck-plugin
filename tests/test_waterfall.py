import pytest
from pathlib import Path
from scripts.charts.waterfall import create_waterfall, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "items" in DEMO_DATA
    for item in DEMO_DATA["items"]:
        assert "name" in item
        assert "value" in item
        assert "highlight" in item

def test_create_waterfall_returns_figure():
    fig = create_waterfall(DEMO_DATA, title="Test")
    assert fig is not None
    assert len(fig.data) > 0

def test_items_sorted_descending():
    fig = create_waterfall(DEMO_DATA, title="Test")
    y_values = list(fig.data[0].y)
    assert y_values[0] >= y_values[-1]

def test_create_waterfall_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_waterfall(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
