"""Shared utilities for consulting-deck chart scripts."""

import json
import sys
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = PLUGIN_ROOT / "themes"
DEFAULT_THEME = THEMES_DIR / "default.yaml"
OUTPUT_DIR = PLUGIN_ROOT / "output"


def load_theme(path: str | None = None) -> dict:
    """Load a YAML theme file. Defaults to themes/default.yaml."""
    theme_path = Path(path) if path else DEFAULT_THEME
    if not theme_path.exists():
        raise FileNotFoundError(f"Theme not found: {theme_path}")
    with open(theme_path) as f:
        return yaml.safe_load(f)


def get_plotly_layout(theme: dict, title: str, source: str = "") -> dict:
    """Build a Plotly layout dict from theme settings."""
    colors = theme["colors"]
    style = theme["style"]
    return {
        "title": {
            "text": title,
            "font": {"size": 28, "color": colors["text"]},
            "x": 0.02,
            "xanchor": "left",
            "y": 0.95,
            "yanchor": "top",
        },
        "width": style["slide_width"],
        "height": style["slide_height"],
        "plot_bgcolor": colors["background"],
        "paper_bgcolor": colors["background"],
        "font": {"color": colors["text"], "size": 14},
        "margin": {"l": 80, "r": 60, "t": 100, "b": 80},
        "annotations": [
            {
                "text": f"Source: {source}" if source else "",
                "xref": "paper",
                "yref": "paper",
                "x": 0.02,
                "y": -0.06,
                "showarrow": False,
                "font": {"size": 10, "color": colors["muted"]},
            }
        ],
    }


def save_chart(fig, output_path: str) -> str:
    """Save a Plotly figure to PNG. Returns the output path."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(out), scale=2)
    return str(out)


def parse_cli_args() -> tuple[dict, str, str | None]:
    """Parse CLI arguments: --data JSON --output PATH [--theme PATH].
    Returns (data_dict, output_path, theme_path).
    """
    args = sys.argv[1:]
    data = {}
    output = "output/chart.png"
    theme_path = None

    i = 0
    while i < len(args):
        if args[i] == "--data" and i + 1 < len(args):
            data = json.loads(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output = args[i + 1]
            i += 2
        elif args[i] == "--theme" and i + 1 < len(args):
            theme_path = args[i + 1]
            i += 2
        else:
            i += 1

    return data, output, theme_path
