#!/usr/bin/env python3
"""Validate a submission directory and pack it into a deterministic submission.zip.

Mirrors the checks in the official harness (adk_submission.validate_directory and
the Getting Started notebook) so problems surface before burning a daily slot:
root config present, allowed extensions only, no symlinks, size < 3 GiB,
!include paths resolve inside the root, exactly one allowed model, only harness
tools, referenced adapters exist, and a rough 12-hour runtime estimate.

Usage: python scripts/build_submission.py submissions/v1 [-o dist/v1/submission.zip]
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

import yaml

ALLOWED_EXT = {".yaml", ".yml", ".md", ".txt", ".py", ".json", ".safetensors"}
ROOT_NAMES = ("agent.yaml", "root_agent.yaml")
MAX_BYTES = 3 * 1024**3
ALLOWED_MODELS = {
    "gemma-4-31b-it-qat-w4a16-ct",
    "gemma-4-12b-it-qat-w4a16-ct",
    "gemma-4-e4b-it-qat-w4a16-ct",
    "gemma-4-e2b-it-qat-w4a16-ct",
}
HARNESS_TOOLS = {
    "run_command", "submit_patch", "get_status", "read_file", "edit_file",
    "write_file", "get_code_neighbors", "search_similar_code", "get_code_subgraph",
}
FORBIDDEN_GEN_KEYS = {"tools", "system_instruction", "http_options", "safety_settings", "response_schema"}
TASKS = 120            # ~60 public + ~60 private
TOTAL_MIN = 12 * 60
OVERHEAD_MIN = 20 + TASKS * 1.0   # vLLM start (<=20 min) + ~1 min sandbox setup per task (guess)


class Error(Exception):
    pass


def make_loader(root: Path):
    class Loader(yaml.SafeLoader):
        pass

    def include(loader: Loader, node: yaml.Node):
        rel = loader.construct_scalar(node)
        base = Path(loader.name).parent
        if Path(rel).is_absolute():
            raise Error(f"!include must be a relative path: {rel}")
        target = (base / rel).resolve()
        if root not in target.parents:
            raise Error(f"!include escapes submission root: {rel}")
        if not target.is_file():
            raise Error(f"!include target missing: {rel} (from {base})")
        if target.suffix in (".yaml", ".yml"):
            return load_yaml(target, root)
        return target.read_text(encoding="utf-8")

    Loader.add_constructor("!include", include)
    return Loader


def load_yaml(path: Path, root: Path):
    with path.open(encoding="utf-8") as fh:
        loader = make_loader(root)(fh)
        loader.name = str(path)
        try:
            return loader.get_single_data()
        finally:
            loader.dispose()


def walk_agents(cfg: dict, base: Path, root: Path, out: list):
    out.append(cfg)
    for tool in cfg.get("tools") or []:
        if isinstance(tool, dict) and "agent_tool" in tool:
            p = (base / tool["agent_tool"]["config_path"]).resolve()
            walk_agents(load_yaml(p, root), p.parent, root, out)
        elif isinstance(tool, dict) and "name" in tool:
            walk_agents(tool, base, root, out)
    for sub in cfg.get("sub_agents") or []:
        if isinstance(sub, dict) and "config_path" in sub:
            p = (base / sub["config_path"]).resolve()
            walk_agents(load_yaml(p, root), p.parent, root, out)
        elif isinstance(sub, dict):
            walk_agents(sub, base, root, out)


def validate(root: Path) -> list[Path]:
    root = root.resolve()
    files, total = [], 0
    for p in sorted(root.rglob("*")):
        if p.is_symlink():
            raise Error(f"symlink not allowed: {p.relative_to(root)}")
        if p.is_file():
            if p.suffix.lower() not in ALLOWED_EXT:
                raise Error(f"disallowed extension: {p.relative_to(root)}")
            total += p.stat().st_size
            files.append(p)
    if total > MAX_BYTES:
        raise Error(f"submission too large: {total} bytes")
    roots = [root / n for n in ROOT_NAMES if (root / n).is_file()]
    if len(roots) != 1:
        raise Error(f"need exactly one root config of {ROOT_NAMES}, found {roots}")

    agents: list[dict] = []
    walk_agents(load_yaml(roots[0], root), root, root, agents)
    models = {a.get("model") for a in agents if a.get("model")}
    models = {m.split("/")[-1] for m in models}
    if len(models) != 1 or not models <= ALLOWED_MODELS:
        raise Error(f"exactly one allowed model required, found {models}")
    for a in agents:
        name = a.get("name", "?")
        for t in a.get("tools") or []:
            if isinstance(t, str) and t not in HARNESS_TOOLS:
                raise Error(f"agent {name}: unknown tool {t!r}")
        ad = a.get("adapter")
        if ad and not (root / "adapters" / ad / "adapter_model.safetensors").is_file():
            raise Error(f"agent {name}: adapter {ad!r} missing under adapters/")
        gen = a.get("generate_content_config") or {}
        bad = FORBIDDEN_GEN_KEYS & set(gen)
        if bad:
            raise Error(f"agent {name}: forbidden generate_content_config keys {bad}")
        tc = gen.get("thinking_config") or {}
        if "thinking_level" in tc:
            print(f"WARN agent {name}: thinking_level is ignored/mis-mapped on vLLM; use thinking_budget")
        if int(gen.get("max_output_tokens", 16384)) > 32768:
            raise Error(f"agent {name}: max_output_tokens > 32768")
        if not a.get("instruction"):
            print(f"WARN agent {name}: empty instruction")
    if (root / "adapters").is_dir() and "gemma-4-31b-it-qat-w4a16-ct" not in models:
        print("WARN adapters/ present with non-31B model: make sure the LoRA shapes match")

    print(f"OK  {len(files)} files, {total/1e6:.2f} MB, model={models.pop()}, agents={len(agents)}")
    budget_report(root)
    return files


def budget_report(root: Path):
    ec = root / "eval_config.yaml"
    if not ec.is_file():
        print("WARN no eval_config.yaml: scorer defaults (60 min/task) will blow the 12 h limit")
        return
    cfg = yaml.safe_load(ec.read_text()) or {}
    ev = cfg.get("evaluation", cfg)
    cap = float(ev.get("max_time_minutes", 60))
    worst = OVERHEAD_MIN + TASKS * cap
    print(f"    budget: max_time_minutes={cap}, max_tool_calls={ev.get('max_tool_calls')}, "
          f"worst case ~{worst/60:.1f} h of 12 h (overhead guess {OVERHEAD_MIN:.0f} min)")
    if worst > TOTAL_MIN:
        avg_ok = (TOTAL_MIN - OVERHEAD_MIN) / TASKS
        print(f"    NOTE: fits only if the average task takes <= {avg_ok:.1f} min")


def pack(root: Path, files: list[Path], out: Path):
    out.parent.mkdir(parents=True, exist_ok=True)
    root = root.resolve()
    with zipfile.ZipFile(out, "w") as zf:
        for p in files:
            info = zipfile.ZipInfo(p.relative_to(root).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, p.read_bytes())
    print(f"    wrote {out} ({out.stat().st_size} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("submission_dir", type=Path)
    ap.add_argument("-o", "--out", type=Path)
    args = ap.parse_args()
    out = args.out or Path("dist") / args.submission_dir.name / "submission.zip"
    try:
        files = validate(args.submission_dir)
    except Error as e:
        sys.exit(f"FAIL {e}")
    pack(args.submission_dir, files, out)


if __name__ == "__main__":
    main()
