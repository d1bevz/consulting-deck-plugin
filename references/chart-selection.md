# Chart Selection Guide

## Decision Matrix: Task -> Chart Type

| Task | Best Chart Type | Template |
|------|----------------|----------|
| Compare composition/parts of whole | Stacked Bar | `stacked_bar` |
| Compare same parameter across objects | Ranked Bars | `waterfall` |
| Show two dimensions per bar (width + height) | Mekko Chart | `timeline_bars` |
| Decompose a metric into drivers | Driver Tree | `driver_tree` |
| Compare profiles across dimensions | Spider / Radar | `spider_radar` |
| Qualitative multi-criteria scoring | Harvey Ball Matrix | `harvey_balls` |
| Position on two parameters + third dim | Bubble / 2x2 Matrix | `bubble_matrix` |
| Present structured feedback pro/contra | Stakeholder Quotes | `stakeholder_quotes` |
| Show presentation structure | Agenda | `agenda` |
| Show cumulative +/- contributions | Waterfall Flow | `waterfall_flow` |

## When to Use Each

### Stacked Bar
- Budget allocation across departments
- Time distribution across activities
- Revenue mix by product/segment
- Market share composition

### Mekko Chart
- Market segments: width=market size, height=growth rate
- Client portfolio: width=revenue, height=margin
- Product lines: width=units sold, height=avg price
- Project timeline: width=duration, height=complexity

### Ranked Bars
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

### Waterfall Flow
- Revenue bridge (starting → contributions → ending)
- P&L waterfall (revenue → costs → profit)
- Budget variance analysis
- Factor influence analysis (what drove the change)
- Before/after decomposition
