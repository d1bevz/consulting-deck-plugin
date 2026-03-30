import pytest
from pathlib import Path
from scripts.charts.driver_tree import create_driver_tree, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "tree" in DEMO_DATA
    root = DEMO_DATA["tree"]
    assert "node" in root
    assert "children" in root
    assert "status" in root

def test_create_driver_tree_returns_figure():
    fig = create_driver_tree(DEMO_DATA, title="Test")
    assert fig is not None

def test_create_driver_tree_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_driver_tree(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
    assert Path(out).stat().st_size > 0
