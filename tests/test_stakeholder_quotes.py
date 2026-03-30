import pytest
from pathlib import Path
from scripts.charts.stakeholder_quotes import create_stakeholder_quotes, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "pro" in DEMO_DATA
    assert "contra" in DEMO_DATA
    assert "summary" in DEMO_DATA
    for q in DEMO_DATA["pro"] + DEMO_DATA["contra"]:
        assert "quote" in q
        assert "source" in q

def test_create_stakeholder_quotes_returns_figure():
    fig = create_stakeholder_quotes(DEMO_DATA, title="Test")
    assert fig is not None

def test_create_stakeholder_quotes_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_stakeholder_quotes(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
