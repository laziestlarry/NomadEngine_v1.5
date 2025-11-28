# Repository Guidelines

Use this as a quick-start reference when contributing to NomadEngine.

## Project Structure & Module Organization
- `core/`: settings, logging, and bootstrap glue linking DB, scheduler, and event bus.
- `api/`: FastAPI app, routers, schemas; keep handlers thin and push logic into pipelines/agents.
- `agents/`: decision agents extending `BaseAgent`; emit events for observability.
- `pipelines/`: helpers that orchestrate tasks/blueprints/execution paths used by workers/scheduler.
- `workers/`: Python worker loop plus platform adapters under `workers/platform_workers/`.
- `scheduler/`: APScheduler engine with recurring jobs configured in `scheduler/context.py`.
- `modules/`: platform connectors loaded by pipelines/workers.
- `db/`: SQLAlchemy models; canonical SQLite lives at `db/nomad_v15.db`—avoid manual edits.
- `events/`: event bus/store/definitions shared across services.
- `common/`: shared utilities; prefer reuse here.
- `launcher/`: entrypoints (`nomad_run_all.py`, `nomad_api_only.py`, `start_python_worker.py`).
- `Archive-dataroom/`, `logs/`: generated data/logs; do not edit by hand.
- `scripts/`: demos and smoke tests such as `scripts/test_event.py`.

## Build, Test, and Development Commands
- Python 3.11+; install deps with `pip install -r requirements.txt`.
- `python launcher/nomad_run_all.py` or `./run_all.sh`: bootstrap DB + scheduler + event bus and serve API at 127.0.0.1:9000.
- `./run_api.sh`: run API only (no scheduler/worker).
- `./run_worker.sh`: start worker loop that consumes pending tasks.
- Smoke test: `python scripts/test_event.py` publishes a demo event before deeper debugging.

## Coding Style & Naming Conventions
- PEP 8 with 4-space indent; snake_case for modules/functions, PascalCase for classes, UPPER_SNAKE for constants.
- Favor type hints and dataclasses for small state; keep business logic out of route handlers.
- Log through `core.logger.logger` and emit meaningful events for downstream consumers.
- When touching DB, manage SQLAlchemy sessions explicitly (commit/close) to avoid leaked handles.

## Testing Guidelines
- Use pytest; place tests under `tests/` named `test_<module>.py`.
- Prefer temp SQLite (`sqlite://` or tmp files) to avoid mutating `db/nomad_v15.db`.
- Seed event/task fixtures so scheduler/worker flows stay deterministic.

## Commit & Pull Request Guidelines
- Write imperative commit titles (e.g., `add worker heartbeat backoff`); emojis optional.
- PRs should describe API/DB/behavior changes, linked issues, and commands/tests run.
- Call out rollout/backfill steps for scheduler/jobs/agents changes that impact production data.
- Avoid committing generated artifacts from `Archive-dataroom/` and `logs/`.

## Configuration & Data Safety
- Keep secrets in `.env`; never commit tokens or credentials.
- Backup SQLite before schema changes; migrations should not clobber `db/nomad_v15.db` data.

## Agent-Specific Notes
- Subclass `BaseAgent`, keep agents stateless, and use `emit_decision` to notify downstream consumers.
- Keep strategies small enough for the worker loop; offload heavy work to pipelines or background tasks.
- If changing task lifecycle or events, mirror updates in pipeline helpers to keep worker/scheduler expectations aligned.
