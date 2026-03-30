import pytest
from pathlib import Path
from scripts.charts.bubble_matrix import create_bubble_matrix, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "x_axis" in DEMO_DATA
    assert "y_axis" in DEMO_DATA
    assert "items" in DEMO_DATA
    for item in DEMO_DATA["items"]:
        assert "name" in item
        assert "x" in item
        assert "y" in item
        assert "size" in item

def test_create_bubble_matrix_returns_figure():
    fig = create_bubble_matrix(DEMO_DATA, title="Test")
    assert fig is not None

def test_create_bubble_matrix_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_bubble_matrix(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
