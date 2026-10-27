# INL Days @ BSU

**How to Build Agentic AI Workflows for Research**: a hands-on session using NASA temperature data.

## Setup (about 20 minutes)

You need three things: Claude Code, uv (which installs Python for you), and this kit's packages.

### 1. Get access to Claude

Claude Code needs a paid Claude account or an API key. **The free claude.ai plan does not include Claude Code.** Any of these work:

- **Through the university:** [BSU AI Documentation](https://talk.confluence.boisestate.edu/wiki/spaces/LTS/pages/2863726675/Using+API+Keys)
- **Personal plan:** Claude Pro or Max.
- **API key:** an Anthropic Console account with billing set up.

The first time you run `claude`, it opens a browser to sign in. Details: https://code.claude.com/docs/en/authentication. This doesn't happen if you set an API key.

### 2. Install Claude Code

Follow the official instructions for your system: **https://code.claude.com/docs/en/setup**

- **macOS / Linux:** use the native installer command on that page, or Homebrew.
- **Windows:** use the PowerShell installer on that page, or WinGet. Installing [Git for Windows](https://git-scm.com/downloads/win) as well is recommended but optional.
- No administrator rights are needed for the native installer.

Then **open a new terminal** and check that it works:

```
claude --version
```

### 3. Install uv

[uv](https://docs.astral.sh/uv/) installs Python and this kit's packages for you. You don't need to install Python separately.

| System | Command |
|---|---|
| macOS / Linux | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Windows (PowerShell) | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

`brew install uv` (macOS) and `winget install --id=astral-sh.uv -e` (Windows) also work. More options: https://docs.astral.sh/uv/getting-started/installation/

Then **open a new terminal** and check that it works:

```
uv --version
```

### 4. Unzip the kit and install packages

Unzip `attendee-kit.zip` somewhere simple, such as your Documents folder. On Windows, avoid OneDrive-synced folders if you can. Open a terminal **in that folder**:

- **macOS:** in Finder, right-click the folder and choose Services > New Terminal at Folder. Or type `cd ` in Terminal and drag the folder in.
- **Windows:** open the folder in File Explorer, click the address bar, type `powershell`, and press Enter.

Then install the packages:

```
uv sync
```

This downloads Python if you need it, creates a `.venv` folder inside the kit, and installs the exact package versions listed in `uv.lock`. Nothing outside the kit folder changes.

### 5. Verify

```
uv run python verify_setup.py
```

You should see **All checks PASSED**. If anything FAILS, follow the `fix:` hint under it. If that doesn't work, reply to the pre-work email and paste the whole output.

Finally, run `claude` in the kit folder once and sign in, so that sign-in is not something you have to do during the session. Type `/exit` to quit.

### Troubleshooting

| Problem | Fix |
|---|---|
| `claude: command not found` / not recognized | Open a **new** terminal. If it still fails, rerun the installer and follow its PATH message. See https://code.claude.com/docs/en/troubleshooting |
| `uv: command not found` / not recognized | Open a **new** terminal. If it still fails, rerun the installer and follow its PATH message |
| `uv sync` fails building pandas or numpy | Your Python is too new for prebuilt packages. Run `uv sync --python 3.13` |
| `verify_setup.py` says a package is missing | You ran plain `python`. Run `uv run python verify_setup.py` instead |
| Windows PowerShell says running scripts is disabled | Use the exact installer command above; `-ExecutionPolicy ByPass` applies only to that one command |
| Claude asks you to log in every time, or login fails | Check with IT which account type you have (see step 1). Run `/logout`, then sign in again |
| Corporate or university proxy blocks sign-in | Ask IT. Claude Code supports `HTTPS_PROXY`; see the setup docs |
| "Permission denied" writing files | Move the kit out of a read-only or synced folder, for example to Documents |

## Tutorial

1. Open a terminal in this folder.
2. Run `uv run python verify_setup.py`.
3. Run `claude`.
4. Open `prompts.md` and copy prompts from it as we go.

## What's here

| File or folder | What it is |
|---|---|
| `prompts.md` | Every prompt we use, in order. |
| `CLAUDE.md` | Project rules Claude reads automatically. |
| `data/` | Raw NASA GISTEMP data. Never edited. |
| `outputs/` | Everything you and Claude make goes here. |
| `checkpoints/` | Reference results for each stage, if you fall behind. |
| `mcp/` | A small read-only database server for Stage 5. |
| `verify_setup.py` | Checks your setup. |
| `pyproject.toml`, `uv.lock` | The Python packages this kit uses. `uv sync` installs them. |

## Three things to know

- **Your results will differ** from your neighbor's and from the screen. Claude writes new code each time. That's fine.
- **Fallen behind?** Every stage in `prompts.md` has a "Stuck?" prompt that copies the checkpoint into `outputs/`.
- **Claude asks permission** before running commands or editing files. Read what it wants to do, then approve. That habit is part of the lesson.

## The five stages

Setup check, then **plan**, **explore**, **graph**, **3D**, and **MCP**, then apply it to your own research.
