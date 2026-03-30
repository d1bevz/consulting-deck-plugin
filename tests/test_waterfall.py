import pytest
from pathlib import Path
from scripts.charts.waterfall import create_ranked_bars, create_waterfall, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "items" in DEMO_DATA
    for item in DEMO_DATA["items"]:
        assert "name" in item
        assert "value" in item
        assert "highlight" in item

def test_create_ranked_bars_returns_figure():
    fig = create_ranked_bars(DEMO_DATA, title="Test")
    assert fig is not None
    assert len(fig.data) > 0

def test_items_sorted_descending():
    fig = create_ranked_bars(DEMO_DATA, title="Test")
    y_values = list(fig.data[0].y)
    assert y_values[0] >= y_values[-1]

def test_create_ranked_bars_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_ranked_bars(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()

def test_backward_compat_alias():
    """create_waterfall still works as an alias."""
    assert create_waterfall is create_ranked_bars

def test_has_average_line():
    fig = create_ranked_bars(DEMO_DATA, title="Test")
    # Should have a horizontal average line shape
    shapes = fig.layout.shapes
    assert len(shapes) >= 1
    assert shapes[0].type == "line"

def test_has_rank_annotations():
    fig = create_ranked_bars(DEMO_DATA, title="Test")
    annotation_texts = [a.text for a in fig.layout.annotations if a.text]
    rank_labels = [t for t in annotation_texts if t.startswith("<b>#")]
    assert len(rank_labels) == len(DEMO_DATA["items"])
