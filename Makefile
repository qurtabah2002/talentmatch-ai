.PHONY: help dev-backend dev-frontend dev train test lint clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Development ──────────────────────────────────────────

dev-backend: ## Start backend dev server (port 8001)
	cd backend && uvicorn app.main:app --reload --port 8001

dev-frontend: ## Start frontend dev server (port 3001)
	cd frontend && npm run dev

dev: ## Start both backend and frontend
	$(MAKE) dev-backend & $(MAKE) dev-frontend

# ── ML ───────────────────────────────────────────────────

train: ## Train the model (logs to MLflow)
	cd backend && python -m app.ml.train

# ── Testing ──────────────────────────────────────────────

test: ## Run all tests
	cd backend && python -m pytest tests/ -v

test-fairness: ## Run fairness evaluation
	cd backend && python -c "from app.ml.train import train; train()"

# ── Lint ─────────────────────────────────────────────────

lint: ## Lint backend + frontend
	cd backend && ruff check .
	cd frontend && npx tsc --noEmit

# ── Docker ───────────────────────────────────────────────

up: ## Start all services with Docker Compose
	docker compose up -d

down: ## Stop all services
	docker compose down

# ── Cleanup ──────────────────────────────────────────────

clean: ## Remove generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/app/ml/data/model.pkl
	rm -rf frontend/.next frontend/node_modules
