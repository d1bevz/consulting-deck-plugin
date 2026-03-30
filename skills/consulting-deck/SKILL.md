---
name: consulting-deck
description: "Full consulting presentation builder with structured discovery, SCR framework, Minto pyramid, and horizontal logic. Use when: user asks to create a presentation, pitch deck, consulting deck, or says 'make a presentation', 'build a deck', 'create slides for', 'pitch deck', 'consulting deck'."
---

# Consulting Deck Builder

Orchestrates the full presentation creation process: discovery -> structure -> slide generation -> assembly.

**Core principle:** Never generate slides without first understanding the story. Discovery and horizontal logic come before any visual work.

## Prerequisites
- Read `${CLAUDE_PLUGIN_ROOT}/references/principles.md` for presentation framework
- Read `${CLAUDE_PLUGIN_ROOT}/references/chart-selection.md` for template selection
- Nano Banana MCP must be available for final styling

## Full Workflow

### Phase 1: Discovery

Conduct a structured interview. Ask one question at a time.

**1.1 Context & Audience**
- Who will see this? (investors, team, client, board, conference)
- What do they already know about the topic?
- What decision or action do you want from them after seeing this?

**1.2 SCR Interview**
- **Situation:** Describe the current state in 2-3 sentences. What is the shared understanding?
- **Complication:** What changed? What's the problem? What's the key question the audience has?
- **Resolution:** What do you propose? (can be a hypothesis at this stage)

**1.3 Data Discovery**
- What data do you have? (metrics, surveys, financials, interviews, research)
- What data is missing?
- What key numbers MUST appear on slides? (the "killer stats")

**1.4 Drivers & Arguments**
- Why is your resolution/proposal the right one? (ask for 3-4 reasons)
- Are there counterarguments? How do you address them?
- What does the audience risk if they DON'T follow your recommendation?

### Phase 2: Structure

**2.1 Formulate Main Message**
Apply Minto pyramid:
- Write one sentence that answers the audience's key question
- It must be: self-contained, new to the audience, a synthesis (not a list)

**2.2 Define 3-4 Arguments**
Each argument:
- Answers "why?" or "how?" relative to the main message
- Is MECE with the other arguments
- Has supporting evidence/data

**2.3 Build Title Chain (Horizontal Logic)**
Write a sequence of slide titles. Present ONLY the titles:

```
Read these as paragraphs of one text. Does the story flow?

1. [Title for context/situation slide]
2. [Title for complication slide]
3. [Title for main message slide]
4. [Title for argument 1 slide]
5. [Title for argument 2 slide]
6. [Title for argument 3 slide]
7. [Title for evidence/data slide]
8. [Title for conclusion/CTA slide]
```

**GATE: Do not proceed until the user approves the title chain.**

Iterate titles until the story is iron-clad. Check:
- Each title is a conclusion (not "Market Overview" but "Market growing at 16% driven by AI adoption")
- Titles flow logically from one to the next
- The full sequence tells a complete, persuasive story
- Max 12-15 words per title

### Phase 3: Template Selection

For each approved title, select the best template:
- Read `${CLAUDE_PLUGIN_ROOT}/references/chart-selection.md`
- Match the slide's PURPOSE to a template
- Present the mapping to user for approval:

```
Slide 1: "Market growing at 16%..." -> Stacked Bar (market segments)
Slide 2: "But 80% of platforms..." -> Waterfall (competitor ranking)
Slide 3: "Root cause is..." -> Driver Tree (problem decomposition)
...
```

### Phase 4: Slide Generation

For each slide, invoke the slide-templates skill workflow:
1. Prepare data for the template
2. Generate Plotly draft
3. Send to Nano Banana with template-specific prompt
4. Show to user for review

**GATE: Each slide must be approved before moving to the next.**

Use conversation_id "consulting-deck" in Nano Banana for style consistency.
Use aspect_ratio "16:9" for all slides.

### Phase 5: Assembly

When all slides are approved:
1. Confirm final order with user
2. Invoke deck-assembly skill
3. Generate PDF and/or PPTX
4. Deliver to user

## Slide Title Rules (enforced throughout)
- Title IS a conclusion or insight
- NOT a topic label ("Market Analysis") -- this is WRONG
- YES a finding ("European market grew 3x while US stagnated") -- this is RIGHT
- Maximum 12-15 words
- Maximum 2 lines

## Content Rules (enforced throughout)
- One slide = one message
- 80-140 words in body
- Source on every data slide
- Three perception levels: immediate (title, 5s) -> scan (layout, 15s) -> read (details, 2min)
