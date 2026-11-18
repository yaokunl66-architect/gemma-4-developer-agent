# Google – The Gemma 4 Developer Agent Competition: Full Context for Claude Code

> Scraped from https://www.kaggle.com/competitions/gemma-4-developer-agent on **2026-11-17** (≈15 days before the final deadline).
> Covers: Overview, Data, Rules, the official Getting Started notebook (code verbatim), a public LB-0.22 reference submission (verbatim), key discussion threads (staff announcements + community experiments), and leaderboard/notebook snapshots.
>
> **Download separately and keep next to this file:** `HARNESS_README.md` (55.9 kB, the authoritative harness guide — §9 below digests it), `sample_submission/`, `tasks.jsonl`. When this file and HARNESS_README.md disagree, trust HARNESS_README.md.

---

## 0. TL;DR for the agent

- **Task:** build a SWE-bench-style coding agent on **Gemma 4** (post-training allowed via LoRA) that resolves real Python issues. Score = % of tasks whose submitted patch passes hidden tests (PASS/FAIL per task).
- **Deliverable:** `submission.zip` with `agent.yaml` at root (Google ADK Agent Config YAML) + optional prompts, configs, sub-agents, LoRA adapters, skills, `eval_config.yaml`.
- **Allowed base models (exactly one per submission):** `gemma-4-31b-it-qat-w4a16-ct`, `gemma-4-12b-it-qat-w4a16-ct`, `gemma-4-e4b-it-qat-w4a16-ct`, `gemma-4-e2b-it-qat-w4a16-ct`. Different LoRA adapters per agent are allowed.
- **Runtime:** 12 h total for ~60 public / ~60 private test tasks (≈120 total; public LB has exactly 58 tasks) on Kaggle **4×L4** (96 GB), vLLM with tensor_parallel=4, max_model_len 32768, no internet. Budget ≈ **5.5 min/task**.
- **Limits:** 1 submission/day, 2 final selections, team ≤5, one pending submission at a time (queue can be >24 h).
- **Deadlines (23:59 UTC):** entry & team merger **2026-11-25**; final submission **2026-12-02**.
- **Prizes:** main $37k/$18k/$10k; $10k bonus for best E2B/E4B submission; separate paper track $35k.
- **Current public LB (2026-11-17):** #1 = 0.29, #2–15 = 0.24, many at 0.22. Best public notebooks ≈ 0.22 without training.
- **What community found:** keep thinking + thought summaries on; graph tools (`search_similar_code`, etc.) gave no benefit; 31B ≫ 12B ≫ E4B; ~8 min / ~28–50 tool calls per task works; force an edit early (an unedited tree scores 0; a working-tree edit counts even without `submit_patch`).

---

## 1. Overview page (verbatim)

**Host:** Google DeepMind · Featured Prediction Competition
**Tagline:** Accelerate research in autonomous coding agents

Today’s best coding agents rely on massive API models running in the cloud. What if every developer could rely on an autonomous agent equally capable offline, on consumer hardware?

Post-train an open model into a reliable agent that navigates complex codebases and drafts fixes for real software issues, accelerating developer workflows on everyday hardware.

### Description

Note: there are two active competitions for the Gemma 4 Developer Agent Competition: this competition, and a paper track, where you can document your approach for this prediction competition.

Today’s most capable coding agents rely on internet-connected models that require powerful commercial infrastructure. That puts advanced software engineering out of reach for many developers.

Small local models have made rapid progress, but they still struggle with complex, multi-turn software engineering. Large codebases are hard to navigate, so fixing bugs and adding features reliably is tough for models that fit on a single accelerator.

In this competition, you’ll post-train Gemma 4 to build autonomous software engineering agents designed to amplify developers’ talents. You’ll explore new fine-tuning and reinforcement learning techniques to create agents that can independently navigate repositories and draft solutions, freeing up human engineers to focus on architecture, logic, and review.

Your solution could help put powerful coding assistants in the hands of millions more developers. Sharing how you did it makes advanced coding tools accessible to everyone.

### Evaluation

You must provide a zip archive (`submission.zip`) that contains your Agent Config, comprising system prompts, custom tools, skills, and LoRA adapters. An `agent.yaml` file must be located at the root of the archive.

```
submission.zip
├── agent.yaml                  # REQUIRED: Root agent config
├── configs/
│   └── sampling.yaml           # Optional: Generation parameters loaded via !include
├── prompts/
│   ├── system.md               # Optional: System instructions loaded via !include
│   └── analyzer.md
├── sub_agents/
│   └── code_analyzer.yaml      # Optional: Sub-agent or AgentTool YAML configurations
├── adapters/                   # Optional: Fine-tuned PEFT LoRA adapters or model weights
│   ├── main_lora/
│   │   ├── adapter_config.json
│   │   └── adapter_model.safetensors
│   └── tool_lora/
│       ├── adapter_config.json
│       └── adapter_model.safetensors
└── skills/                     # Optional: ADK Skill directories
    └── repo_navigation/
        ├── SKILL.md
        ├── scripts/            # Python or bash scripts executed in a sandbox
        └── resources/          # Domain knowledge markdown files
```

The config language follows the Google ADK Agent Config specification with additional restrictions to prevent code execution outside of a sandbox. The submissions themselves are compiled into ADK agents to be evaluated.

**Issue Scoring.** Similar to SWE-Bench, your agent's submitted patches are evaluated by a PASS/FAIL metric. For each issue, the submitted patch is applied to that issue's code repository and that issue's validation tests are run. Your submission's overall score is the percentage of patched repositories that pass the validation tests.

Your agent has a limit of 12 hours to submit patches for all tasks, inclusive of sandbox setup time, but excluding time for patch validation. You may, but are not required, to set per-task time limits in your submission's `eval_config.yaml`.

### Timeline

- September 23, 2026 – Start Date.
- November 12, 2026 (optional) – Deadline to submit Research Paper.
- November 25, 2026 – Entry Deadline. You must accept the competition rules before this date in order to compete.
- November 25, 2026 – Team Merger Deadline.
- December 2, 2026 – Final Submission Deadline.

All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted.

### Prizes

Total Prizes Available: $110,000

**Main competition: $65,000** — 1st $37,000 · 2nd $18,000 · 3rd $10,000

**Paper Submission Award: $35,000.** Original, unpublished research on topics including:
- Tuning & Optimization: PEFT and RL approaches tailored to improve SWE agent capabilities.
- Code Comprehension: code-graph generation, parsing, and embedding for deep comprehension of complex repositories.
- Tasks & Benchmarks: new tasks, evaluation datasets, or resources targeting code structure, graphs, and structured code generation.
- Graph Reasoning: improving LLM reasoning over large-scale graphs.
(Sign up for the paper track separately; paper deadline Nov 12, 2026 23:59 UTC.)

**Bonus Prize: Small Model Development: $10,000** — to the highest-ranking submission using **Gemma E2B or Gemma E4B** as base model. Must be one of the team’s two selected final submissions. LoRA fine-tuning allowed. Scored on private test set; same tie-breaking. A separate daily-updated Kaggle notebook shows filtered standings. Remains eligible for the main leaderboard and paper track.

### Model Selection, Budget, and Harness Rules

**Model Selection and LoRA Adapters.** Supported variants:
- `gemma-4-31b-it-qat-w4a16-ct`
- `gemma-4-12b-it-qat-w4a16-ct`
- `gemma-4-e4b-it-qat-w4a16-ct`
- `gemma-4-e2b-it-qat-w4a16-ct`

Every agent and subagent in your submission must use the same model. You may include one or more `.safetensors` LoRA adapters; different adapters per agent are allowed:
- Place PEFT LoRA directories (containing `adapter_config.json` and `adapter_model.safetensors`) inside `adapters/<adapter_name>/`.
- Reference `adapter: <adapter_name>` on any LlmAgent in `agent.yaml` or `sub_agents/*.yaml` (e.g. `adapter: main_lora` on the root coder agent and `adapter: tool_lora` on a read-only analyzer AgentTool).

**Tool, Prompt, and Skill Rules**
- `!include` resolves file paths relative to the directory of the file containing the tag (e.g. in `agent.yaml`, `!include prompts/system.md`).
- Sandboxing: path traversal outside the submission root (`../`, symlinks) is not allowed.
- Allowed tools: only tools provided by the harness, or custom subagents defined via `agent_tool`.
- Skills: each skill is a directory with a `SKILL.md` manifest with YAML frontmatter (`name: <skill-name>`). Scripts run via `run_skill_script` inside the competition's persistent Docker container, sharing filesystem with `run_command` and debiting the central time budget. Agents read knowledge files via `load_skill_resource`.

**Predefined tools:**
```
run_command(command: str) -> str                      # /bin/bash -c inside /workspace
submit_patch() -> str                                 # git add -N . ; captures git diff HEAD from /workspace
get_status() -> str                                   # live budget consumption + patch status
read_file(filepath: str, start_line: int|None=None, end_line: int|None=None) -> str   # 1-indexed inclusive
edit_file(filepath: str, old_string: str, new_string: str, allow_multiple: bool=False) -> str
write_file(filepath: str, content: str) -> str        # creates/overwrites, mkdir -p parents
get_code_neighbors(node: str, edge_type: str|None=None, max_neighbors: int=50) -> str
search_similar_code(query: str, k: int=10) -> str     # cosine similarity over precomputed embeddings
get_code_subgraph(nodes: list[str]) -> str            # induced subgraph
```
See `HARNESS_README.md` in the dataset for details.

### Upgraded Accelerators
Access to Kaggle **L4×4** machines (96 GB GPU memory). L4×4 notebooks consume GPU quota at 2× the rate of T4×2/P100. L4s are only for notebooks attached to this competition. **All L4 sessions must have internet disabled.**

### Stats (2026-11-17)
17,243 entrants · 6,755 participants · 6,009 teams · 50,997 submissions. Tags: AI, Coding, Custom Metric.

---

## 2. Data page (verbatim)

This competition evaluates AI software engineering agents on their ability to solve real-world Python bug fixes and feature requests.

To assist agents in large codebase navigation, dependency understanding, and semantic retrieval, the competition provides code graphs, graph/node embeddings, and specialized graph tools alongside traditional repository exploration mechanisms.

Participants are provided with a training set (tasks, code graphs, embeddings) for local agent development, prompt engineering, and offline validation. Submissions are evaluated against a test set curated under a similar pipeline, with identical graph generation methods and verification standards. In this public-facing dataset you only see the training set; at scoring time it is replaced with the hidden test set.

**Size:** 524 files, 22.42 GB, Apache 2.0. Top-level: `docker/ embeddings/ graphs/ sample_submission/ sandbox/ snapshots/ wheels/ HARNESS_README.md tasks.jsonl`. Kaggle path: `/kaggle/input/competitions/gemma-4-developer-agent`.

### Files

**`tasks.jsonl`** — 129 public development tasks, one JSON per line:
- `instance_id` — e.g. `fastapi_11194`, `rich_3454`.
- `repo` — `owner/repo` (fastapi/fastapi, Textualize/rich, psf/requests, encode/httpx).
- `base_commit` — 40-char SHA of the snapshot before the fix.
- `problem_statement` — issue text given to the agent as the task prompt.
- `hints_text` — optional comments/hints (may be empty).
- `patch` — reference (gold) diff; present in the public file, excluded from the hidden test set.
- `test_patch` — diff with the verification tests run by pytest in Phase 2 grading; public only for local verification.
- `created_at` — ISO-8601.

**`snapshots/`** — 129 `snapshots/<instance_id>.tgz`, each a full git repo frozen at `base_commit` with forward history removed (safe to run `git status/log/diff` in `/workspace`).

**`graphs/`** — NetworkX AST call/dependency graphs in JSON (256 files: 129 `<instance_id>.json` hard-linked to 127 `<repo_short>_<base_commit>.json`). Back `get_code_neighbors` / `get_code_subgraph`. Schema:
- `directed: true`, `multigraph: true`, `graph: {...}`
- `nodes[*].id` — fully qualified symbol path (e.g. `fastapi.routing._prepare_response_content`); `nodes[*].name`; `nodes[*].text` — full source of the def/class at base_commit.
- `edges[*].source`, `.target`, `.type` (e.g. `calls`), `.key` (parallel-edge index).
- Note: `async def` functions are NOT in the graphs (affects some public fastapi/httpx tasks; host says no private task touches async defs).

**`embeddings/`** — `.npz` (256 files, same hard-link scheme). Each `<node_id>.npy` = float32[256] vector. Powers `search_similar_code`.

**`wheels/`** — 124 offline wheels (fastapi, starlette, pydantic, requests, urllib3, rich, httpx, httpcore, pytest, transitive deps). Mounted read-only at `/wheels/` in the sandbox.

**`docker/`** — `Dockerfile.sandbox` (Python 3.13, git, pytest, setuptools/hatchling/flit-core/poetry-core/pdm-backend), `Dockerfile.public` (variant for the 129 public tasks), `imp.py` and `telnetlib.py` shims for modules removed in 3.13.

**`sandbox/setup.py`** — runs in `/workspace` when preparing a task: inspects pyproject/setup.cfg/requirements, resolves offline wheels, `pip install --no-index --find-links=/wheels -e .`, makes a clean baseline commit so `git diff HEAD` only captures agent edits.

**`sample_submission/`** — ready-to-run baseline ADK submission illustrating the YAML schema, multi-agent delegation and multi-LoRA routing (its dummy LoRAs are shaped for 31B).

**`HARNESS_README.md`** — in-depth guide to the `swegemma`, `adk-submission`, `adk-eval-core` libraries, the two-container sandbox lifecycle, tool signatures, context compaction, local CLI eval commands.

**`submission.parquet`** — produced automatically at `/kaggle/working/submission.parquet` during evaluation: `id` (= instance_id), `prediction` (unified diff relative to base_commit, or `NO_PATCH`).

### Dataset generation & verification pipeline
1. Commit & PR mining: commits that jointly modify core logic (`.py`) and unit tests (`test_*.py` / `*_test.py`).
2. Issue linking & prompt extraction.
3. Filtering: drop mechanical refactors, docs-only, large automated changes, ambiguous issues.
4. Execution verification: **Fail-to-Pass** — test_patch on base_commit without fix must fail; **Pass-to-Pass** — fix + test_patch, whole suite must pass.
5. Near completion with frontier models (test set): a larger frontier model passes or gets within one test case of passing.

About 120 tasks in the test set, evenly split public/private. **The test set was curated from a set of private repositories** (none of the public repos appear in the test set).

---

## 3. Rules

### 3.1 Competition-specific terms (verbatim essentials)
- Sponsor: Google LLC. Total prizes (main): $65,000 (37k / 18k / 10k).
- Winner license: **Open Source Apache 2.0**. Data access and use: Competition Use and Commercial Apache 2.0.
- **Team limits:** max team size 5. Mergers allowed (by team leader) if combined submission count ≤ (submissions/day × days running) as of merger deadline.
- **Submission limits:** max **1 submission per day**; select up to **2 Final Submissions**.
- **Data security:** don't share competition data with non-participants.
- **Winner obligations:** deliver training code, inference code, environment description; detailed reproducible write-up (architecture, preprocessing, loss, training details, hyper-parameters) with link to a code repo.
- **External data and tools:** allowed if publicly available and equally accessible at no/minimal cost ("Reasonableness Standard"). Small subscriptions (e.g. Gemini Advanced) OK; proprietary data costing more than a prize is not. AutoML tools OK with appropriate license.
- Host/Kaggle employees can participate but can't win prizes.

### 3.2 Kaggle Foundational Rules (summary)
- One Kaggle account per person; no multi-accounting.
- No private sharing of code/data outside your team; public sharing must be on this competition's Kaggle forums/notebooks (then deemed OSI-licensed).
- Open-source code used must be under an OSI-approved license that does not limit commercial use.
- No hand labeling / human prediction of test data.
- Winners determined by **Private Leaderboard**; ties → earliest submission wins.
- Winners must respond within 1 week and return prize docs within 2 weeks.

### 3.3 Host clarification: distillation from external LLMs (thread 742807)
Using proprietary or open-weight models (e.g. frontier APIs) to generate synthetic patches/trajectories for training Gemma is allowed, **as long as you use them in accordance with their model license terms** and the output used in your submission doesn't conflict with the competition's license requirements.

---

## 4. Official "Getting Started – Gemma 4 Developer Agent" notebook (verbatim code)

Source: https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent (Ryan Holbrook, Kaggle staff, v3, 2840 votes). Runtime 8m22s on GPU L4×4.
**Inputs:** competition data; dataset **"Gemma 4 Developer Agent Wheelhouse"** (`/kaggle/input/datasets/metric/gemma-4-developer-agent-wheelhouse`, 41 wheels incl. swegemma, adk_submission, google-adk, vLLM, litellm); Model **Gemma 4 / other / V2** (`/kaggle/input/models/google/gemma-4/other/<model>/2`).
Sections: 1. Env & install · 2. Dataset & sample submission · 3. Code graph functions · 4. Start vLLM · 5. Phase 1 inference + Phase 2 verification · 6. Package submission.

### Cell 1 – Environment configuration and package installation
```python
import glob
import importlib
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Configure environment variables for offline vLLM serving and LiteLLM routing
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['TRANSFORMERS_NO_FLAX'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['VLLM_NO_USAGE_STATS'] = '1'
os.environ['VLLM_WORKER_MULTIPROC_METHOD'] = 'spawn'
os.environ['VLLM_ENGINE_READY_TIMEOUT_S'] = '1200'
os.environ['VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS'] = '1'
os.environ['NCCL_DEBUG'] = 'WARN'
os.environ['LITELLM_LOCAL_MODEL_COST_MAP'] = 'True'
os.environ['LITELLM_TELEMETRY'] = 'False'
os.environ['LITELLM_LOG'] = 'WARNING'
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', 'EMPTY')
os.environ['LOCAL_API_KEY'] = os.environ.get('LOCAL_API_KEY', 'EMPTY')
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
os.environ['OTEL_SDK_DISABLED'] = 'true'
os.environ['OTEL_PYTHON_DISABLED'] = 'true'

def configure_logging() -> None:
    """Silence verbose third-party loggers."""
    for name in (
        'LiteLLM', 'LiteLLM Router', 'LiteLLM Proxy', 'litellm',
        'httpx', 'httpcore', 'openai', 'urllib3',
        'opentelemetry', 'opentelemetry.context',
    ):
        lg = logging.getLogger(name)
        lg.setLevel(logging.WARNING)
        if 'litellm' in name.lower():
            lg.propagate = False
            lg.handlers.clear()

configure_logging()

WHEELHOUSE_DIR = Path('/kaggle/input/datasets/metric/gemma-4-developer-agent-wheelhouse')

# Remove broken cutlass .pth hooks if present
for pth_pattern in (
    '/usr/local/lib/python*/dist-packages/*cutlass*.pth',
    '/usr/local/lib/python*/site-packages/*cutlass*.pth',
):
    for pth in glob.glob(pth_pattern):
        try:
            os.unlink(pth)
        except OSError:
            pass

# Restore PEP 440 '+cu128' wheel filenames stripped by Kaggle dataset uploads
tmp_whl = Path('/tmp/wheelhouse')
tmp_whl.mkdir(parents=True, exist_ok=True)
for w in WHEELHOUSE_DIR.glob('*.whl'):
    if 'cutlass' in w.name.lower():
        continue
    target_name = (
        w.name.replace('cu128', '+cu128')
        if ('cu128' in w.name and '+' not in w.name)
        else w.name
    )
    target = tmp_whl / target_name
    if not target.exists():
        try:
            os.symlink(w, target)
        except OSError:
            shutil.copyfile(w, target)

wheels = sorted(str(w) for w in tmp_whl.glob('*.whl'))
print(f'Installing {len(wheels)} wheels from {WHEELHOUSE_DIR}...')
subprocess.run(
    [sys.executable, '-m', 'pip', 'install', '-q', '--no-deps', '--force-reinstall', *wheels],
    check=True,
)
importlib.invalidate_caches()
configure_logging()
print('Wheelhouse installation complete.')
# -> Installing 41 wheels ... Wheelhouse installation complete.
```

### Cell 2 – Competition dataset and sample submission
```python
import re
from swegemma.models import load_tasks

DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
WORKING_DIR = Path('/kaggle/working')
WORKING_DIR.mkdir(parents=True, exist_ok=True)

# Official quantized competition models:
# - 'gemma-4-31b-it-qat-w4a16-ct' (default in sample_submission)
# - 'gemma-4-12b-it-qat-w4a16-ct'
# - 'gemma-4-e4b-it-qat-w4a16-ct'
# - 'gemma-4-e2b-it-qat-w4a16-ct'
MODEL_NAME = 'gemma-4-12b-it-qat-w4a16-ct'

# Copy sample_submission to a writable directory for customization and packaging
SAMPLE_SUBMISSION_SRC = DATA_DIR / 'sample_submission'
AGENT_DIR = WORKING_DIR / 'sample_submission'
if AGENT_DIR.exists():
    shutil.rmtree(AGENT_DIR)
shutil.copytree(SAMPLE_SUBMISSION_SRC, AGENT_DIR)

# If switching away from 31B, update all agent YAMLs and remove the 31B-shaped sample LoRA adapters
if MODEL_NAME != 'gemma-4-31b-it-qat-w4a16-ct':
    for yaml_path in [AGENT_DIR / 'agent.yaml', *sorted((AGENT_DIR / 'sub_agents').glob('*.yaml'))]:
        if yaml_path.is_file():
            text = yaml_path.read_text(encoding='utf-8')
            text = re.sub(r'^(\s*model:\s*).*$', rf'\g<1>{MODEL_NAME}', text, flags=re.MULTILINE)
            text = re.sub(r'^\s*adapter:\s*.*\n?', '', text, flags=re.MULTILINE)
            yaml_path.write_text(text, encoding='utf-8')
    shutil.rmtree(AGENT_DIR / 'adapters', ignore_errors=True)

# Load tasks from the published dataset
TASKS_PATH = DATA_DIR / 'tasks.jsonl'
tasks = load_tasks(TASKS_PATH)

print(f'Data directory: {DATA_DIR}')
print(f'Agent directory: {AGENT_DIR} (model={MODEL_NAME})')
print(f'Loaded {len(tasks)} tasks from {TASKS_PATH.name}')
for t in tasks[:5]:
    print(f' - {t.instance_id} ({t.repo} @ {t.base_commit[:8]})')
# -> Loaded 129 tasks; first: fastapi_15661, fastapi_15588, fastapi_15589, fastapi_15030, fastapi_14962
```

### Cell 3 – Code graph functions
```python
from swegemma import graph as sg

sample_task = tasks[0]
GRAPH_DIR = str(DATA_DIR / 'graphs')
EMBEDDINGS_DIR = str(DATA_DIR / 'embeddings')

repo_graph = sg.get_graph(
    repo_name=sample_task.repo,
    graph_dir=GRAPH_DIR,
    embeddings_dir=EMBEDDINGS_DIR,
    base_commit=sample_task.base_commit,
)
sample_nodes = list(repo_graph.nodes())
print(f'Graph for {sample_task.repo} ({sample_task.instance_id}):')
print(f' Nodes: {repo_graph.number_of_nodes()}, Edges: {repo_graph.number_of_edges()}')

query_node = next((n for n, deg in repo_graph.degree() if deg >= 5), sample_nodes[0])
neighbors = sg.get_neighbor(node=query_node, graph=repo_graph, max_neighbors=10)

similar = sg.get_similar_nodes(
    node=query_node,
    repo_name=sample_task.repo,
    k=5,
    graph=repo_graph,
    graph_dir=GRAPH_DIR,
    embeddings_dir=EMBEDDINGS_DIR,
    base_commit=sample_task.base_commit,
)
for item in similar:
    print(f" - {item['node_name']} (similarity={item['similarity']:.4f})")

focal_nodes = [query_node, *neighbors[:4]]
subgraph = sg.get_induced_subgraph(repo_graph, focal_nodes)
# Output example: fastapi graph 4263 nodes / 2430 edges; neighbor ids look like
# 'fastapi/fastapi;fastapi.exceptions.HTTPException'; similarity scores are all ~0.999 (embeddings poorly discriminative).
```

### Cell 4 – Start vLLM server
```python
import litellm
import torch
from adk_submission import VllmConfig, VllmServer, discover_adapters
from adk_submission.discovery import discover_declared_models
from swegemma.config import ALLOWED_ADAPTER_EXTENSIONS

litellm.drop_params = True

ALLOWED_MODEL_NAMES = frozenset({
    'gemma-4-31b-it-qat-w4a16-ct',
    'gemma-4-12b-it-qat-w4a16-ct',
    'gemma-4-e4b-it-qat-w4a16-ct',
    'gemma-4-e2b-it-qat-w4a16-ct',
})
MODEL_VLLM_EXTRA_ARGS = {
    'gemma-4-12b-it-qat-w4a16-ct': (
        '--hf-overrides',
        '{"architectures": ["Gemma4ForCausalLM"], "model_type": "gemma4"}',
    ),
}
_SAFE_PATH_COMPONENT = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]*')
INFERENCE_API_KEY = os.environ.get('LOCAL_API_KEY', 'EMPTY')

declared_models = discover_declared_models(AGENT_DIR)
assert len(declared_models) == 1, f'Expected exactly 1 declared model, got: {sorted(declared_models)}'
declared_model = next(iter(declared_models))
assert declared_model in ALLOWED_MODEL_NAMES

MODEL_PATH = Path(f'/kaggle/input/models/google/gemma-4/other/{declared_model}/2')
assert MODEL_PATH.exists(), f'Model weights not found at {MODEL_PATH}. Ensure the model input is attached.'

adapters = discover_adapters(str(AGENT_DIR), adapter_extensions=ALLOWED_ADAPTER_EXTENSIONS)
adapter_map = getattr(adapters, 'adapters', None) or {}
for adapter_name in adapter_map:
    assert _SAFE_PATH_COMPONENT.fullmatch(adapter_name), (
        f'Unsafe adapter name {adapter_name!r}: must match [A-Za-z0-9][A-Za-z0-9._-]*'
    )
detected_ranks = [
    r for info in adapter_map.values() if (r := getattr(info, 'rank', None)) is not None and r > 0
]

gpu_count = torch.cuda.device_count() if torch.cuda.is_available() else 1
tp_size = 4 if gpu_count >= 4 else (2 if gpu_count >= 2 else 1)

if 'server_instance' in globals() and server_instance is not None:
    server_instance.stop()

vllm_cfg = VllmConfig(
    model=str(MODEL_PATH),
    port=8000,
    host='127.0.0.1',
    tool_call_parser='gemma4',
    reasoning_parser='gemma4',
    max_model_len=32768,
    dtype='bfloat16' if (torch.cuda.is_available() and torch.cuda.is_bf16_supported()) else 'auto',
    gpu_memory_utilization=0.90,
    enable_auto_tool_choice=True,
    enable_lora=bool(adapter_map),
    max_loras=max(1, len(adapter_map)),
    max_lora_rank=max(detected_ranks) if detected_ranks else 128,
    scheduler_reserve_full_isl=False,
    tensor_parallel_size=tp_size,
    startup_timeout=60 * 20,
    extra_args=MODEL_VLLM_EXTRA_ARGS.get(declared_model, ()),
)
server_instance = VllmServer(vllm_cfg, adapter_manifest=adapters)
server_instance.start()
print(f'vLLM server started on {server_instance.base_url} (tp={tp_size})')

# Register model and LoRA adapter aliases for Google ADK
models = server_instance.create_model_registry(
    aliases=[declared_model],
    model_prefix='openai/',
    api_key=INFERENCE_API_KEY,
)
```

### Cell 5 – Phase 1 inference and Phase 2 verification
```python
import asyncio
import concurrent.futures
import pandas as pd
import yaml
from google.adk.agents.context_cache_config import ContextCacheConfig
from google.adk.apps._configs import EventsCompactionConfig
from swegemma.config import EvalConfig, build_submission_limits
from swegemma.evaluate import Evaluator

def run_sync(coro_or_fn, *args, **kwargs):
    """Run an async coroutine synchronously inside a notebook event loop."""
    if callable(coro_or_fn) and not asyncio.iscoroutine(coro_or_fn):
        fn = lambda: coro_or_fn(*args, **kwargs)
    else:
        fn = lambda: coro_or_fn
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop is not None and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(lambda: asyncio.run(fn())).result()
    return asyncio.run(fn())

# Read optional evaluation settings from the submission's eval_config.yaml / eval_config.yml
eval_config_file = next(
    (c for name in ('eval_config.yaml', 'eval_config.yml') if (c := AGENT_DIR / name).is_file()),
    None,
)
raw_eval_cfg = (
    yaml.safe_load(eval_config_file.read_text(encoding='utf-8')) or {}
    if eval_config_file is not None else {}
)
eval_section = raw_eval_cfg.get('evaluation', raw_eval_cfg)

timeout_seconds = int(eval_section.get('timeout_seconds', 300))                       # per run_command
verification_timeout_seconds = int(eval_section.get('verification_timeout_seconds', 300))
max_tool_calls = int(eval_section.get('max_tool_calls', 100))
max_time_minutes = float(eval_section.get('max_time_minutes', 60.0))
turns_raw = eval_section.get('max_turns', eval_section.get('max_llm_calls'))
max_turns = int(turns_raw) if turns_raw is not None else None

SAMPLE_TASKS = tasks[:2]
limits, gen_constraints = build_submission_limits()

eval_config = EvalConfig(
    tasks_path=TASKS_PATH,
    snapshots_dir=DATA_DIR / 'snapshots',
    results_dir=WORKING_DIR / 'results',
    submission_dir=AGENT_DIR,
    models=models,
    sandbox='subprocess',
    timeout_seconds=timeout_seconds,
    verification_timeout_seconds=verification_timeout_seconds,
    max_time_minutes=max_time_minutes,
    max_tool_calls=max_tool_calls,
    max_turns=max_turns,
    limits=limits,
    generation_constraints=gen_constraints,
    adapter_manifest=adapters,
    context_cache_config=ContextCacheConfig(min_tokens=2048, ttl_seconds=1800, cache_intervals=10),
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=15,
        overlap_size=2,
        token_threshold=14336,
        event_retention_size=5,
    ),
    graph_dir=GRAPH_DIR,
    embeddings_dir=EMBEDDINGS_DIR,
    wheels_dir=DATA_DIR / 'wheels',
    verbose=False,
)

evaluator = Evaluator(eval_config)
predictions = []
for idx, task in enumerate(SAMPLE_TASKS, start=1):
    result = run_sync(evaluator.evaluate_task, task=task, task_index=idx, total_tasks=len(SAMPLE_TASKS))
    patch = (result.agent_patch or '').strip()
    predictions.append({'id': task.instance_id, 'prediction': patch if patch else 'NO_PATCH'})
    print(f' -> resolved={result.resolved}, exit_code={result.test_exit_code}, '
          f'patch_chars={len(patch)}, tool_calls={result.tool_calls}, duration={result.duration_seconds:.1f}s')

submission_df = pd.DataFrame(predictions, columns=['id', 'prediction'])
```
Notes from the run log: sample system prompt starts with *"You are an expert autonomous software engineer assigned to resolve an issue in a repository efficiently and decisively."*; task prompt starts with *"You are evaluating a software engineering task for repository fastapi/fastapi."* The demo used a tiny budget (10 tool calls / 1 min) so both tasks ended `NO_PATCH` with warnings `agent timed out` and `completed without explicit submit_patch call and no working tree modifications`. Result object fields: `resolved`, `test_exit_code`, `agent_patch`, `tool_calls`, `duration_seconds`.

### Cell 6 – Package submission archive
```python
import zipfile
from adk_submission import validate_directory
from swegemma.config import ALLOWED_SUBMISSION_EXTENSIONS, MAX_SUBMISSION_SIZE_BYTES

for dirpath, dirnames, filenames in os.walk(AGENT_DIR, followlinks=False):
    parent = Path(dirpath)
    for name in (*dirnames, *filenames):
        assert not (parent / name).is_symlink(), f'Symlinks are not permitted: {(parent / name).relative_to(AGENT_DIR)}'
validate_directory(AGENT_DIR, limits=limits)

zip_base = WORKING_DIR / 'submission'
zip_path = Path(shutil.make_archive(str(zip_base), 'zip', root_dir=AGENT_DIR))

with zipfile.ZipFile(zip_path, 'r') as zf:
    infos = zf.infolist()
    total_size = sum(i.file_size for i in infos)
    assert total_size <= MAX_SUBMISSION_SIZE_BYTES, f'Archive exceeds 3 GiB limit: {total_size}'
    for info in infos:
        if not info.is_dir():
            ext = Path(info.filename).suffix.lower()
            assert ext in ALLOWED_SUBMISSION_EXTENSIONS, f'Disallowed file extension: {info.filename}'
print(f'Created {zip_path}')
```
Submission size limit: **3 GiB**; only allowed file extensions; no symlinks.

---

## 5. Reference submission: "Gemma 4 | Budget-Aware Coding Agent v2" (public score 0.22, verbatim)

Source: https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-coding-agent-v2 (717 votes, Gold). Derived from matterhorn3838 "Gemma 4 SuperAgent" (0.18). Single agent, no training. Packages 4 files.

### `agent.yaml`
```yaml
name: swe_agent
model: gemma-4-31b-it-qat-w4a16-ct
instruction: !include prompts/system.md
tools:
- run_command
- read_file
- edit_file
- write_file
- get_status
- submit_patch
- get_code_neighbors
- search_similar_code
- get_code_subgraph
generate_content_config: !include configs/sampling.yaml
```

### `configs/sampling.yaml`
```yaml
temperature: 0.2
top_p: 0.95
max_output_tokens: 8192
thinking_config:
  thinking_budget: 4096
  include_thoughts: true
```

### `eval_config.yaml`
```yaml
evaluation:
  timeout_seconds: 240
  max_tool_calls: 28
  max_time_minutes: 8
  max_turns: 80
```
(Other accepted keys seen in the harness: `verification_timeout_seconds`, `max_llm_calls` as alias of `max_turns`.)

### `prompts/system.md`
```markdown
You are an autonomous software engineer. Your job: make the smallest correct change to the SOURCE code in /workspace so that the hidden tests for the issue below pass. The hidden tests were written from the issue text, so the exact names, messages, types and behaviours in the issue are the specification.

# HARD LIMITS
- 28 tool calls and 8 minutes in total. When either runs out, the working tree is graded as it is. An edit that exists counts, even if you never call `submit_patch`. An unedited tree always scores zero.
- Never create, modify or delete test files (`test_*.py`, `*_test.py`, anything under `tests/`). This is an automatic failure.
- Never run a full test suite (bare `pytest`, `pytest .`, `unittest discover`). Always name one test file, and add `-k` when you can.
- Never look outside /workspace. All dependencies are already installed.
- Never use `search_similar_code`, `get_code_neighbors` or `get_code_subgraph`. They return nothing useful.

# CALL PLAN
- Calls 1-8: locate and read. Calls 9-12: edit. You MUST have edited a source file by call 12. If you are unsure, make your best-guess edit in the most likely place now. A wrong edit can still be corrected. Pure reading cannot score.
- Calls 13-20: verify and correct.
- Call 20 onward: no new exploration. Check, fix, submit.
- Always finish with `git diff` followed by `submit_patch`.

# PROCEDURE

## 1. Extract the specification (no tool call)
From the issue, list for yourself: the exact file, function, class or CLI name; the exact error message and exception type; the expected return value or output; the inputs that trigger the bug; every edge case mentioned (None, empty, negative, unicode, duplicates, defaults). Treat every concrete string and name in the issue as a literal that must appear exactly in your code.

## 2. Locate
- Use exact paths from the issue directly. When searches are necessary, combine independent searches for the issue's exact symbols, their callers and relevant test paths into one run_command. Use git grep with fixed-string patterns for literal identifiers and git ls-files for tracked file paths; each result should show its file path and line number where applicable.
- Batch only searches whose inputs are already known. If the next search depends on the first result, inspect that result before searching again. Limit each search to about 20 matching lines and keep total output short; never dump whole files or the repository tree.
- Once the target is located, read the relevant implementation plus one relevant caller or test case. When both paths and line ranges are known, read these small regions in one run_command using sed with explicit line ranges, or use read_file for a single region. Aim for about 40 lines per region and at most three regions per command. Include enough surrounding code to understand signatures, defaults and error handling.
- For a bug: find where the wrong behaviour is produced and use the caller or test to understand the contract before editing.
- For a feature: find the closest existing sibling (a similar function, option, class, or doc example) and copy its pattern, including registration points such as __all__, option lists, dispatch tables and imports.
- Reuse paths and test names already discovered. Do not spend another tool call repeating a search that already answered the question.
- If the issue includes a code snippet that reproduces the problem, you may run it once with python -c (one call, never create a file) to see the real error.

## 3. Edit
- Use edit_file for changes to existing code. Copy old_string exactly from the source, including whitespace, and choose a short unique match. Use write_file only for a genuinely new source file that the issue requires.
- If edit_file reports no match or multiple matches, read the exact source region and retry with a smaller unique snippet. Never repeat an identical failed edit. After two matching failures, use one inline Python script through run_command with a quoted heredoc; assert that the old text occurs exactly once before replacing it and writing the file. Preserve unrelated content and do not rewrite the file from memory.
- Fix the cause, not the symptom. Do not special-case the example from the issue.
- Change only what the issue requires. Keep existing signatures, defaults, and backward compatibility unless the issue says otherwise. Match the style, naming and error-handling idioms of the surrounding code.
- Use the exact exception class and exact message text from the issue. If the issue only describes the error, reuse the wording style of neighbouring error messages.
- Handle every edge case you listed in step 1.
- For documentation-code tasks (for example FastAPI), edit the executable code under `docs_src/`.

## 4. Verify (at most 2 calls)
- Find the test file with `find tests -name "*keyword*.py"`, then run `timeout 150 python -m pytest tests/path/test_x.py -x -q -k keyword`. Use `python3 -m unittest tests.test_x` for unittest projects.
- Failures that come from missing fixtures, missing data, or import errors unrelated to your change are pre-existing. Ignore them. Never repair tests or the environment.
- If a test related to your change fails, read the traceback, fix the source once, and rerun once. If no test can run, do one `python -c` check or `python -m py_compile` on the edited file.

## 5. Final check and submit
- Run `git diff`. Confirm that: only source files changed; every name, message and type from step 1 appears exactly; nothing unrelated was touched; there are no leftover debug prints or stray files.
- Call `submit_patch`. Confirm `patch_size > 0` and `files_changed > 0`. If either is 0, you have not edited anything. Edit now and submit again.
- End with a single-sentence summary of the fix.

# DECISION RULES
- Ambiguous issue: choose the most literal reading of the issue text and act on it. Do not ask questions and do not stall.
- Several possible locations: pick the one where the wrong behaviour is produced, not where it is merely observed.
- Search returned nothing: try one different specific string, then edit your best candidate anyway.
- Stuck after a failed fix: make a different, smaller change. Do not repeat the same edit.
- Never conclude that nothing needs to change. Every task requires a non-empty source patch.
```

### Packaging (from the same notebook)
```python
with zipfile.ZipFile(ZIP_PATH, 'w') as archive:
    for relative, content in sorted(FILES.items()):
        entry = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o100644 << 16
        archive.writestr(entry, content.encode('utf-8'))
```

---

## 6. Discussion digest (top-voted + pinned threads)

Base URL: `https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/<id>`. Posts by staff/host are marked [STAFF]. Community numbers are single-run observations; treat ±5 tasks as noise.

### 6.1 Official announcements
- **[STAFF] 748287 – New Gemma 4 models (12B, E4B, E2B).** All four variants allowed; no mixing within a submission (different LoRAs OK). Suggested strategies for small models: more test-time compute, `ParallelAgent` for concurrent LLM calls (tool calls still sequential), cheaper LoRA finetuning, more specialized agents. 12B needs vLLM extra args `--hf-overrides '{"architectures": ["Gemma4ForCausalLM"], "model_type": "gemma4"}'` (scorer already has it). Community note: ParallelAgent has a known bug in the ADK version used (v1.36; fixed upstream in v2, google/adk-python issue 7324). One user: official Wheelhouse V31 wheels are cp312 — works on Kaggle env pinned to Python 3.12 (2026-07-01), not on Python 3.13 env (2026-10-03).
- **[STAFF] 751104 – Small-model bonus prize ($10k)** — see §1.
- **[STAFF] 745998 – Code graphs exclude `async def` functions.** Affects some public fastapi/httpx tasks; no private task touches async defs (≤1.8% of private functions are async). No fix planned.
- **[STAFF] 747519 – "Kaggle Error" & queue delays.** Submissions waiting >15 h used to be marked Kaggle Error; queue timeout extended; affected runs rescored automatically. **New rule: one pending submission per team** (separate from 1/day). Queue delays have been 14–33 h; in mid-Nov several submissions stuck PENDING for 5+ days (staff investigating as of 2026-11-16). Plan submissions early; a stuck run burns daily slots.
- **[STAFF] 743683 – Rerunning failed submissions** ("requested more CPU/GPU/TPU than available" errors); rescoring paused pending L4 queue fixes.
- **[STAFF] 744807 – Errors after Sep 30 wheelhouse update** were due to an overnight GPU outage.
- **[STAFF] 751339 – "Notebook Threw Exception"** on valid bundles around 2026-10-21 was a scorer-side failure (likely slow vLLM startup on L4 hitting the 1,200 s server-start limit); staff said they'd rerun. Example user eval_config: `max_time_minutes: 5, max_tool_calls: 40, max_turns: 80, timeout_seconds: 300`.
- **[STAFF] 742882 – Local harness.** Packages (`swegemma`, `adk-submission`, `adk-eval-core`) are distributed via the Kaggle dataset **"Gemma 4 Developer Agent Wheelhouse"**; usage shown in the Getting Started notebook (§4). HARNESS_README §9 references `swegemma eval --tasks … --submission-dir starter_kit/sample_submission --sandbox docker`.
- **[STAFF] 747248 – fastapi tasks failing with gold patch locally.** Cause in public env: `wheels/` lacks `typing_inspection` (pydantic ≥2.11 needs it) and bundled release wheels of the repo-under-test shadow `/workspace` on sys.path. Staff: none of the training repos appear in the test set, and **every test-set task validates at 100% with a gold patch** on the scorer. So local public-task scores under-estimate; don't over-fit to public-repo quirks.
- **742815 – Getting started / Discord** (discord.gg/kaggle; not staff-monitored; code sharing must be public on Kaggle).
- **742807 – Distillation from external LLMs is allowed** (see §3.3).

### 6.2 Community findings
- **743506 – Public LB has exactly 58 tasks** (deduced from rounding-down of displayed scores). So one task ≈ 0.017 public score; 0.22 ≈ 13/58, 0.24 ≈ 14/58, 0.29 ≈ 17/58.
- **746250 – Ablations on 31B (129 public tasks, local, single runs):**
  - Thinking disabled: 17.8% vs ~37–40% enabled. Hiding thought summaries (`include_thoughts: false`): 27%. → **keep thinking + include_thoughts on.**
  - Temp 0.4 and 1.0 tied best (39.5%); top-p 0.8/1.0 no change; thinking budget 2048≈4096≥6144. Recommended baseline: temp 1.0, top_p 0.95, thinking_budget 4096.
  - Active time cap: 6 min 28.7%, 10 min 35.7%, **15 min 41.9%**, 20 min 38%, 60 min 39.5%.
  - Graph tools: no benefit (all semantic searches returned empty; subgraph never used).
  - Analyzer sub-agent: +1 task (noise). Halving tool budget 50→25: −29% runtime, −14 tasks.
  - Kaggle 4×L4 calibration (TP=4, sequential): ~900 s per 1M tokens, ~1,110 tok/s, ~8.7 s per model call with thinking. **Plan ≈5.5 min/task on Kaggle** (120×5.5 = 11 h + ~1 h setup).
  - "Gains will come from post-training; data curation and fine-tuning should be the center."
- **747168 – Stronger teachers barely beat Gemma 31B in this harness** (124 public tasks, 25 min/50 calls, 32k ctx + compaction): Gemma 54/124 & 53/123; DeepSeek V4 Pro 58; Qwen3.6-27B 59. 15% of tasks flip between identical Gemma runs. Union of 4 runs 73/123. Conclusion: ceiling is the setup (32k context + compaction, call budget, sparse issue texts like "Fixes #NNNN"); teachers are faster (3.5–3.9 vs 5.2 min median) — speed may matter more. Gotchas: `run_command` is synchronous and blocks the event loop (run one task per process when timing); vLLM gemma4 tool-call parser sometimes mangles `edit_file` calls whose `old_string` contains `"""` (keys like `<|"|>,filepath`) → ADK rejects ("mandatory input parameters are not present") and the model retries the identical call many times (rejected calls don't count toward the cap but cost time).
- **750974 – 31B vs 12B vs E4B (same agent files):** 31B 9–11/31 at 8 min; 12B 4/31 (writes ~2× faster but ~3× more tokens, so slower per task; a 12B 8-min submission didn't finish in 12 h); 12B coder+reviewer 3/31; E4B 0/31. A second test on Kaggle 4×L4: 31B 31–44% vs 12B 17%; decode 31B ≈33–35 tok/s, 12B ≈62–64 tok/s.
- **751487 – Scorer-like local eval:** in a plain notebook only 52/129 gold patches pass; rebuilding a sandbox per `Dockerfile.sandbox` (clean venv, pytest, competition wheels + missing test packages: `inline_snapshot`, `dirty_equals`, `annotated_doc`, `typing_inspection`, `pytest-httpbin`, period-correct Pygments for 7 rich tasks) → 127/129 pass. Resources: notebook "Gemma 4 Agent: Do Gold Patches Pass Locally?" (kaggle.com/zbigniewkirchner/code), datasets `zbigniewkirchner/gemma-4-agent-local-eval-wheels` and `zbigniewkirchner/gemma-4-agent-local-eval-pythons`.

---

## 7. Snapshots

### 7.1 Public leaderboard (2026-11-17, top)
1 Yurnero 0.29 · 2–15: 0.24 (Yike Xu, MUHAMMED IDRIS BIN YACOOB, SAVE, chizhu, pluris, Alberth Moreira, tammam alasha, Pınar Aksoy, Takumu Hata, Serhii Mosiiash, LuisSpecian, Radek, Sophia0817, bgunshui) · 16–49+: 0.22. ~6,010 teams total. Public LB ≈ 50% of test data (58 tasks).

### 7.2 Top public notebooks (by votes) — `https://www.kaggle.com/code/<slug>`
| Notebook | Public score | Slug |
|---|---|---|
| Getting Started – Gemma 4 Developer Agent (pinned, staff) | – | ryanholbrook/getting-started-gemma-4-developer-agent |
| Small Model Leaderboard (pinned, daily) | – | ryanholbrook/gemma-4-developer-agent-small-model-leaderboard |
| Budget-Aware Coding Agent v2 | 0.22 | flexonafft/gemma-4-budget-aware-coding-agent-v2 |
| EDA, Baseline for a start | 0.12 | romanrozen/gemma-eda-baseline-for-a-start-lb-top-1 |
| Budget-Fit Single Agent | 0.18 | verracodeguacas/gemma-4-agent-budget-fit-single-agent |
| Gemma and the Shape of Doubt | 0.20 | prvsiyan/gemma-and-the-shape-of-doubt |
| Black Cat SWE Agent – Pack Instinct | 0.12 | lucifer19/black-cat-swe-agent-pack-instinct |
| Repair Lab: Compare Before You Submit | 0.22 | denpugovkin/gemma-4-repair-lab-compare-before-you-submit |
| Task Soundness, Serving and Evaluation | 0.18 | dmitriigluzdov/gemma-4-task-soundness-serving-and-evaluation |
| Walkthrough, Findings & Submission | 0.15 | zhukovoleksiy/gemma-4-walkthrough-findings-submission |
| Version 1 added Adaptor (LoRA) | 0.22 | ayush04barai/version-1-added-adaptor |
| SuperAgent Reproduction | 0.20 | jvnhonglei/gemma-4-superagent-reproduction |
| LB 0.22 – 3 tweaks, 40 tool calls, no training | 0.22 | bliverrigpdoge/lb-0-22-3-tweaks-40-tool-calls-no-training |
| Gemma 4 Baseline | 0.18 | honghanhhh/gemma-4-baseline |
| Score To – Gemma 4 | 0.20 | leoprovorov/score-to-gemma-4 |
| E2B LoRA Fine-Tuning & SWE-Agent Baseline | 0.17 | boristown/gemma-4-e2b-lora-fine-tuning-swe-agent-baseline |
| SWE Agent T8 Static | 0.20 | navyadevadiga/gemma4-swe-agent-t8-static |
| Gemma 4 SuperAgent (original budget strategy) | 0.17–0.18 | matterhorn3838/gemma-4-superagent |

### 7.3 Models tab
Competition models: `google/gemma-4/other/gemma-4-{31b,12b,e4b,e2b}-it-qat-w4a16-ct` (version 2). Unquantized/Transformers variants (`gemma-4-*-it`, `*-qat-q4_0-unquantized`) also exist on Kaggle Models — useful as LoRA training bases.

---

## 8. Practical checklist / gotchas
1. Exactly one `model:` across `agent.yaml` and all `sub_agents/*.yaml`; must be one of the 4 allowed names.
2. LoRA adapters must match the chosen base model's shape (sample_submission adapters are 31B-shaped — delete them if you switch). Adapter dir names must match `[A-Za-z0-9][A-Za-z0-9._-]*`. vLLM `max_lora_rank` defaults to 128 if no rank detected.
3. Context is 32,768 tokens with ADK events compaction (interval 15, overlap 2, threshold 14,336 tokens, retain 5) — keep tool outputs short.
4. 12 h for ~120 tasks including sandbox setup → ≈5.5 min/task wall clock on 4×L4 with 31B. A config that overruns gets **no score**.
5. A working-tree edit is graded even without `submit_patch`; an empty tree = fail. Never touch test files.
6. Graph/embedding tools were found useless by multiple teams (embeddings ~0.999 similarity everywhere; async defs missing).
7. Local scores on public tasks are pessimistic unless you rebuild the scorer-like sandbox (§6.2 751487); test set is from private repos, all gold-solvable.
8. Submission queue: 1/day, 1 pending at a time, delays of 1+ days — leave buffer before **Dec 2, 2026 23:59 UTC**; select 2 finals (include an E2B/E4B run if going for the $10k bonus).
9. Distilling from frontier models for training data is allowed if their license terms permit; winners must open-source (Apache 2.0) code and give a reproducible write-up.

---

## 9. HARNESS_README.md digest (swegemma / adk-submission / adk-eval-core)

### 9.1 Stack
- **adk-submission** – compiles the submission YAML into ADK agents (`compile_submission`); no competitor Python is ever imported. Also runs the local `VllmServer`.
- **adk-eval-core** – sandboxes (Docker / subprocess), 3-tier `apply_replacement` for edits, token budgets, `ModelRetryPlugin`, trajectory traces.
- **swegemma** – two-container lifecycle (`Evaluator`, `run_agent_sandbox`, `verify_task`), the 9 tools, prompt construction + nudges, patch extraction, pytest/JUnit scoring.

### 9.2 Submission schema
- Exactly one root config: `agent.yaml` / `agent.yml` / `root_agent.yaml` / `root_agent.yml`.
- `!include`: `.md`/`.txt` → raw string; `.yaml`/`.yml` → parsed recursively (depth ≤10, cycle detection). No absolute paths, `..`, or symlinks out of root.
- `agent_class`: `LlmAgent` (default), `SequentialAgent`, `ParallelAgent`, `LoopAgent` (`max_iterations` 1–500).
- LlmAgent fields: `name`, `model`, `adapter`, `description`, `instruction`, `tools` (names, `agent_tool: {config_path, skip_summarization}`, or inline agents), `skills` (relative dirs), `sub_agents` (`{config_path}`), `output_key`, `include_contents` (`default`/`none`), `disallow_transfer_to_parent/peers`, `generate_content_config`.
- **`instruction` supports ADK state templating: `{problem_description}`, `{hints}`** (hints only present if non-empty), plus any `output_key` values.
- Allowed file extensions: `.yaml .yml .md .txt .py .json .safetensors` only (no `.bin/.pt/.pth`). Total unpacked size < 3 GiB. Other limits are loose (10k files, 500 agents, depth 50…).
- `generate_content_config`: temperature, top_p, top_k, max_output_tokens (1–32768, default 16384), penalties, stop_sequences, seed, `thinking_config`:
  - `thinking_budget` 0–32768 (default 4096; 0 disables thinking).
  - `include_thoughts: true` keeps thoughts in history; `false` still thinks but strips thoughts from history.
  - Don't use `thinking_level` with vLLM/LoRA — use `thinking_budget` + `include_thoughts`.
  - Forbidden inside it: `tools`, `system_instruction`, `http_options`, `safety_settings`, `response_schema`.

### 9.3 Serving / hardware
- 4×L4 (24 GB each), vLLM TP=4, `gpu_memory_utilization 0.90`, `max_model_len 32768`, `tool_call_parser/reasoning_parser gemma4`, reasoning delimiters `<|channel>` … `<channel|>`.
- Weight footprint (W4A16): 31B ~16–18 GB, 12B ~6–8 GB, E4B ~3–4 GB, E2B ~2–3 GB.
- Single base model rule enforced by `validate_single_declared_model` (scans root, sub_agents, agent_tool configs, standalone YAMLs; provider prefixes stripped). Violation → `ParticipantVisibleError`.
- LoRA: `adapters/<name>/{adapter_config.json, adapter_model.safetensors}`, `max_lora_rank ≤ 128`. Size for 31B, all linear projections: r16 ≈110–220 MB, r32 ≈220–450 MB, r64 ≈450–900 MB, r128 ≈0.9–1.8 GB.
- Each sandbox container: **4 GiB RAM, 2 vCPU, no network**. OOM → exit 137.

### 9.4 Per-task lifecycle
Container A (agent): wheels → extract snapshot (no future git history) → `.git/info/exclude` (`__pycache__/ *.pyc .pytest_cache/ *.egg-info/ build/ dist/ .coverage`) → `pip install -e /workspace --no-deps` → test deps → **harness writes `/workspace/pytest.ini` and prepends a hook to `/workspace/conftest.py`** → `git commit -m baseline` → agent timer starts (setup time is NOT counted in `max_time_minutes`).
Container B (verification): fresh snapshot, same setup → apply agent patch (4 fallback passes: `git apply` variants, `-p0`, GNU `patch`) → reset test/config files → apply `test_patch` → `pytest <targets> --junitxml … -p no:anyio` (300 s fixed timeout).
**Resolved iff** pytest exit code 0 AND JUnit shows >0 passed, 0 failures, 0 errors, and every required test (FAIL_TO_PASS / PASS_TO_PASS / tests from test_patch) passed and was not skipped.

### 9.5 What the agent sees
Initial user message (built by `build_agent_prompt`):
1. `You are evaluating a software engineering task for repository {repo}.` + `Problem Statement:` …
2. `## Hints:` (if any)
3. `## Task Budget` — time, tool calls, turns.
4. `## Execution Environment Rules` — 300 s command timeout, 5000-char command output, `read_file` 150 lines / 10 000 chars, offline, don't pip install.
5. Standard instructions (work in /workspace, follow conventions, verify with targeted tests, call `submit_patch`, end with text).
6. `## Code Intelligence Tools` — only if graph tools are declared.
7. Workspace layout (≤200 entries of `find -maxdepth 3`, docs/tests pruned).
Undeclared tools are never advertised. pytest/unittest are available inside Container A by default.

### 9.6 Loop control
- Exiting: after a turn in which `submit_patch()` was called, the loop ends immediately.
- If a turn ends without a tool call and without submit, harness sends a **nudge**; >3 consecutive tool-less turns → session ends. Nudge texts cover: truncated `<|tool_call>` (split edits smaller), MAX_TOKENS while thinking (think less, act), plain stop ("continue or submit_patch").
- Hallucinated/undeclared tool calls return a structured error instead of crashing (`ToolErrorPlugin`).
- Transient model errors retried up to 5× with backoff.
- Context: events compaction (interval 15, overlap 2, threshold 14 336 tokens, keep 5) + context caching.

### 9.7 Tool details
| Tool | Counts toward `max_tool_calls` | Notes |
|---|---|---|
| `run_command` | yes | timeout = min(300 s, remaining time); timeout returns `TimeoutExceeded` but session continues; stdout/stderr each truncated to 5000 chars; non-zero exit → `status: error, CommandError` |
| `submit_patch` | **no** | `git add -N .` + `git diff --binary`; returns `patch_size`, `files_changed`; usable even when tool calls are exhausted |
| `get_status` | **no** | tool calls used/remaining, time remaining, patch status |
| `read_file` | yes | max 150 lines **and** 10 000 chars per call; `is_truncated`, `total_lines` returned |
| `edit_file` | yes | 3-tier match: exact → whitespace-flexible (auto re-indent) → regex across delimiters; >1 match without `allow_multiple` = error; file must exist & be non-empty |
| `write_file` | yes | mkdir -p; overwrites |
| `get_code_neighbors` | yes | short-name resolution (exact → suffix → case-insensitive → substring) |
| `search_similar_code` | yes | **offline: query must be a symbol name** (e.g. `Class.method`); computes similarity from that node's stored embedding; lexical fallback for multi-word queries — explains why natural-language queries return nothing |
| `get_code_subgraph` | yes | induced subgraph, 5000-char cap |
- Paths: leading `/` or `/workspace/` stripped; `..` rejected; string ints/bools auto-coerced.
- When `max_tool_calls ≥ 20` and ≤10 remain, every response carries a `budget_warning`.

### 9.8 Patch extraction rules (important)
- If the agent never calls `submit_patch`, the harness still extracts the working-tree diff → it is graded.
- **Stripped from every patch:** test files (`test_*.py`, `*_test.py`, `.py` under `tests/ test/ testing/`) and runner configs (`conftest.py`, `pytest.ini`, `pyproject.toml`, `tox.ini`, `setup.cfg`, `.pytest.ini`, `sitecustomize.py`, `usercustomize.py`, `*.pth`). → A fix that requires changing `pyproject.toml`/`setup.cfg` will be lost.
- **Untracked files inside /workspace are included** (because of `git add -N .`). Put scratch/repro scripts in `/tmp`, or delete them before submitting.
- Don't touch the harness-generated `pytest.ini` / `conftest.py`.

### 9.9 Budgets (`eval_config.yaml`, key `evaluation:`)
| Key | Scorer default | Env override |
|---|---|---|
| `max_time_minutes` | 60 | `SWE_MAX_TIME_MINUTES` |
| `max_tool_calls` | 100 | `SWE_MAX_TOOL_CALLS` |
| `max_turns` | 500 | `SWE_MAX_TURNS` |
| `timeout_seconds` (per command) | 300 | `SWE_TIMEOUT_SECONDS` |
| verification timeout | 300 (fixed on scorer) | – |
Defaults are far too generous for the 12 h global cap — always set your own.

### 9.10 Local CLI
```bash
swegemma eval \
  --tasks tasks.jsonl --snapshots-dir snapshots \
  --submission-dir sample_submission --results-dir results/run_01 \
  --sandbox docker --max-tool-calls 50 --max-time-minutes 30 \
  --concurrency 2 --display auto
# also: --task-id / --task-ids, --sandbox subprocess, --timeout-seconds,
#       --verification-timeout-seconds, --shard-index k --num-shards M,
#       --models-yaml, --skip-agent-patch (check that tests fail on baseline)
```
Outputs in `results/run_01/`: `summary.json`, `task_results.jsonl`, `patches/<id>.patch`, `test_outputs/<id>.log`, `traces/trace_<id>.json`, `logs/<id>.log`.

### 9.11 Official best practices
1. Keep `edit_file` payloads small; e.g. `thinking_budget: 4096` with `max_output_tokens: 16384`, so tool calls aren't cut off.
2. Don't modify `/workspace/pytest.ini` or `/workspace/conftest.py`.
3. Scratch scripts go in `/tmp`.
4. Use an `agent_tool` sub-agent with `skip_summarization: true` for read-only exploration, to keep file dumps out of the root agent's context.
5. Call `submit_patch()` explicitly and last (it's free, but ends the session).

---

## 10. sample_submission (as shipped)

`agent.yaml`
```yaml
name: swe_baseline_agent
model: gemma-4-31b-it-qat-w4a16-ct
adapter: main_lora
instruction: !include prompts/system.md
tools:
  - run_command
  - read_file
  - edit_file
  - write_file
  - get_status
  - submit_patch
  - get_code_neighbors
  - search_similar_code
  - get_code_subgraph
  - agent_tool:
      config_path: sub_agents/code_analyzer.yaml
      skip_summarization: true
generate_content_config: !include configs/sampling.yaml
```

`configs/sampling.yaml`
```yaml
temperature: 0.2
top_p: 0.95
max_output_tokens: 16384
thinking_config:
  thinking_budget: 4096
  include_thoughts: true
```

`eval_config.yaml` (demo budget only — far too small for real submissions)
```yaml
evaluation:
  timeout_seconds: 60
  max_tool_calls: 10
  max_time_minutes: 1
  max_turns: 50
```

Other files: `prompts/system.md` (3.9 kB; begins "You are an expert autonomous software engineer assigned to resolve an issue in a repository efficiently and decisively."), `prompts/analyzer.md` (527 B; read-only analysis sub-agent that returns file paths + line numbers, root cause, and a recommended minimal change), `sub_agents/code_analyzer.yaml` (`name: code_analyzer_agent`, read-only analyzer used as an AgentTool), `adapters/main_lora/` and `adapters/tool_lora/` (dummy zero-init LoRAs shaped for 31B — delete them if you change the model). Read the full files from the downloaded dataset.
