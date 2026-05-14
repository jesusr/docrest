"""Install recipes for optional external tools."""
from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class InstallRecipe:
    tool: str
    manager: str
    command: list[str]
    note: str = ""


def _macos_recipe(tool: str) -> InstallRecipe | None:
    mapping = {
        "pandoc": InstallRecipe("pandoc", "brew", ["brew", "install", "pandoc"]),
        "plantuml": InstallRecipe(
            "plantuml",
            "brew",
            ["brew", "install", "plantuml"],
            note="requires a Java runtime",
        ),
        "weasyprint": InstallRecipe(
            "weasyprint",
            "brew",
            ["brew", "install", "pango"],
            note="installs pango/cairo runtime libraries used by weasyprint",
        ),
        "mmdc": InstallRecipe(
            "mmdc",
            "npm",
            ["npm", "install", "-g", "@mermaid-js/mermaid-cli"],
        ),
    }
    return mapping.get(tool)


def _linux_recipe(tool: str) -> InstallRecipe | None:
    mapping = {
        "pandoc": InstallRecipe("pandoc", "apt", ["sudo", "apt-get", "install", "-y", "pandoc"]),
        "plantuml": InstallRecipe(
            "plantuml",
            "apt",
            ["sudo", "apt-get", "install", "-y", "plantuml"],
        ),
        "weasyprint": InstallRecipe(
            "weasyprint",
            "apt",
            [
                "sudo",
                "apt-get",
                "install",
                "-y",
                "libpango-1.0-0",
                "libpangoft2-1.0-0",
            ],
            note="installs pango runtime used by weasyprint",
        ),
        "mmdc": InstallRecipe(
            "mmdc",
            "npm",
            ["npm", "install", "-g", "@mermaid-js/mermaid-cli"],
        ),
    }
    return mapping.get(tool)


def recipe_for(tool: str) -> InstallRecipe | None:
    system = platform.system()
    if system == "Darwin":
        return _macos_recipe(tool)
    if system == "Linux":
        return _linux_recipe(tool)
    return None


class InstallError(RuntimeError):
    """Raised when installation cannot proceed."""


def run_recipe(recipe: InstallRecipe) -> None:
    if not shutil.which(recipe.command[0]):
        raise InstallError(
            f"package manager '{recipe.command[0]}' not found on PATH; install it first"
        )
    completed = subprocess.run(recipe.command, check=False)
    if completed.returncode != 0:
        raise InstallError(
            f"installer exited with code {completed.returncode}: {' '.join(recipe.command)}"
        )
