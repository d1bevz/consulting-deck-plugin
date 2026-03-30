import pytest
from pathlib import Path

from scripts.utils import load_theme, get_plotly_layout, PLUGIN_ROOT


def test_load_theme_default():
    theme = load_theme()
    assert theme["name"] == "Premium Startup"
    assert theme["colors"]["primary"] == "#1a1a2e"
    assert theme["colors"]["accent"] == "#e94560"
    assert len(theme["colors"]["chart_palette"]) == 8
    assert theme["style"]["slide_width"] == 1920
    assert theme["style"]["slide_height"] == 1080


def test_load_theme_custom(tmp_path):
    custom = tmp_path / "custom.yaml"
    custom.write_text('name: "Test"\ncolors:\n  primary: "#000000"\n  chart_palette: ["#111"]')
    theme = load_theme(str(custom))
    assert theme["name"] == "Test"
    assert theme["colors"]["primary"] == "#000000"


def test_load_theme_missing_file():
    with pytest.raises(FileNotFoundError):
        load_theme("/nonexistent/theme.yaml")


def test_get_plotly_layout():
    theme = load_theme()
    layout = get_plotly_layout(theme, title="Test Title", source="Test Source")
    assert layout["title"]["text"] == "Test Title"
    assert layout["width"] == 1920
    assert layout["height"] == 1080
    assert layout["plot_bgcolor"] == "#ffffff"
    source_annotations = [a for a in layout["annotations"] if "Test Source" in a.get("text", "")]
    assert len(source_annotations) == 1


def test_plugin_root_exists():
    assert PLUGIN_ROOT.exists()
