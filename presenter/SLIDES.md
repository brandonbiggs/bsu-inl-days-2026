---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono&display=swap');
  /* INL brand palette, ordered by usage */
  :root {
    --inl-blue:   #07519E;  /* primary: headings, title bg, tables, code */
    --inl-green:  #8DC340;  /* secondary: accent bars, bullets */
    --inl-sky:    #2BA8E0;  /* tertiary: quotes, links */
    --inl-red:    #CF1E4C;  /* accent: warnings, emphasis */
    --inl-orange: #F68C20;  /* accent: page numbers, small details */
    --ink:        #1f2a37;
    --brand-bar: linear-gradient(90deg,
      var(--inl-blue) 0 40%, var(--inl-green) 40% 65%, var(--inl-sky) 65% 80%,
      var(--inl-red) 80% 92%, var(--inl-orange) 92% 100%);
  }
  section {
    font-family: 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 32px;
    background: #ffffff;
    color: var(--ink);
    padding: 70px 80px 60px;
  }
  section::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 14px;
    background: var(--brand-bar);
  }
  section::after { color: var(--inl-orange); font-weight: 600; font-size: 20px; }
  h1, h2 { color: var(--inl-blue); font-weight: 800; letter-spacing: -0.02em; }
  h1 { font-size: 60px; }
  h2 {
    font-size: 46px;
    border-left: 8px solid var(--inl-green);
    padding-left: 20px;
    margin-bottom: 30px;
  }
  strong { color: var(--inl-blue); }
  em { color: var(--inl-red); font-style: normal; font-weight: 600; }
  a { color: var(--inl-sky); }
  code {
    font-family: 'JetBrains Mono', Menlo, monospace;
    background: #e8f0f9;
    color: var(--inl-blue);
    padding: 2px 8px;
    border-radius: 6px;
  }
  ul li::marker, ol li::marker { color: var(--inl-green); font-weight: 800; }
  blockquote {
    border-left: 6px solid var(--inl-sky);
    background: #eaf6fc;
    color: var(--ink);
    padding: 20px 30px;
    border-radius: 0 10px 10px 0;
    font-style: italic;
  }
  table { border-collapse: collapse; font-size: 26px; margin: 20px 0; }
  th { background: var(--inl-blue); color: #ffffff; border: none; }
  td { background: #f4f8fc; border: 1px solid #d5e2f0; }
  th, td { padding: 14px 22px; }
  .small { font-size: 22px; color: #5b6b7c; }
  .warn { color: var(--inl-red); font-weight: 600; }

  /* Title / closing slides: solid INL blue */
  section.lead {
    background: var(--inl-blue);
    color: #ffffff;
    justify-content: center;
    text-align: center;
  }
  section.lead::before { top: auto; bottom: 0; }
  section.lead h1 { color: #ffffff; font-size: 68px; }
  section.lead h1::after {
    content: ''; display: block; width: 160px; height: 8px;
    background: var(--inl-green); margin: 30px auto 0;
  }
  section.lead p { font-size: 30px; }
  section.lead strong { color: var(--inl-green); }
  section.lead .small { color: #cfe3f5; }

---

<!-- _class: lead -->
<!-- _paginate: false -->

# How to Build Agentic AI Workflows for Research

NASA GISTEMP v4 zonal temperature anomalies

<p class="small">You'll leave with outputs, the scripts that made them, and a template for your own work.</p>

---

## What makes a workflow agentic?

**Plan → Act → Check → Revise**

LLM answers. An agent takes steps, looks at the results, and adjusts.

Research risks: **unverified claims** · **irreproducible results** · **silent errors**

---

## Today's map

**Setup → Plan → Explore → Graphs → 3D → MCP → Your research**

- Every stage makes something you can see
- Every stage has a checkpoint folder
- `CLAUDE.md` holds the lab rules

---

## Stage 1: Plan before you act

**Shift+Tab** until "plan mode on" (Windows: **Alt+M** if needed) or `/plan`

> I want to explore the GISTEMP data in data/ and produce a short report with two figures. Write scripts to generate figures.

Good plan?
- Assumptions stated?
- Output files named?
- Missing values handled?
- Verification step?

---

## Stage 2: Iterate and Execute

Before approving the plan, review and modify. When happy with the plan, approve it.

---

## Stage 3: Figures are code

![bg right:55% fit](../attendee-kit/checkpoints/stage3_graphs/outputs/lat_year_heatmap.png)

- Line chart + latitude × year heatmap
- PNG + SVG
- Iterate in plain English
- New data? Rerun one script.

---

## Stage 4: Same data, new representation

Interactive 3D surface in **one self-contained HTML file**

---

## Stage 5: MCP, from reading files to using tools

| Stage 2 | Stage 5 |
|---|---|
| Claude opens a CSV and writes code against it | Claude calls a database through a structured tool interface |

List tables · Describe · Read-only query

**One protocol, many servers.**

---

## What else could you connect?

<p class="small">Examples, not demos</p>

- Reference managers (e.g. Zotero)
- Cloud drives (e.g. Google Drive)
- Literature search (e.g. PubMed)
- Institutional databases / data warehouses

<p class="warn">⚠️ MCP servers run with your permissions.</p>

---

## Take it home

> "I study **[field]**. I have **[data]**. I want to **[goal]**.
> Make a plan with stages, outputs, and checks..."

1. **Define stages and outputs first.**
2. **Make the agent show its evidence.**
3. **Keep a human at the decision points.**

