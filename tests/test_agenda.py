import pytest
from pathlib import Path
from scripts.charts.agenda import create_agenda, DEMO_DATA

def test_demo_data_has_required_keys():
    assert "sections" in DEMO_DATA
    for section in DEMO_DATA["sections"]:
        assert "title" in section

def test_create_agenda_returns_figure():
    fig = create_agenda(DEMO_DATA, title="Test")
    assert fig is not None

def test_create_agenda_saves_png(tmp_path):
    out = str(tmp_path / "test.png")
    create_agenda(DEMO_DATA, title="Test", output_path=out)
    assert Path(out).exists()
