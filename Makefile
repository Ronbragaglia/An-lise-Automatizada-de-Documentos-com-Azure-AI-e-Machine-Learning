.PHONY: help install install-dev test lint format clean build run docker-build docker-run docker-stop jupyter

# Variáveis
PYTHON := python3
VENV := venv
ACTIVATE := $(VENV)/bin/activate
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black
ISORT := $(VENV)/bin/isort
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy

help: ## Mostra esta mensagem de ajuda
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos disponíveis:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Configura o ambiente de desenvolvimento
	@echo "🚀 Configurando ambiente de desenvolvimento..."
	$(PYTHON) -m venv $(VENV)
	. $(ACTIVATE) && $(PIP) install --upgrade pip
	. $(ACTIVATE) && $(PIP) install -e ".[dev,jupyter]"
	@echo "✅ Ambiente configurado com sucesso!"

install: ## Instala as dependências do projeto
	@echo "📦 Instalando dependências..."
	. $(ACTIVATE) && $(PIP) install -r requirements.txt
	@echo "✅ Dependências instaladas!"

install-dev: ## Instala dependências de desenvolvimento
	@echo "📦 Instalando dependências de desenvolvimento..."
	. $(ACTIVATE) && $(PIP) install -e ".[dev,jupyter]"
	@echo "✅ Dependências de desenvolvimento instaladas!"

test: ## Executa os testes
	@echo "🧪 Executando testes..."
	. $(ACTIVATE) && $(PYTEST) tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "✅ Testes concluídos!"

test-unit: ## Executa apenas testes unitários
	@echo "🧪 Executando testes unitários..."
	. $(ACTIVATE) && $(PYTEST) tests/ -v -m unit
	@echo "✅ Testes unitários concluídos!"

test-integration: ## Executa apenas testes de integração
	@echo "🧪 Executando testes de integração..."
	. $(ACTIVATE) && $(PYTEST) tests/ -v -m integration
	@echo "✅ Testes de integração concluídos!"

lint: ## Verifica o estilo do código
	@echo "🔍 Verificando estilo do código..."
	. $(ACTIVATE) && $(FLAKE8) src/ tests/
	@echo "✅ Verificação de estilo concluída!"

format: ## Formata o código automaticamente
	@echo "🎨 Formatando código..."
	. $(ACTIVATE) && $(BLACK) src/ tests/
	. $(ACTIVATE) && $(ISORT) src/ tests/
	@echo "✅ Código formatado!"

type-check: ## Verifica tipos com mypy
	@echo "🔍 Verificando tipos..."
	. $(ACTIVATE) && $(MYPY) src/
	@echo "✅ Verificação de tipos concluída!"

check: lint type-check ## Executa todas as verificações (lint + type-check)
	@echo "✅ Todas as verificações concluídas!"

clean: ## Limpa arquivos temporários e caches
	@echo "🧹 Limpando arquivos temporários..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg 2>/dev/null || true
	@echo "✅ Limpeza concluída!"

build: ## Constrói o pacote do projeto
	@echo "🔨 Construindo pacote..."
	. $(ACTIVATE) && $(PYTHON) -m build
	@echo "✅ Pacote construído!"

run: ## Executa a aplicação
	@echo "🚀 Executando aplicação..."
	. $(ACTIVATE) && $(PYTHON) -m src.cli

jupyter: ## Inicia o Jupyter Notebook
	@echo "📓 Iniciando Jupyter Notebook..."
	. $(ACTIVATE) && jupyter notebook

docker-build: ## Constrói a imagem Docker
	@echo "🐳 Construindo imagem Docker..."
	docker-compose build

docker-run: ## Executa os containers Docker
	@echo "🐳 Executando containers Docker..."
	docker-compose up -d

docker-stop: ## Para os containers Docker
	@echo "🛑 Parando containers Docker..."
	docker-compose down

docker-logs: ## Mostra os logs dos containers Docker
	@echo "📋 Mostrando logs..."
	docker-compose logs -f

docker-clean: ## Remove containers e volumes Docker
	@echo "🧹 Limpando Docker..."
	docker-compose down -v
	docker system prune -f

train-model: ## Treina o modelo de detecção de fraudes
	@echo "🤖 Treinando modelo..."
	. $(ACTIVATE) && $(PYTHON) -m src.train_model
	@echo "✅ Modelo treinado!"

analyze: ## Analisa um documento (uso: make analyze FILE=path/to/document.pdf)
	@echo "📄 Analisando documento..."
	. $(ACTIVATE) && $(PYTHON) -m src.cli analyze $(FILE)

all: clean install-dev lint test ## Executa: clean + install-dev + lint + test

.DEFAULT_GOAL := help
