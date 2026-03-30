---
name: slide-templates
description: "9 consulting slide templates with Plotly drafts and Nano Banana styling. Use when: user asks for a specific chart type (spider chart, stacked bar, 2x2 matrix, driver tree, ranked bars, harvey balls, bubble chart, stakeholder quotes, agenda), wants to create a single consulting-style slide, or says 'slide template', 'chart', 'make a slide', 'consulting slide'."
---

# Slide Templates

10 consulting-style slide templates. Each produces a Plotly draft for data accuracy, then sends to Nano Banana MCP for premium styling.

## Available Templates

| # | Template | Script | When to Use |
|---|----------|--------|-------------|
| 1 | Stacked Bar | `stacked_bar.py` | Compare composition across objects |
| 2 | Mekko Chart | `timeline_bars.py` | Two dimensions per bar (width + height) |
| 3 | Ranked Bars | `waterfall.py` | Rank/benchmark against alternatives |
| 4 | Driver Tree | `driver_tree.py` | Decompose a KPI into components |
| 5 | Spider/Radar | `spider_radar.py` | Compare profiles across dimensions |
| 6 | Harvey Balls | `harvey_balls.py` | Qualitative multi-criteria scoring |
| 7 | Bubble/2x2 | `bubble_matrix.py` | Strategic positioning (2 axes + size) |
| 8 | Quotes | `stakeholder_quotes.py` | Structured pro/contra feedback |
| 9 | Agenda | `agenda.py` | Presentation navigation/TOC |
| 10 | Waterfall Flow | `waterfall_flow.py` | Cumulative +/- contributions to total |

For help choosing: read `${CLAUDE_PLUGIN_ROOT}/references/chart-selection.md`

## Workflow for Each Slide

### Step 1: Clarify Data
Ask the user what data goes into the chart. Each template has a specific data schema.
If the user is unsure, show them the DEMO_DATA from the script as an example.

### Step 2: Prepare Data Dict
Structure the user's data into the template's expected format (Python dict / JSON).

### Step 3: Generate Plotly Draft
```bash
cd ${CLAUDE_PLUGIN_ROOT}
uv run python -m scripts.charts.<template> --data '<JSON>' --output output/draft_<name>.png
```

### Step 4: Review Draft with User
Show the draft PNG. Confirm data accuracy. Adjust if needed.

### Step 5: Style with Nano Banana
Send a TEXT-ONLY prompt to Nano Banana MCP. DO NOT send the Plotly draft as reference_images — Nano Banana must create its own visual design from scratch. The Plotly draft is only for YOUR data verification.

Use `mcp__nanobanana-mcp__gemini_generate_image` with:
- `aspect_ratio`: "16:9"
- `conversation_id`: "consulting-deck" (for style consistency across slides)
- `prompt`: Build from base prompt + ALL DATA described in text + template-specific accents
- **NO reference_images** — Nano Banana designs freely, not copying Plotly's look

The prompt must include ALL data points as text (exact numbers, labels, categories). Nano Banana cannot see the Plotly chart — it gets everything from the prompt.

### Step 6: Review Styled Slide
Show the Nano Banana output. If user wants changes, use `mcp__nanobanana-mcp__gemini_edit_image`.

## Base Prompt for Nano Banana

```
Create a premium consulting slide from scratch. Design it as a professional presentation slide.

LAYOUT:
- Title at top-left: bold, large, max 2 lines
- Title IS a conclusion/insight, not a description
- Chart/content centered, ~60% of slide area
- Source footnote bottom-left, small text

VISUAL PRINCIPLES:
- Focus: highlight the key takeaway visually (color, size, border)
- Grouping: related elements close together
- Contrast: primary larger/brighter, secondary smaller/muted
- Whitespace: generous — air = premium
- No decorative elements, no gradients, no shadows
- Flat design with depth through spacing

STYLE:
- Premium startup aesthetic — Series B pitch deck quality
- Clean, minimal, professional
- Color palette from theme (load ${CLAUDE_PLUGIN_ROOT}/themes/default.yaml)

DATA:
- All data is provided in the prompt as text — render it accurately
- Do not invent or approximate numbers
- [INSERT ALL DATA POINTS, LABELS, VALUES, AND CATEGORIES HERE]

CALLOUT ANNOTATIONS:
- Add callout boxes or arrows pointing to key data changes or insights
- Use accent color for callout borders/arrows
- Callout text should be brief (5-10 words max)
- Examples: "3x growth YoY", "Biggest gap", "Key driver", "Below target"
- Position callouts so they don't obscure data
- Use sparingly — 1-3 per slide maximum

TEXT READABILITY:
- All text must be readable when projected from 5 meters
- Minimum font size equivalent: 14px for body, 18px for data labels, 24px for titles
- Use bold for key numbers and insights
- High contrast between text and background

TITLE: "[insert approved headline]"
SOURCE: "[insert data source]"
```

## Template-Specific Prompt Additions

### Stacked Bar
```
ACCENTS:
- Thin connecting lines between corresponding segments across bars
- Percentage labels inside each segment (white text, bold)
- Highlight the dominant segment with slightly bolder color
- Callout arrow pointing to the most interesting difference between bars
- Total value labels above each bar
```

### Mekko Chart
```
ACCENTS:
- Bar WIDTH encodes one dimension, HEIGHT encodes another — label both axes clearly
- Label each bar with its name (large, bold) and both dimension values
- Color code bars by category or performance
- Callout on the most interesting bar explaining why it stands out
- Annotations showing the width-dimension value (e.g., "$25B market")
```

### Waterfall / Ranked Bars
```
ACCENTS:
- Highlighted bar(s) in accent color, rest in muted gray
- Value labels on top of each bar (bold, 16px+)
- Rank numbers (#1, #2...) next to bar labels
- Descending sort, clean spacing
- Horizontal average/benchmark line with label
- Callout showing delta from leader for highlighted item
```

### Driver Tree
```
ACCENTS:
- Nodes colored by status: green=met, red=unmet, yellow=partial
- Clear top-to-bottom hierarchical layout with generous level spacing
- Thick connecting lines between parent and children (2px+)
- Root node significantly larger and bolder
- Status labels next to each node (Met/Unmet/Partial)
- Callout annotation on the critical unmet node explaining the gap
```

### Spider / Radar
```
ACCENTS:
- Semi-transparent fill under each profile line
- Circle or highlight the 2 biggest gaps between profiles
- Annotate gap areas with callout text explaining the gap (e.g., "Integration: -25pts")
- Legend positioned cleanly (top-right or bottom-center)
- Axis labels large and readable (14px+)
- Value labels at each data point
```

### Harvey Ball Matrix
```
ACCENTS:
- Clean grid layout with generous spacing
- Large circles (40px+) with proportional fill (0%=empty, 25%, 50%, 75%, 100%=full)
- Row headers bold and large (16px+), column headers at top (14px+)
- Highlight the "winner" row with subtle background
- Add a fill legend at bottom
- Alternating row backgrounds for readability
```

### Bubble / 2x2 Matrix
```
ACCENTS:
- Dashed lines dividing quadrants
- Quadrant labels LARGE and BOLD in corners (18px+, e.g., "Stars", "Cash Cows")
- Key bubble larger and in accent color with bold label
- Size legend explaining what bubble size represents
- Item labels large (16px+) with (x, y) value annotations
- Callout on the key item explaining why it's positioned there
- "Top box" zone optionally highlighted with subtle background
```

### Stakeholder Quotes
```
ACCENTS:
- Two-column layout: positive (left) vs concerns (right)
- Large styled quotation marks (« » or oversized " ")
- Quote text large and readable (18px+)
- Attribution in muted text (14px+) below each quote
- Numbered bullets for each quote
- Summary box at bottom with key takeaway, prominent (16px+ bold)
- Vertical divider between columns
```

### Agenda
```
ACCENTS:
- Section numbers in VERY large bold type (36px+)
- Section titles prominent and bold (26px+)
- Subsections readable (16px+), muted color
- Generous spacing between sections
- Thin separators between sections
- Accent bar/stripe on the left side of each section
- Optionally highlight current section in accent color
```

### Waterfall Flow
```
ACCENTS:
- Green bars for positive contributions, red for negative, dark blue for totals
- Value labels above each bar (bold, 18px+), with +/- prefix for relative items
- Dotted connector lines between bars showing the cumulative flow
- Callout on the largest positive and largest negative factor
- Clear separation between starting value, contributions, and ending total
- Y-axis shows the value scale, X-axis shows factor names (angled if needed)
```

## Theme
Load colors and typography from: `${CLAUDE_PLUGIN_ROOT}/themes/default.yaml`
Users can customize by editing or replacing this file.
