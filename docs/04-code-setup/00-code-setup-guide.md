# Step 4: Code Setup (Phase 0) — Mentor Guide

> Goal: create a **working, tested repository with CI running**, so you can start implementing Phase 1 directly.
> Estimate: **11 hours** (backlog tasks P0-01 through P0-07). Starter files are in the `opspilot/` folder. **Do not copy files without understanding them**; this guide explains the purpose of each file.
> I ran all Python checks on the starter (lint, type checks, boundary rules, and tests), and they passed. **I could not run Docker/Compose in my environment**, so test that part on your machine first. If an error occurs, share the complete output.

---

## 0. First, start the product track (10 minutes)

Since you plan to sell the product, do these alongside coding:
1. Read the [product brief](../01-product/17-product-brief-and-positioning.md) and [customer discovery plan](../01-product/18-customer-discovery-plan.md).
2. **Send three outreach messages this week** to people working in HR or operations. Use the template in the [customer discovery plan](../01-product/18-customer-discovery-plan.md).
3. **Check your employment terms:** See section 2 of the [commercial readiness checklist](../01-product/20-commercial-readiness-checklist.md). Your offer letter includes a confidentiality clause. Read the full agreement and policies, then ask HR in writing whether side projects are allowed. Resolve this before selling the product.

Doing this now will give you evidence for Gate A in November.

---

## 1. What we are setting up (Phase 0 overview)

```
opspilot/
├── backend/
│   ├── app/
│   │   ├── main.py             # Creates the app and registers routers
│   │   ├── core/               # Configuration and health checks (foundation for all modules)
│   │   ├── api/                # Thin HTTP layer with Phase 1 routes
│   │   └── modules/            # 10 ta module, prottek-ta: service.py (public), models.py, repository.py (private)
│   ├── tests/
│   ├── pyproject.toml          # dependencies + tool config + module boundary rules
│   ├── uv.lock                 # exact version lock
│   └── Dockerfile
├── infra/postgres/init/        # Enables the pgvector extension on initial database creation
├── docker-compose.yml          # api + postgres(pgvector) + redis + storage (SeaweedFS)
├── .github/                    # CI workflow, dependabot, issue/PR templates
├── .pre-commit-config.yaml     # Automatic checks before each commit
├── Makefile                    # shortcut: make up / make check
├── scripts/create_labels.sh    # GitHub label bulk create
└── docs/                       # Project documentation
```

**Exit criteria (end of Phase 0):** [ ] All services are healthy after `make up` [ ] `make check` passes [ ] CI is green and blocks a failing pull request [ ] The project board and Phase 1 issues are ready.

---

## 2. Tooling decisions (why these tools)

| Tool | Purpose | Why | Alternative |
|---|---|---|---|
| **uv** | Python version, dependencies, and virtual environment | Fast; one tool handles everything and creates a lockfile | pip + venv, Poetry |
| **FastAPI** | Web framework | Async support, type hints, and automatic OpenAPI | Django (in your broader plan, but not used by OpsPilot) |
| **pydantic-settings** | Environment-based configuration | Type-safe settings and validation | python-dotenv |
| **ruff** | Linting and formatting | One fast tool | flake8 + black + isort |
| **mypy (strict)** | Static type checking | Finds bugs early | pyright |
| **pytest** | Test | Industry standard | unittest |
| **import-linter** | Module boundary rules | Enforces modular-monolith boundaries in CI | Manual review |
| **pre-commit** | Checks before a commit | Prevents poor-quality code from entering the repository | CI only |
| **Docker Compose** | Local service stack | Starts everything with one command | Podman compose |
| **pgvector image** | Postgres with the vector extension ready | No manual extension setup | Build a custom image |
| **SeaweedFS** | Local S3-compatible storage | MinIO has been archived (ADR-0010) | Garage |

---

## 3. Task walkthrough

### P0-01: Repo + docs (1.5 h)

```bash
mkdir opspilot && cd opspilot
git init -b main
# Copy the starter files from the opspilot/ folder into this folder.
# Add the project documentation under docs/ (product, design decisions, plans, and setup).
git add -A && git commit -m "chore: initial project skeleton and docs"
```

Create a **private** GitHub repository first; the documentation contains business hypotheses and pricing.
```bash
git remote add origin git@github.com:<you>/opspilot.git
git push -u origin main
```
If you do not have an SSH key, run `ssh-keygen -t ed25519 -C "your@email"`, then add the public key under GitHub Settings > SSH keys.

**Check:** Mermaid diagrams render in the `docs/` folder on GitHub.

**Why `.gitignore` matters:** Never commit `.env` (secrets) or `.venv`. Commit `.env.example`, which contains variable names and descriptions only.

### P0-02: Fedora dev environment (2 h)

**Docker Engine** (see the official installation guide at `docs.docker.com/engine/install/fedora/`; commands may differ across Fedora and DNF versions):

```bash
sudo dnf -y install dnf-plugins-core
# For newer Fedora versions using DNF5:
sudo dnf config-manager addrepo --from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER       # tarpor logout/login
docker run hello-world
docker compose version
```
Note: Membership in the `docker` group grants root-equivalent privileges. This may be acceptable on your personal laptop, but understand the security implications.

**Podman is an alternative and may already be installed on Fedora:** use `podman compose` or `podman-compose`. This guide assumes Docker. Whichever option you choose, **record it in the README**.

**uv ar Python:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh       # tarpor notun terminal
uv --version
uv python install 3.12
```

**Git config:**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```
Optional: install GitHub CLI with `sudo dnf install gh`, then run `gh auth login` (needed by the label script).

**Check:** `docker run hello-world` and `uv --version` both run successfully.

### P0-03: Backend skeleton (2 h)

```bash
cd backend
uv sync                  # Creates .venv and installs dependencies from the lockfile
uv run pytest            # 6 ta test pass
uv run ruff check .
uv run ruff format --check .
uv run mypy app tests
uv run lint-imports      # 12 ta contract KEPT
```

Now read these files and understand their purpose:

| File | Purpose | Question to understand |
|---|---|---|
| `app/main.py` | `create_app()` factory that registers routers | Why use a factory? Tests can create separate app instances |
| `app/core/config.py` | Loads `Settings` from the environment | Why is hard-coded configuration a problem? |
| `app/core/health.py` | `/health/live` and `/health/ready` endpoints | Liveness versus readiness (see below) |
| `modules/*/service.py` | The module's public interface | Other modules should import only this interface |
| `modules/*/models.py, repository.py` | Private implementation | CI fails if another module imports these directly |
| `pyproject.toml` `[tool.importlinter]` | Module boundary rules | Lower layers must not import upper layers |
| `tests/test_health.py` | Health check test | Simulate a database outage with a dependency override |

**Liveness vs Readiness:**
- **Live** = Is the process running? If this check fails, restart the container.
- **Ready** = Can the service handle work (for example, is the database available)? If this check fails, stop sending traffic, but do not restart automatically.
These distinctions are important in Kubernetes and are useful to understand now.

**Pre-commit install:**
```bash
cd .. && make hooks
git commit --allow-empty -m "test: hooks"      # Verify that the hook runs
```

### P0-04: Docker Compose (2 h)

```bash
cp .env.example .env         # Edit .env and make the passwords match in both settings
make up
make ps                      # Ready when every service reports "healthy"
curl localhost:8000/health/live
curl localhost:8000/health/ready
```

**Compose file concepts to understand:**

| Line or concept | Meaning |
|---|---|
| `build.target: dev` | The Dockerfile's `dev` stage, including test and lint tools |
| `volumes: ./backend/app:/app/app:z` | Mounts source code for live reload. `:z` sets an **SELinux label** |
| `depends_on ... condition: service_healthy` | The API waits for the database to become healthy |
| `healthcheck` | Docker checks the service's health |
| `pgdata` volume | Data persists even after a container is deleted |
| `infra/postgres/init/*.sql` | Runs `CREATE EXTENSION vector` when the database is first created |
| `storage` (SeaweedFS) | Local S3-compatible storage. **It has no authentication; do not expose it publicly.** |

**Verify that pgvector is enabled:**
```bash
docker compose exec db psql -U opspilot -d opspilot -c "\dx"
```
The output should include `vector`.

There is no **worker** yet. It is added in Phase 2 (P2-06).

### P0-05: Health endpoint test (1 h)

The test is already in place. **Now try it with a real database:**
```bash
docker compose stop db
curl -i localhost:8000/health/ready      # Expected result: 503
docker compose start db
curl -i localhost:8000/health/ready      # kichukkhon por 200
```
This demonstrates readiness behavior. The test currently uses a simulated database check; a real-database integration test will be added in Phase 1.

### P0-06: CI + branch protection (1.5 h)

`.github/workflows/ci.yml` prottek PR-e: install, lint, format check, mypy, boundaries, tests.

In the GitHub repository, open **Settings > Branches** (or Rules) and add a rule for `main`: require pull requests and the **`backend` status check**, and disable force pushes.
(GitHub may change menu names; look for "branch protection" or "rulesets." Some features depend on your private-repository plan.)

**Test this; it is required:**
```bash
git switch -c test/failing-ci
# Temporarily change a test in tests/test_health.py to "assert 1 == 2".
git commit -am "test: prove CI blocks" && git push -u origin test/failing-ci
```
Open a pull request: CI should fail and block merging. Then delete the test branch.

**Dependabot:** `.github/dependabot.yml` opens weekly pull requests for GitHub Actions, uv, and Docker updates. Review and merge each update to keep dependencies maintained.

### P0-07: Board, labels, templates (1 h)

```bash
gh auth login
./scripts/create_labels.sh
```
Create a GitHub Projects board with Backlog, Ready, In Progress, In Review, and Done columns. Create a milestone for each phase (`Phase 0 Setup` through `Phase 8`). Create GitHub issues for the **12 Phase 1 tasks** in [the backlog](../03-planning/14-backlog.md), using the task template. Schedule a weekly review for Sunday.

---

## 4. Break-it exercise (30 minutes)

| # | Action | Expected result | Lesson |
|---|---|---|---|
| 1 | Add `from app.modules.documents import models` to `app/modules/chat/service.py` | `make boundaries` fails | Private implementation boundaries |
| 2 | Add `from app.modules.chat import service` to `app/modules/documents/service.py` | `make boundaries` fails (layering rule) | Dependency direction |
| 3 | Remove a function's type hint in `health.py` | `make typecheck` fails | Strict typing |
| 4 | Add an unused import and commit it | pre-commit fixes it or blocks the commit | The hook is working |
| 5 | `docker compose stop db` | `/health/ready` 503 | Readiness |
| 6 | Put the wrong database password in `.env`, then run `make up` | API logs an error and readiness returns 503 | Debugging configuration errors |
| 7 | Run `docker compose down -v`, then `make up` again | Database data is removed and the extension is recreated | What a volume does |

After each exercise, write two lines in `docs/notes/phase0.md` describing **what happened and why**.

---

## 5. Fedora troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `permission denied ... docker.sock` | The user is not in the Docker group or has not logged in again | Run `sudo usermod -aG docker $USER`, then log out and back in |
| `Permission denied` on a mounted directory in a container | **SELinux** label | Add `:z` or `:Z` to the volume and inspect with `ls -Z`; never disable SELinux |
| `port is already allocated` (5432, 6379, 8000) | Another Postgres or Redis service is using the host port | Run `sudo ss -ltnp | grep 5432`, stop that service, or change `POSTGRES_PORT` in `.env` |
| `docker compose` command is missing | Compose plugin is not installed | Install `docker-compose-plugin` |
| `depends_on condition` does not work in Podman | Podman Compose version | Upgrade Podman Compose or use Docker |
| API is `unhealthy` | Check `docker compose logs api` | Often caused by a `.env` or database-password mismatch |
| `uv: command not found` | PATH has not been updated | Open a new terminal and check whether `~/.local/bin` is in PATH |
| `uv sync` cannot find Python | Python 3.12 is missing | Run `uv python install 3.12` |
| `uv.lock` is missing during build | Lockfile was not committed | Run `cd backend && uv lock`, then commit the file |
| SeaweedFS image pull fails | Invalid tag or network issue | Run `docker pull chrislusf/seaweedfs` or check for a current tag |
| Redis health check fails | Image-specific issue | Check `docker compose logs redis` |

---

## 6. What I tested in the starter and what I did not

| Area | Status |
|---|---|
| `ruff`, `mypy`, `lint-imports`, `pytest` (6 tests), `uv lock/sync` | **Run and passed** |
| Boundary rule violations (private import, upward import) | **Run and verified to fail** |
| Pre-commit hooks (in a fresh Git repository) | **Run and passed** |
| GitHub Actions workflow | Written, but **verify it on the first run in your repository** |
| `docker compose up`, Dockerfile build, health checks, SeaweedFS | **Not tested** (Docker was unavailable in my environment). Share the output if the first run fails |
| Tool versions (action versions, image tags) | Current when this guide was written; Dependabot may update them. Check the SeaweedFS tag yourself |

---

## 7. Phase 0 completion checklist

- [ ] All services are healthy after `make up`; `/health/ready` returns 200
- [ ] `make check` pass
- [ ] CI is green and a failing pull request is blocked (verified)
- [ ] Hooks cholche
- [ ] Documentation is in the repository and Mermaid diagrams render
- [ ] Board, labels, milestones, Phase 1 issues ready
- [ ] `docs/notes/phase0.md`-te exercise note
- [ ] Complete [Phase 0 learning checkpoints](../03-planning/16-learning-checkpoints.md)
- [ ] Three outreach messages sent and the employment-policy review started
- [ ] Phase 0 retrospective recorded in `docs/retros/phase0.md`: estimated versus actual hours, what went well, and what did not
- [ ] Tag: `git tag v0.0.1 && git push --tags`

Record **estimated versus actual effort** to measure your velocity. Use it to recalibrate the remaining plan.

---

## 8. Next step

After Phase 0, begin **Phase 1: Foundation**. Start with settings and structured logging (P1-01), then the database layer and Alembic (P1-02), followed by the **RLS spike (P1-03)**. Work through the spike step by step. Revisit this guide when Phase 0 is complete or if you get stuck.
