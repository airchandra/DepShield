.PHONY: help dev dev-backend dev-frontend build install-deps

help:
	@echo "DepShield UI Development"
	@echo ""
	@echo "Available targets:"
	@echo "  make install-deps        - Install all dependencies"
	@echo "  make dev                 - Run both backend and frontend in watch mode"
	@echo "  make dev-backend         - Run backend only"
	@echo "  make dev-frontend        - Run frontend only"
	@echo "  make build-backend       - Build backend Docker image"
	@echo "  make build-frontend      - Build frontend for production"
	@echo "  make build               - Build both for production"

install-deps:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

dev: dev-backend dev-frontend

dev-backend:
	cd backend && uvicorn main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

build-frontend:
	cd frontend && npm run build

build:
	make build-frontend
	@echo "✅ Frontend built to ui/frontend/dist/"

clean:
	rm -rf frontend/dist frontend/node_modules
	find backend -type d -name __pycache__ -exec rm -rf {} +
	find backend -type f -name "*.pyc" -delete
