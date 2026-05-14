"""docrest command-line interface."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from docrest import __version__
from docrest.converters import ConversionError, convert as run_convert, supported_pairs
from docrest.core.detect import detect_tools
from docrest.core.install import InstallError, recipe_for, run_recipe

app = typer.Typer(
    add_completion=False,
    help="Convert documentation between formats (md, txt, docx, pdf, html, mermaid, plantuml).",
)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(f"docrest {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        callback=_version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """docrest: documentation format converter."""


@app.command()
def convert(
    source: Path = typer.Argument(..., exists=True, readable=True, help="Input file."),
    target: Path = typer.Argument(..., help="Output file."),
    src_fmt: Optional[str] = typer.Option(None, "--from", help="Override source format."),
    dst_fmt: Optional[str] = typer.Option(None, "--to", help="Override target format."),
) -> None:
    """Convert SOURCE into TARGET. Formats inferred from file extensions."""
    try:
        out = run_convert(source, target, src_fmt=src_fmt, dst_fmt=dst_fmt)
    except (ConversionError, ValueError) as exc:
        console.print(f"[red]error:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    console.print(f"[green]wrote[/green] {out}")


@app.command()
def formats() -> None:
    """List supported (source -> target) format pairs."""
    table = Table(title="Supported conversions")
    table.add_column("source")
    table.add_column("target")
    for src, dst in supported_pairs():
        table.add_row(src, dst)
    console.print(table)


def _print_tool_table(statuses) -> None:
    table = Table(title="External tools")
    table.add_column("tool")
    table.add_column("available")
    table.add_column("path")
    table.add_column("version")
    for name, status in statuses.items():
        table.add_row(
            name,
            "yes" if status.available else "no",
            status.path or "-",
            status.version or "-",
        )
    console.print(table)


def _install_tool(name: str, *, assume_yes: bool) -> bool:
    recipe = recipe_for(name)
    if recipe is None:
        console.print(f"[yellow]no install recipe for {name} on this platform[/yellow]")
        return False
    note = f" ({recipe.note})" if recipe.note else ""
    console.print(
        f"[cyan]install {name}[/cyan] via [bold]{recipe.manager}[/bold]: "
        f"`{' '.join(recipe.command)}`{note}"
    )
    if not assume_yes and not typer.confirm(f"run installer for {name}?", default=False):
        console.print(f"[yellow]skipped {name}[/yellow]")
        return False
    try:
        run_recipe(recipe)
    except InstallError as exc:
        console.print(f"[red]install failed for {name}:[/red] {exc}")
        return False
    console.print(f"[green]installed {name}[/green]")
    return True


@app.command("detect")
@app.command("doctor", hidden=True)
def detect(
    install: bool = typer.Option(
        False,
        "--install",
        help="Offer to install missing external tools using the platform package manager.",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompts when used with --install.",
    ),
) -> None:
    """Show availability of optional external binaries. Optionally install missing ones."""
    statuses = detect_tools()
    _print_tool_table(statuses)

    if not install:
        missing = [name for name, status in statuses.items() if not status.available]
        if missing:
            console.print(
                f"\n[dim]missing: {', '.join(missing)}. "
                f"Run [bold]docrest doctor --install[/bold] to install.[/dim]"
            )
        return

    missing = [name for name, status in statuses.items() if not status.available]
    if not missing:
        console.print("[green]all external tools already available[/green]")
        return

    console.print(f"\n[bold]missing tools:[/bold] {', '.join(missing)}")
    installed_any = False
    for name in missing:
        if _install_tool(name, assume_yes=yes):
            installed_any = True

    if installed_any:
        console.print("\n[bold]re-running detection:[/bold]")
        _print_tool_table(detect_tools())


@app.command("install")
def install_cmd(
    tools: list[str] = typer.Argument(
        None,
        help="Tools to install. Omit to install all missing ones.",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts."),
) -> None:
    """Install optional external tools (pandoc, mmdc, plantuml, weasyprint runtime)."""
    statuses = detect_tools()
    known = list(statuses.keys())

    if not tools:
        targets = [name for name, status in statuses.items() if not status.available]
        if not targets:
            console.print("[green]nothing to install — all tools already available[/green]")
            return
    else:
        unknown = [t for t in tools if t not in known]
        if unknown:
            console.print(
                f"[red]unknown tool(s):[/red] {', '.join(unknown)}. "
                f"Known: {', '.join(known)}."
            )
            raise typer.Exit(code=1)
        targets = tools

    failures: list[str] = []
    for name in targets:
        if not _install_tool(name, assume_yes=yes):
            failures.append(name)

    console.print("\n[bold]post-install state:[/bold]")
    _print_tool_table(detect_tools())

    if failures:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
