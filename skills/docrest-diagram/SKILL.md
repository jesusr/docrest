---
name: docrest-diagram
description: Render Mermaid (.mmd) or PlantUML (.puml) diagram sources into SVG, PNG, or PDF using the docrest CLI. Use when the user asks to render, export, or compile a diagram source file.
---

# docrest-diagram

Render diagram source files to image formats.

## When to use

- Input file is a Mermaid (`.mmd`, `.mermaid`) or PlantUML (`.puml`, `.plantuml`) source.
- User wants `svg`, `png`, or `pdf` output.

For prose documentation conversions use `docrest-convert`.

## Supported pairs

| source | targets        |
|--------|----------------|
| mmd    | svg, png, pdf  |
| puml   | svg, png, pdf  |

## Usage

```bash
docrest convert diagram.mmd diagram.svg
docrest convert architecture.puml architecture.png
```

## External requirements

- Mermaid: `mmdc` (`npm install -g @mermaid-js/mermaid-cli`).
- PlantUML: `plantuml` binary (and Java runtime).

Run `docrest detect` to verify both are on PATH before attempting conversion. If the binary is missing, instruct the user to install it; do not attempt to fall back silently.
