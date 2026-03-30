import pytest
from pathlib import Path

from scripts.assembly import assemble_pdf, assemble_pptx


@pytest.fixture
def sample_pngs(tmp_path):
    """Create fake PNG files for testing."""
    import plotly.graph_objects as go
    paths = []
    for i in range(3):
        p = tmp_path / f"slide_{i}.png"
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2], y=[i, i + 1]))
        fig.write_image(str(p), width=1920, height=1080)
        paths.append(str(p))
    return paths


def test_assemble_pdf(sample_pngs, tmp_path):
    out = str(tmp_path / "deck.pdf")
    result = assemble_pdf(sample_pngs, out)
    assert Path(result).exists()
    assert Path(result).stat().st_size > 0


def test_assemble_pptx(sample_pngs, tmp_path):
    out = str(tmp_path / "deck.pptx")
    result = assemble_pptx(sample_pngs, out)
    assert Path(result).exists()
    assert Path(result).stat().st_size > 0


def test_assemble_pdf_empty_raises():
    with pytest.raises(ValueError):
        assemble_pdf([], "/tmp/empty.pdf")


def test_assemble_pptx_empty_raises():
    with pytest.raises(ValueError):
        assemble_pptx([], "/tmp/empty.pptx")
