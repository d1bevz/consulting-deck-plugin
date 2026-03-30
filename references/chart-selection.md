# Chart Selection Guide

## Decision Matrix: Task -> Chart Type

| Task | Best Chart Type | Template |
|------|----------------|----------|
| Compare composition/parts of whole | Stacked Bar | `stacked_bar` |
| Compare same parameter across objects | Waterfall / Ranked Bars | `waterfall` |
| Show change over time | Timeline Bars | `timeline_bars` |
| Decompose a metric into drivers | Driver Tree | `driver_tree` |
| Compare profiles across dimensions | Spider / Radar | `spider_radar` |
| Qualitative multi-criteria scoring | Harvey Ball Matrix | `harvey_balls` |
| Position on two parameters + third dim | Bubble / 2x2 Matrix | `bubble_matrix` |
| Present structured feedback pro/contra | Stakeholder Quotes | `stakeholder_quotes` |
| Show presentation structure | Agenda | `agenda` |

## When to Use Each

### Stacked Bar
- Budget allocation across departments
- Time distribution across activities
- Revenue mix by product/segment
- Market share composition

### Timeline Bars
- Company growth by funding rounds
- Product version evolution
- Market entry history
- Project milestone timeline

### Waterfall / Ranked Bars
- NPS or CSAT benchmarking
- Feature comparison vs competitors
- Ranking of options by score
- Performance comparison

### Driver Tree
- Revenue or cost decomposition
- Root cause analysis
- Decision criteria assessment
- Product-market fit evaluation

### Spider / Radar
- Competitor analysis (multi-dimension)
- Team skill assessment
- Product feature comparison
- Capability maturity model

### Harvey Ball Matrix
- Vendor or technology evaluation
- Hiring candidate comparison
- Solution assessment against criteria
- Maturity assessment

### Bubble / 2x2 Matrix
- BCG growth-share matrix
- Risk vs impact prioritization
- Market attractiveness vs competitive position
- Effort vs value mapping

### Stakeholder Quotes
- Customer interview synthesis
- Market research findings
- Internal feedback compilation
- Expert opinion summary

### Agenda
- Presentation opening
- Section transitions (with highlight_index)
