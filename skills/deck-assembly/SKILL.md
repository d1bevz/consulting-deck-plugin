---
name: deck-assembly
description: "Assemble approved slide PNGs into PDF or PPTX presentations. Use when: user asks to combine slides, export deck, create PDF from slides, or says 'assemble deck', 'export slides', 'combine slides', 'make PDF', 'make PPTX'."
---

# Deck Assembly

Combines approved slide PNG images into a final PDF or PPTX file.

## Workflow

### Step 1: Find Slides
Look for slide PNGs in the working directory or `${CLAUDE_PLUGIN_ROOT}/output/`.
List them and show to user:

```
Found slides:
1. slide_01_agenda.png
2. slide_02_market.png
3. slide_03_problem.png
...
```

### Step 2: Confirm Order
Ask user to confirm or reorder. They can also exclude slides.

### Step 3: Choose Format
- **PDF** (default) -- universal, good for sharing
- **PPTX** -- editable in PowerPoint/Google Slides (images as slide backgrounds)
- **Both** -- generate both formats

### Step 4: Assemble

```bash
cd ${CLAUDE_PLUGIN_ROOT}

# For PDF:
uv run python -m scripts.assembly output pdf

# For PPTX:
uv run python -m scripts.assembly output pptx
```

Or call programmatically:
```python
from scripts.assembly import assemble_pdf, assemble_pptx

image_paths = ["output/slide_01.png", "output/slide_02.png", ...]
assemble_pdf(image_paths, "output/final_deck.pdf")
assemble_pptx(image_paths, "output/final_deck.pptx")
```

### Step 5: Deliver
Send the assembled file to the user.
