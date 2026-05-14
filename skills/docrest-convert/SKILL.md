---
name: docrest-convert
description: Convert documentation files between md, txt, docx, pdf, and html using the docrest CLI. Use when the user asks to transform a documentation file from one format to another (e.g. "turn this docx into markdown", "export README to pdf").
---

# docrest-convert

Convert documentation between common formats using the `docrest` CLI.

## When to use

- User provides a source file path and an output format (or output path) for documentation: `md`, `txt`, `docx`, `pdf`, `html`.
- User asks to "convert", "export", or "render" a documentation file.

Do **not** use for diagrams (Mermaid/PlantUML) — use `docrest-diagram` instead.

## Supported pairs

| source | targets               |
|--------|-----------------------|
| md     | txt, html, docx, pdf  |
| txt    | md, docx, pdf         |
| docx   | md, txt, pdf          |
| pdf    | txt, md               |

Run `docrest formats` for the live list.

## Usage

1. Confirm source path exists and target extension is supported.
2. Run:
   ```bash
   docrest convert <source> <target>
   ```
3. Override format detection when needed:
   ```bash
   docrest convert input.dat output.md --from txt --to md
   ```
4. If conversion fails with a missing-binary error, run `docrest detect` and surface which external tool (`pandoc`, `weasyprint`) needs installing.

## Notes

- `md ↔ docx` and `docx → pdf` require `pandoc` on PATH.
- `*.pdf` output requires `weasyprint`.
- Output directories are created automatically.
