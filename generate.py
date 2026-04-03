#!/usr/bin/env python3
"""Generate plugin READMEs and marketplace README from skill/agent/hook metadata."""

import json
from pathlib import Path

import frontmatter
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

console = Console()
ROOT = Path(__file__).parent


class SkillMetadata(BaseModel):
    name: str
    description: str
    version: str = ""


class AgentMetadata(BaseModel):
    name: str
    description: str
    model: str = "inherit"
    color: str = ""
    tools: list[str] = []


def scan_subdir(parent: Path, subdir_name: str, relative_to: Path) -> list[dict]:
    subdir = parent / subdir_name
    if not subdir.exists():
        return []
    return [
        {"name": f.name, "path": str(f.relative_to(relative_to))}
        for f in sorted(subdir.iterdir())
        if not f.name.startswith(".")
    ]


def scan_skill(skill_dir: Path, plugin_dir: Path) -> dict | None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None
    post = frontmatter.load(skill_md)
    meta = SkillMetadata(**post.metadata)
    return {
        **meta.model_dump(),
        "dir_name": skill_dir.name,
        "plugin_path": str(skill_md.relative_to(plugin_dir)),
        "root_path": str(skill_md.relative_to(ROOT)),
        "references": scan_subdir(skill_dir, "references", plugin_dir),
        "scripts": scan_subdir(skill_dir, "scripts", plugin_dir),
        "examples": scan_subdir(skill_dir, "examples", plugin_dir),
        "root_references": scan_subdir(skill_dir, "references", ROOT),
        "root_scripts": scan_subdir(skill_dir, "scripts", ROOT),
        "root_examples": scan_subdir(skill_dir, "examples", ROOT),
    }


def scan_agent(agent_file: Path, plugin_dir: Path) -> dict | None:
    post = frontmatter.load(agent_file)
    meta = AgentMetadata(**post.metadata)
    return {
        **meta.model_dump(),
        "plugin_path": str(agent_file.relative_to(plugin_dir)),
        "root_path": str(agent_file.relative_to(ROOT)),
    }


def scan_hook(hook_file: Path, plugin_dir: Path) -> dict:
    post = frontmatter.load(hook_file)
    return {
        "name": post.metadata.get("name", hook_file.stem),
        "description": post.metadata.get("description", ""),
        "plugin_path": str(hook_file.relative_to(plugin_dir)),
        "root_path": str(hook_file.relative_to(ROOT)),
    }


def scan_plugin(plugin_dir: Path) -> dict:
    plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
    meta = (
        json.loads(plugin_json.read_text())
        if plugin_json.exists()
        else {"name": plugin_dir.name, "description": "", "version": "0.0.0"}
    )

    skills = []
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir() and not d.name.startswith("."):
                s = scan_skill(d, plugin_dir)
                if s:
                    skills.append(s)

    agents = []
    agents_dir = plugin_dir / "agents"
    if agents_dir.exists():
        for f in sorted(agents_dir.glob("*.md")):
            a = scan_agent(f, plugin_dir)
            if a:
                agents.append(a)

    hooks = []
    hooks_dir = plugin_dir / "hooks"
    if hooks_dir.exists():
        for f in sorted(hooks_dir.glob("*.md")):
            hooks.append(scan_hook(f, plugin_dir))

    return {
        "dir_name": plugin_dir.name,
        "meta": meta,
        "skills": skills,
        "agents": agents,
        "hooks": hooks,
    }


def main():
    plugins = []

    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        if d.name == "templates":
            continue
        has_plugin = (d / ".claude-plugin" / "plugin.json").exists()
        has_skills = (d / "skills").exists()
        if has_plugin or has_skills:
            plugins.append(scan_plugin(d))

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["oneline"] = lambda s: " ".join(s.split()) if s else ""

    plugin_tpl = env.get_template("plugin.md")
    marketplace_tpl = env.get_template("marketplace.md")

    # Phase 1: generate plugin READMEs (leaves)
    for plugin in plugins:
        content = plugin_tpl.render(plugin=plugin)
        (ROOT / plugin["dir_name"] / "README.md").write_text(content)

    # Phase 2: generate marketplace README (root)
    total_skills = sum(len(p["skills"]) for p in plugins)
    total_agents = sum(len(p["agents"]) for p in plugins)
    total_hooks = sum(len(p["hooks"]) for p in plugins)

    marketplace_json = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace_meta = (
        json.loads(marketplace_json.read_text()) if marketplace_json.exists() else {}
    )

    marketplace = marketplace_tpl.render(
        plugins=plugins,
        marketplace=marketplace_meta,
        total_skills=total_skills,
        total_agents=total_agents,
        total_hooks=total_hooks,
    )
    (ROOT / "README.md").write_text(marketplace)

    # Summary
    console.print(
        f"\n[green]✓ Generated {len(plugins)} plugin READMEs + marketplace README[/green]"
    )
    console.print(
        f"[dim]  {total_skills} skills, {total_agents} agents, {total_hooks} hooks[/dim]"
    )

    table = Table(show_header=True, box=None, padding=(0, 2))
    table.add_column("Plugin")
    table.add_column("Skills", justify="right")
    table.add_column("Agents", justify="right")
    table.add_column("Version")

    for p in plugins:
        table.add_row(
            p["dir_name"],
            str(len(p["skills"])),
            str(len(p["agents"])),
            p["meta"].get("version", "-"),
        )

    console.print(table)
    console.print()


if __name__ == "__main__":
    main()
