# docrest

CLI + Claude Code skills to convert documentation between formats: `md`, `txt`, `docx`, `pdf`, `html`, and diagrams (Mermaid `.mmd`, PlantUML `.puml`).

Pure-Python core, with optional external tools (`pandoc`, `weasyprint` runtime libs, `mmdc`, `plantuml`) for richer conversions. `docrest doctor` detects what's available and can install what's missing.

## Install

```bash
git clone <repo> docrest && cd docrest
python3.13 -m venv .venv
.venv/bin/pip install -e ".[dev]"
# now `.venv/bin/docrest` is on PATH inside the venv
```

Requires Python ≥ 3.10.

## Optional external tools

Auto-detected — install only what you need. `docrest doctor --install` handles it for you.

| Tool | Used for | macOS recipe | Linux recipe |
|------|----------|--------------|--------------|
| `pandoc` | md ↔ docx, docx → md, docx → pdf | `brew install pandoc` | `apt-get install pandoc` |
| `weasyprint` runtime (pango/cairo) | any PDF output | `brew install pango` | `apt-get install libpango-1.0-0 libpangoft2-1.0-0` |
| `mmdc` | Mermaid → svg/png/pdf | `npm i -g @mermaid-js/mermaid-cli` | same |
| `plantuml` | PlantUML → svg/png/pdf | `brew install plantuml` | `apt-get install plantuml` |

## Usage

### Inspect environment

```bash
docrest --version
docrest formats                # list every supported (src -> dst) pair
docrest doctor                 # show external tool availability (alias: detect)
```

### Install missing tools from the CLI

```bash
docrest doctor --install       # prompt-confirm install of each missing tool
docrest doctor --install -y    # install all missing tools without prompting

docrest install                # same as `doctor --install`, but installer-focused
docrest install pandoc mmdc    # install specific tools
docrest install -y pandoc      # no confirmation prompt
```

Recipes use the platform package manager (`brew` on macOS, `apt-get` on Linux; `npm` for `mmdc` on both). On Linux, `apt-get` recipes call `sudo` and will prompt for your password. On unsupported platforms `docrest` prints the recipe but does not run anything.

### Convert files

```bash
# Format inferred from file extensions
docrest convert README.md README.html
docrest convert notes.docx notes.md
docrest convert report.pdf report.txt
docrest convert diagram.mmd diagram.svg

# Override format detection
docrest convert weird.dat out.md --from txt --to md
```

Output directories are created automatically. Errors (missing binary, unsupported pair) exit with code 1 and print a single-line `error: …` message.

## Supported conversions

Run `docrest formats` for the live list. As of now:

| Source | Targets |
|--------|---------|
| `md` | `txt`, `html`, `docx`, `pdf` |
| `txt` | `md`, `docx`, `pdf` |
| `docx` | `md`, `txt`, `pdf` |
| `pdf` | `txt`, `md` |
| `mmd` (Mermaid) | `svg`, `png`, `pdf` |
| `puml` (PlantUML) | `svg`, `png`, `pdf` |

## Claude Code skills

Two skills ship under `skills/`. Symlink them into `~/.claude/skills/` (or your project's `.claude/skills/`) to expose them to Claude Code:

- [`docrest-convert`](skills/docrest-convert/SKILL.md) — generic documentation conversions (md / txt / docx / pdf / html).
- [`docrest-diagram`](skills/docrest-diagram/SKILL.md) — Mermaid + PlantUML rendering.

```bash
ln -s "$(pwd)/skills/docrest-convert" ~/.claude/skills/docrest-convert
ln -s "$(pwd)/skills/docrest-diagram" ~/.claude/skills/docrest-diagram
```

## Tests

```bash
.venv/bin/pytest -v
```

19 tests cover format detection, the converter registry, Markdown rendering, docx ↔ txt round-trip, and the CLI.

## Layout

```text
src/docrest/
  cli.py                  # Typer entrypoint (convert, formats, doctor, install)
  core/
    detect.py             # External tool probes + extension -> format inference
    install.py            # Per-platform install recipes
  converters/
    base.py               # Converter protocol + ConversionError
    registry.py           # (src, dst) -> converter dispatch
    markdown.py           # md -> txt/html/docx/pdf
    docx.py               # docx <-> md/txt/pdf
    pdf.py                # pdf -> txt/md
    txt.py                # txt -> pdf
    diagrams.py           # mmd/puml -> svg/png/pdf
skills/
  docrest-convert/SKILL.md
  docrest-diagram/SKILL.md
examples/
  sample.md
  sample.mmd
tests/
  test_detect.py
  test_registry.py
  test_markdown.py
  test_docx_txt.py
  test_cli.py
```

## License

MIT.
