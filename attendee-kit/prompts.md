# Workshop prompts

Copy each prompt into Claude Code. **Your results will differ from your neighbor's and from the presenter's.** That is normal: Claude writes new code each time. What matters is that you get the same *kinds* of output and that Claude shows its evidence.

**Fallen behind?** Each stage has a checkpoint. Paste the "Stuck?" prompt for the stage you want to join and Claude copies the reference files into `outputs/` for you.

| Stage | What you make | Minutes |
|---|---|---|
| 0 Setup check | Claude describes your folder | 5 |
| 1 Plan | A reviewed, edited plan | 7 |
| 2 Explore | Tidy data file + checks | 7 |
| 3 Graphs | Line chart + heatmap (PNG, SVG) | 7 |
| 4 3D | Interactive 3D surface (HTML) | 8 |
| 5 MCP | Ask a database questions in English | 8 |
| Wrap-up | A prompt for your own research | 3 |

---

## Stage 0: Setup check (5 min)

In a terminal, go to this folder and check your setup:

```
uv run python verify_setup.py
```

Every line should say PASS. Then start Claude Code in this folder:

```
claude
```

Paste:

```
Describe this folder in 5 short bullet points: what files are here, what the data is, and what CLAUDE.md asks you to do.
```

**You should see:** a short summary mentioning the NASA GISTEMP CSV, the `outputs/` folder, and rules from `CLAUDE.md` (save to `outputs/`, don't touch `data/`, state assumptions).

**Make it your own:**

```
Read CLAUDE.md. Which of these rules would matter most in my field, and what rule would you add?
```

**Stuck?** If `verify_setup.py` fails, follow the `fix:` line it prints and wave for help. You can still follow along on the presenter's screen.

---

## Stage 1: Plan before you act (7 min)

**Turn on plan mode.** Press **Shift+Tab** until the bottom of the screen says **⏸ plan mode on**. The number of presses depends on which mode you start in. On Windows, if Shift+Tab does nothing, try **Alt+M**. You can also start the prompt with `/plan `. In plan mode, Claude reads files and proposes a plan but does not change anything.

Paste:

```
I want to explore the GISTEMP data in data/ and produce a short report with two figures. Make a step-by-step plan. Don't write any code yet.
```

**Read the plan and check it:**

- [ ] Does it state its assumptions (units, baseline period, what the columns mean)?
- [ ] Does it name the output files and put them in `outputs/`?
- [ ] Does it say how it will handle missing values?
- [ ] Does it include a step that verifies the results?

**Change one step.** Use this prompt or write your own:

```
Revise the plan: (1) save a tidy long-format file outputs/gistemp_tidy.csv with columns year, band, lat_min, lat_max, anomaly; (2) add a verification step after each phase. Group the plan into phases: explore, figures, 3D, report. When I approve, do only the explore phase, then stop and show me your checks.
```

**Approve.** When Claude asks whether to proceed, pick the option that says **Yes**. Either "auto-accept edits" or "manually approve edits" is fine. Approving starts Stage 2.

**Make it your own:**

```
What assumption in this plan is most likely to be wrong, and how would we find out?
```

**Stuck?** See an example plan in `checkpoints/stage1_plan/plan_example.md`.

---

## Stage 2: Execute and explore (7 min)

If you approved the plan in Stage 1, Claude is already working. Watch it run, and approve any commands it asks to run. If you need to start this stage fresh, paste:

```
Do the explore phase only: load data/ZonAnn.Ts+dSST.csv, check for missing values, summarize each column, flag anything odd, and save a tidy file outputs/gistemp_tidy.csv with columns year, band, lat_min, lat_max, anomaly. Stop before making figures.
```

**Then ask for evidence:**

```
List every check you ran on the data, and for each one show the evidence (numbers or output), not just the conclusion.
```

**You should see:** row and year counts, a statement about missing values (this copy has none, and Claude should say so), per-band summaries, and `outputs/gistemp_tidy.csv`.

**Nudge, if Claude didn't mention overlapping bands:**

```
Check whether any of these latitude bands overlap. If they do, make the tidy file use only non-overlapping bands, and tell me which ones you kept.
```

A good result keeps 8 bands: 90S-64S, 64S-44S, 44S-24S, 24S-EQU, EQU-24N, 24N-44N, 44N-64N, 64N-90N. That gives 146 years x 8 bands = 1168 rows.

**Extra evidence check (optional):**

```
Recompute the global mean from the 8 bands using area weights (proportional to sin(lat_max) - sin(lat_min)) and compare it with the Glob column. How close is it?
```

**Ask your own question:**

```
[Your question about the data, e.g. "Which band has the most year-to-year variability, and why might that be?"]
```

**Stuck?** Paste:

```
Copy everything in checkpoints/stage2_explore/outputs/ into outputs/, then summarize what those files contain.
```

---

## Stage 3: Graphs (7 min)

```
Make two figures and save each to outputs/ as PNG and SVG, using a script saved in outputs/. (1) A line chart of the global anomaly (Glob) by year with a smoothed line; tell me which smoothing you chose and why. (2) A heatmap of anomaly by latitude band (south at the bottom) and year, from outputs/gistemp_tidy.csv. Then look at each PNG and tell me one thing you checked.
```

**You should see:** two PNG and two SVG files in `outputs/`. Open the PNGs from your file browser.

**Iterate in plain English.** Try one or more:

```
Use a colorblind-safe palette for the line chart.
```

```
Make sure the heatmap uses a diverging colormap centered at zero, so blue is cooler and red is warmer than the 1951-1980 baseline.
```

```
Restyle both figures for a journal: serif font, 10 pt text, no top or right axis lines, 7 inches wide.
```

```
Add a caption under each figure: "Data: NASA GISS GISTEMP v4. Anomaly relative to 1951-1980."
```

**Make it your own:**

```
Make the figure I would actually put in a paper about polar amplification, and write its caption.
```

**Stuck?** Paste:

```
Copy everything in checkpoints/stage3_graphs/outputs/ into outputs/, then list the figures.
```

---

## Stage 4: 3D (8 min)

```
Using outputs/gistemp_tidy.csv, make an interactive 3D Plotly surface: x = year, y = latitude (band center), z = anomaly, with a diverging colorscale centered at zero. Save it in outputs/ as one self-contained HTML file that works offline (embed plotly.js, no CDN). Then open it in my web browser.
```

**You should see:** a 3D surface in your browser that you can rotate and zoom. Hover to see values. The Arctic edge should rise most sharply in recent decades.

**Make it your own (data sculpture):**

```
Turn this into a "data sculpture": exaggerate the vertical scale, make the Arctic band stand out, and write a 3-sentence museum label for it. Save it as a new HTML file.
```

**Stretch: printable STL (CUT FIRST if we're short on time)**

```
Also export the surface as a 3D-printable STL in outputs/: a closed solid with a flat base at least 5 mm thick and about 180 mm wide; state the vertical scale in mm per °C. Use only numpy, no new packages. Tell me how you checked that it is watertight.
```

**Stuck?** Paste:

```
Copy everything in checkpoints/stage4_3d/outputs/ into outputs/, then open the HTML file in my browser.
```

---

## Stage 5: Connect a tool with MCP (8 min)

**Step 1: build a database.** Paste:

```
Build a SQLite database outputs/data.db from outputs/gistemp_tidy.csv with one table: anomalies(year, band, lat_min, lat_max, anomaly). Use Python's built-in sqlite3. Show the row count and 3 sample rows.
```

**Step 2: connect it.** Exit Claude by typing `/exit`. In the same terminal, run the `claude mcp add` command that `verify_setup.py` printed at the end. It looks like this, with your own Python path:

```
claude mcp add gistemp -- /path/to/attendee-kit/.venv/bin/python mcp/sqlite_server.py outputs/data.db
```

Then restart Claude and pick up where you left off:

```
claude --continue
```

Type `/mcp`. You should see **gistemp** marked as connected. `mcp/sqlite_server.py` is a small read-only server included in this kit. Open it and read it: it is about 60 lines.

**Step 3: ask questions.** Claude will ask permission the first time it uses each tool. Read the prompt before you approve.

```
Using only the gistemp database tools (not the CSV files): which decade had the largest warming at 64N-90N? Show the SQL you ran.
```

```
Using the gistemp database: for each band, compare the 1951-1980 average with the 1996-2025 average. Which band warmed most and which least? Show the SQL.
```

```
Using the gistemp database: in which year did each band reach its record high? Show the SQL.
```

**Make it your own:**

```
Using the gistemp database, try to delete all rows from the anomalies table. What happened, and why?
```

(It should fail: the server opens the database read-only.)

**Stuck?** Paste:

```
Copy everything in checkpoints/stage5_mcp/outputs/ into outputs/.
```

Then do Step 2. If `/mcp` shows failed, see `checkpoints/stage5_mcp/README.md`.

---

## Wrap-up: your own research (3 min)

Fill in the brackets and paste. Plan mode is a good place to try it.

```
I study [field]. I have [data, format, size, where it lives]. I want to [question or output]. Make a plan with stages, and for each stage name the output file and the check you will run. List the decisions where I should review before you continue. Don't write code yet.
```

**Three takeaways**

1. Define the stages and outputs first.
2. Make the agent show its evidence.
3. Keep a human at the decision points.
