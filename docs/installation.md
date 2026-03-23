# Guia de Instalação

Este guia fornece instruções detalhadas para instalar e configurar o sistema de detecção de fraudes em documentos.

## 📋 Pré-requisitos

### Requisitos do Sistema

- **Python**: 3.9 ou superior
- **Sistema Operacional**: Linux, macOS ou Windows
- **Memória RAM**: Mínimo 4GB (recomendado 8GB)
- **Espaço em Disco**: Mínimo 1GB livre

### Requisitos do Azure

- Conta do Azure ativa
- Recurso de [Azure Form Recognizer](https://azure.microsoft.com/en-us/services/ai-services/form-recognizer/)
- Chave de API e Endpoint do serviço

## 🔧 Instalação Local

### 1. Clone o Repositório

```bash
git clone https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning.git
cd An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning
```

### 2. Crie um Ambiente Virtual

**Linux/macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Para desenvolvimento, instale as dependências extras:

```bash
pip install -e ".[dev,jupyter]"
```

### 4. Configure o Azure

#### 4.1 Criar um Recurso do Azure Form Recognizer

1. Acesse o [Portal do Azure](https://portal.azure.com/)
2. Clique em "Criar um recurso"
3. Pesquise por "Form Recognizer"
4. Clique em "Criar"
5. Preencha os campos obrigatórios:
   - **Nome do recurso**: Escolha um nome único
   - **Assinatura**: Selecione sua assinatura
   - **Grupo de recursos**: Crie ou selecione um existente
   - **Região**: Escolha a região mais próxima de você
   - **Camada de preços**: Selecione a camada adequada (F0 é gratuita)
6. Clique em "Revisar + criar" e depois em "Criar"
7. Aguarde a implantação ser concluída

#### 4.2 Obter Chave e Endpoint

1. Acesse o recurso criado no Portal do Azure
2. No menu lateral, clique em "Chaves e Endpoint"
3. Copie a **Chave** e o **Endpoint**

#### 4.3 Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# Azure Form Recognizer Configuration
AZURE_FORM_RECOGNIZER_ENDPOINT=https://seu-resource.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=sua-chave-aqui

# Application Configuration
APP_NAME=Document Fraud Detection
APP_VERSION=1.0.0
APP_ENV=development

# Model Configuration
MODEL_NAME=fraud_detection_model
MODEL_VERSION=1.0.0
MODEL_PATH=models/

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Data Configuration
DATA_DIR=data/
OUTPUT_DIR=output/

# Thresholds
FRAUD_THRESHOLD=0.5
QR_CODE_REQUIRED=true
```

### 5. Verifique a Instalação

```bash
python -m src.cli --help
```

Você deve ver a mensagem de ajuda da CLI.

## 🐳 Instalação com Docker

### Usando Docker Compose (Recomendado)

```bash
# Construir e executar os containers
docker-compose up -d

# Verificar os logs
docker-compose logs -f

# Parar os containers
docker-compose down
```

### Usando Dockerfile

```bash
# Construir a imagem
docker build -t document-fraud-detection .

# Executar o container
docker run -it --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -e AZURE_FORM_RECOGNIZER_KEY=sua-chave \
  -e AZURE_FORM_RECOGNIZER_ENDPOINT=https://seu-endpoint \
  document-fraud-detection
```

## 📦 Instalação como Pacote Python

### Instalação do Repositório Local

```bash
cd An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning
pip install -e .
```

### Uso como Pacote

```python
from src.detector import FraudDetector
from src.logger import FraudDetectionLogger

detector = FraudDetector()
result = detector.detect("documento.pdf")

logger = FraudDetectionLogger()
logger.log_detection(result)
```

## 🔨 Desenvolvimento

### Configuração do Ambiente de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning.git
cd An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências de desenvolvimento
pip install -e ".[dev,jupyter]"

# Instale os pre-commit hooks (opcional)
pre-commit install
```

### Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com coverage
pytest --cov=src --cov-report=html

# Executar apenas testes unitários
pytest -m unit
```

### Formatar e Verificar Código

```bash
# Formatar código com Black
black src/ tests/

# Ordenar imports com isort
isort src/ tests/

# Verificar estilo com flake8
flake8 src/ tests/

# Verificar tipos com mypy
mypy src/
```

## 🌐 Google Colab

Para usar no Google Colab:

1. Abra o notebook [Análise Automatizada de Documentos](../Análise_Automatizada_de_Documentos_com_Azure_AI_e_Machine_Learning_para_Detecção_de_Fraudes.ipynb)
2. Execute as células de instalação
3. Configure suas credenciais do Azure nas células apropriadas

## ⚠️ Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'src'"

**Solução**: Instale o pacote em modo de desenvolvimento:

```bash
pip install -e .
```

### Erro: "Azure authentication failed"

**Solução**: Verifique se suas credenciais do Azure estão corretas no arquivo `.env`:

```env
AZURE_FORM_RECOGNIZER_ENDPOINT=https://seu-resource.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=sua-chave-aqui
```

### Erro: "OpenCV error"

**Solução**: Instale as dependências do sistema:

**Ubuntu/Debian:**

```bash
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

**macOS:**

```bash
brew install opencv
```

### Erro: "Permission denied" ao criar diretórios

**Solução**: Verifique as permissões dos diretórios:

```bash
chmod -R 755 data logs models output
```

### Erro: "Docker build failed"

**Solução**: Verifique se o Docker está instalado e rodando:

```bash
docker --version
docker ps
```

## 📚 Próximos Passos

Após a instalação bem-sucedida:

1. Leia o [Guia de Uso](usage.md) para aprender a usar o sistema
2. Explore os [Exemplos](../examples/) para ver casos de uso práticos
3. Consulte a [API Reference](api-reference.md) para detalhes técnicos
4. Entenda a [Arquitetura](architecture.md) do sistema

## 🔗 Recursos Adicionais

- [Documentação do Azure Form Recognizer](https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/)
- [Documentação do Scikit-learn](https://scikit-learn.org/stable/documentation.html)
- [Documentação do OpenCV](https://docs.opencv.org/)

---

**Versão**: 1.0.0 | **Última Atualização**: 2025
