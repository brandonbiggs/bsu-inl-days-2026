# Preflight checklist

## 3-5 days before

- [ ] Rebuild the zip if you changed anything: `tools/package_kit.sh`, then `tools/test_kit.sh` (all PASS).
- [ ] Ask the venue: power strips, projector input, Wi-Fi details. Claude itself still needs internet.

## Day before

- [ ] **Clean-machine test:** unzip the kit into a new folder, follow `PREWORK.md` from scratch, `verify_setup.py` all PASS.
- [ ] Full rehearsal with a stopwatch, running every prompt in `prompts.md`. Note anything slower than `FACILITATOR_SCRIPT.md` expects.
- [ ] Save **screenshots of each stage** (plan, checks, both figures, 3D, `/mcp`, an MCP answer) into a folder and into the slides.
- [ ] Keep an **offline copy** of the rehearsal outputs: the checkpoints already contain every output. Open `checkpoints/stage4_3d/outputs/anomaly_surface_3d.html` with Wi-Fi off and confirm it renders.
- [ ] Put a **backup copy of the kit on a USB stick** (zip + unzipped), plus a few copies for attendees who never downloaded.
- [ ] Clear the MCP server from your rehearsal folder (`claude mcp remove gistemp`) so the live add is real.

## Day of (30 minutes before)

- [ ] Fresh kit folder for the demo. `outputs/` contains only `.gitkeep`.
- [ ] Run `uv sync`, then `uv run python verify_setup.py`.
- [ ] Copy the `claude mcp add` line it prints into a note.
- [ ] Start `claude` once to confirm you're signed in, then exit.
- [ ] Terminal: **font 20 pt or larger**, light theme with high contrast, window wide enough that tables don't wrap.
- [ ] Check readability from the back of the room.
- [ ] **Notifications off** (macOS Focus / Windows Do Not Disturb). Close email and chat.
- [ ] Open `prompts.md` on the second screen, or print it.
- [ ] Open the slides at slide 1.
- [ ] Have the file browser open on `outputs/` for showing PNGs.
- [ ] Check a browser opens files. Set its zoom to 125%.
- [ ] Phone hotspot ready as a Wi-Fi backup.
- [ ] Have `CONTINGENCY.md` open in a tab.
