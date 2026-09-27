# GitHub validation matrix

The first validation corpus covers different structures and risks. Upstream repositories are read-only inputs; this project does not write to them.

Read-only inventory date: 2026-09-27 (Asia/Shanghai, UTC+08:00). Default branches and representative paths were read through the GitHub API.

| Repository | Default branch | Profile | Representative surfaces | Route scenario |
|---|---|---|---|---|
| `sharkdp/fd` | `master` | basic CLI | `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `Cargo.toml`, `tests/` | `update.basic.readme.low.static` |
| `psf/requests` | `main` | mature library | `README.md`, `.github/CONTRIBUTING.md`, `HISTORY.md`, `docs/api.rst`, `docs/community/release-process.rst`, `tests/` | `update.library.api.medium.test` |
| `encode/httpx` | `master` | library with dedicated docs | `README.md`, `.github/CONTRIBUTING.md`, `CHANGELOG.md`, `docs/api.md`, `docs/compatibility.md`, `docs/contributing.md`, `mkdocs.yml`, `tests/` | `update.library.api.medium.test` |
| `immich-app/immich` | `main` | multi-service self-hosted app | `CONTRIBUTING.md`, `docs/docs/developer/architecture.mdx`, `database-migrations.md`, `setup.md`, `testing.md`, `docs/docs/administration/backup-and-restore.md`, docs-build/migration workflows | `update.service.data.high.runtime` |
| `apache/airflow` | `main` | large workflow platform | `CONTRIBUTING.rst`, `airflow-core/adr/`, `airflow-core/docs/`, administration/deployment docs, release-management files, Provider surfaces | `update.platform.architecture.high.external` |
| `kubernetes/kubernetes` | `master` | infrastructure project with external authority | `README.md`, `CONTRIBUTING.md`, `build/README.md`, `api/openapi-spec/README.md`, `cluster/README.md`, release/build scripts | `review.infra.ops.high.external` |

Pass conditions:

- small work is not forced into enterprise documentation;
- complex work is not reduced to README-only edits;
- route/ledger/workflow/progress are recommended only when useful;
- external authority and generated docs are identified;
- evidence boundaries remain explicit;
- no upstream repository is modified.

Observed inventory result:

- All six repositories expose a repository-specific entry point and contribution/development signals.
- The mature and large projects expose dedicated API, architecture, testing, release, operations, migration, or build surfaces rather than one universal README.
- The small CLI exposes a compact surface, confirming that the skill must support a bounded path without enterprise ceremony.
- The API tree inventory is structural evidence only; it does not prove that every command, test, release, or production workflow passes.
