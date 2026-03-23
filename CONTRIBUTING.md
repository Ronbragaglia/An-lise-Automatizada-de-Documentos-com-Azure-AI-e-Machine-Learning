# Contribuindo para Document Fraud Detection

Obrigado por se interessar em contribuir com o projeto Document Fraud Detection! Este documento fornece diretrizes e instruções para contribuir.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Documentação](#documentação)
- [Relatando Issues](#relatando-issues)
- [Pull Requests](#pull-requests)

## 🤝 Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e inclusivo:

- Seja respeitoso e construtivo
- Aceite e ofereça críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros da comunidade

## 🚀 Como Contribuir

### 1. Encontre um Issue para Trabalhar

- Procure issues marcadas com `good first issue` para começar
- Verifique issues marcadas com `help wanted` para contribuições mais complexas
- Comente no issue para informar que você vai trabalhar nele

### 2. Faça um Fork do Repositório

```bash
# Faça um fork do repositório no GitHub
# Clone seu fork localmente
git clone https://github.com/SEU_USUARIO/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning.git
cd An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning
```

### 3. Crie uma Branch

```bash
# Crie uma branch para sua feature
git checkout -b feature/sua-feature

# Ou para correção de bug
git checkout -b bugfix/correcao-do-bug
```

### 4. Faça as Alterações

- Siga os padrões de código definidos abaixo
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário

### 5. Commit suas Alterações

```bash
git add .
git commit -m "feat: adicionar nova funcionalidade de detecção"
```

### 6. Push e Crie um Pull Request

```bash
git push origin feature/sua-feature
```

Então, vá ao GitHub e crie um Pull Request.

## 🔄 Processo de Desenvolvimento

### Setup do Ambiente de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning.git
cd An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -e ".[dev]"

# Copie o arquivo de exemplo de ambiente
cp .env.example .env
# Edite o .env com suas configurações
```

### Executando Testes

```bash
# Execute todos os testes
pytest

# Execute com coverage
pytest --cov=src --cov-report=html

# Execute apenas testes unitários
pytest -m unit

# Execute apenas testes de integração
pytest -m integration
```

### Formatação de Código

```bash
# Formate o código com Black
black src/ tests/

# Ordene imports com isort
isort src/ tests/

# Verifique estilo com flake8
flake8 src/ tests/

# Verifique tipos com mypy
mypy src/
```

## 📐 Padrões de Código

### Convenções de Nomenclatura

- **Variáveis e Funções**: `snake_case`
- **Classes**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Módulos**: `snake_case`

### Estilo de Código

Seguimos as convenções PEP 8 e usamos ferramentas automáticas:

- **Black**: Formatação automática de código
- **isort**: Ordenação de imports
- **flake8**: Verificação de estilo
- **mypy**: Verificação de tipos

### Exemplo de Código

```python
"""Módulo de exemplo para detecção de fraudes."""

from typing import Optional
import pandas as pd


class FraudDetector:
    """Classe para detecção de fraudes em documentos."""

    def __init__(self, model_path: str, threshold: float = 0.5) -> None:
        """Inicializa o detector de fraudes.

        Args:
            model_path: Caminho para o modelo treinado.
            threshold: Limiar para classificação de fraude.
        """
        self.model_path = model_path
        self.threshold = threshold
        self.model = self._load_model()

    def _load_model(self) -> Any:
        """Carrega o modelo de detecção de fraudes.

        Returns:
            Modelo carregado.
        """
        # Implementação
        pass

    def detect(self, document: pd.DataFrame) -> dict:
        """Detecta fraude em um documento.

        Args:
            document: DataFrame com características do documento.

        Returns:
            Dicionário com resultados da detecção.
        """
        # Implementação
        pass
```

## 🧪 Testes

### Escrevendo Testes

- Escreva testes para novas funcionalidades
- Use `pytest` como framework de testes
- Mantenha testes independentes e rápidos
- Use fixtures para configuração de teste

### Exemplo de Teste

```python
import pytest
from src.detector import FraudDetector


@pytest.fixture
def detector():
    """Fixture para criar um detector de fraudes."""
    return FraudDetector(model_path="models/test_model.pkl")


def test_fraud_detection(detector):
    """Testa a detecção de fraudes."""
    document = pd.DataFrame({
        "text_length": [500],
        "has_qrcode": [1],
        "has_suspicious_words": [0]
    })
    
    result = detector.detect(document)
    
    assert "fraud_score" in result
    assert "classification" in result
    assert 0 <= result["fraud_score"] <= 1
```

## 📚 Documentação

### Atualizando a Documentação

- Mantenha a documentação atualizada com as mudanças
- Use docstrings para todas as funções e classes públicas
- Siga o formato Google Style para docstrings
- Adicione exemplos de uso quando apropriado

### Exemplo de Docstring

```python
def analyze_document(
    file_path: str,
    extract_features: bool = True
) -> dict:
    """Analisa um documento para detecção de fraudes.

    Esta função extrai texto e características do documento,
    verifica a autenticidade via QR Code e aplica o modelo
    de Machine Learning para detecção de fraudes.

    Args:
        file_path: Caminho para o arquivo do documento.
        extract_features: Se True, extrai características adicionais.

    Returns:
        Dicionário contendo:
            - text: Texto extraído do documento
            - features: Características extraídas
            - fraud_score: Score de fraude (0-1)
            - classification: Classificação do documento

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se o formato do arquivo não for suportado.

    Example:
        >>> result = analyze_document("document.pdf")
        >>> print(result["fraud_score"])
        0.25
    """
    pass
```

## 🐛 Relatando Issues

Ao relatar um issue, inclua:

- **Título**: Descrição clara e concisa
- **Descrição**: Detalhes completos do problema
- **Passos para Reproduzir**: Passos detalhados
- **Comportamento Esperado**: O que deveria acontecer
- **Comportamento Atual**: O que está acontecendo
- **Ambiente**:
  - Versão do Python
  - Versão do projeto
  - Sistema operacional
- **Logs**: Logs relevantes (se aplicável)

### Template de Issue

```markdown
## Descrição
Breve descrição do problema.

## Passos para Reproduzir
1. Primeiro passo
2. Segundo passo
3. ...

## Comportamento Esperado
O que deveria acontecer.

## Comportamento Atual
O que está acontecendo.

## Ambiente
- Python: 3.9.0
- Versão: 1.0.0
- OS: Ubuntu 20.04

## Logs
```
Logs relevantes aqui
```
```

## 🔀 Pull Requests

### Checklist para Pull Requests

Antes de enviar um PR, verifique:

- [ ] O código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Todos os testes passam
- [ ] Documentação foi atualizada
- [ ] Commits seguem o formato de mensagens
- [ ] PR descreve claramente as mudanças

### Formato de Mensagens de Commit

Usamos o formato Conventional Commits:

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Mudanças de estilo (formatação, etc.)
- `refactor`: Refatoração de código
- `test`: Adição ou modificação de testes
- `chore`: Mudanças no processo de build ou ferramentas

**Exemplos:**

```
feat(detector): adicionar suporte a novos formatos de documento

Implementa suporte para PDF e DOCX além de imagens.

Closes #123
```

```
fix(model): corrigir erro de predição com valores nulos

O modelo estava falhando quando recebia valores nulos
nas características. Agora trata esses casos adequadamente.
```

### Processo de Review

1. **Automated Checks**: CI/CD verifica estilo, testes e tipos
2. **Code Review**: Mantenedores revisam o código
3. **Aprovação**: Após aprovação, o PR é mergeado
4. **Release**: Mudanças são incluídas na próxima release

## 💬 Perguntas?

Se você tiver dúvidas sobre como contribuir:

1. Verifique a [documentação](docs/)
2. Procure issues similares
3. Abra uma nova issue com a tag `question`
4. Entre em contato com os mantenedores

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a licença MIT do projeto.

---

Obrigado por contribuir! 🎉
