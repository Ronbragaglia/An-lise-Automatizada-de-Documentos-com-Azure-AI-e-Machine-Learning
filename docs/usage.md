# Guia de Uso

Este guia fornece exemplos e instruções detalhadas para usar o sistema de detecção de fraudes em documentos.

## 📋 Índice

- [Interface de Linha de Comando (CLI)](#interface-de-linha-de-comando-cli)
- [Uso como Biblioteca Python](#uso-como-biblioteca-python)
- [Exemplos Práticos](#exemplos-práticos)
- [Dicas e Melhores Práticas](#dicas-e-melhores-práticas)

## 🖥️ Interface de Linha de Comando (CLI)

### Comandos Disponíveis

```bash
python -m src.cli --help
```

### Analisar um Documento

```bash
python -m src.cli analyze documento.pdf
```

**Saída:**

```
🚀 Iniciando análise de 1 documento(s)...
============================================================

📊 Resultados da Análise:
============================================================

1. ✅ documento.pdf
   Score de Fraude: 0.25
   Classificação: Autêntico
   Tem QR Code: Sim
   Palavras Suspeitas: Não

============================================================
📈 Estatísticas:
   Total: 1
   Autênticos: 1
   Suspeitos: 0
   Score Médio: 0.25
============================================================
```

### Analisar Múltiplos Documentos

```bash
python -m src.cli analyze doc1.pdf doc2.pdf doc3.pdf
```

### Analisar Diretório Inteiro

```bash
python -m src.cli analyze-dir ./data/documents
```

### Treinar Modelo

```bash
python -m src.cli train
```

### Ver Estatísticas

```bash
python -m src.cli stats
```

**Saída:**

```
📊 Estatísticas de Detecção de Fraudes
============================================================
Total de Detecções: 10
Documentos Autênticos: 8
Documentos Suspeitos: 2
Score Médio de Fraude: 0.35
============================================================

📋 Últimas Detecções:
============================================================
timestamp                file_path    text_length  has_qrcode  has_suspicious_words  fraud_score  classification
2025-01-15 10:30:00  doc1.pdf      500          True         False                0.25         Autêntico
2025-01-15 10:31:00  doc2.pdf      300          False        True                 0.75         Suspeito de Fraude
============================================================
```

### Limpar Logs

```bash
python -m src.cli clear-logs
```

## 🐍 Uso como Biblioteca Python

### Detecção Básica

```python
from src.detector import FraudDetector
from src.logger import FraudDetectionLogger

# Inicializar detector
detector = FraudDetector()

# Detectar fraude em um documento
result = detector.detect("documento.pdf")

# Exibir resultado
print(f"Score de Fraude: {result['fraud_score']:.2f}")
print(f"Classificação: {result['classification']}")

# Logar resultado
logger = FraudDetectionLogger()
logger.log_detection(result)
logger.log_to_csv(result)
```

### Detecção em Lote

```python
from src.detector import FraudDetector

# Inicializar detector
detector = FraudDetector()

# Lista de documentos
file_paths = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

# Detectar em lote
results = detector.batch_detect(file_paths)

# Processar resultados
for result in results:
    if "error" in result:
        print(f"❌ {result['file_path']}: {result['error']}")
    else:
        print(f"✅ {result['file_path']}: {result['classification']}")
```

### Análise de Documentos

```python
from src.document_analyzer import DocumentAnalyzer

# Inicializar analisador
analyzer = DocumentAnalyzer()

# Analisar documento
analysis = analyzer.analyze("documento.pdf")

# Exibir informações
print(f"Texto: {analysis['text'][:100]}...")
print(f"Tem QR Code: {analysis['has_qrcode']}")
print(f"Características: {analysis['features']}")
```

### Verificação de QR Code

```python
from src.qr_verifier import QRCodeVerifier

# Inicializar verificador
verifier = QRCodeVerifier()

# Verificar se tem QR Code
has_qrcode = verifier.verify("documento.png")
print(f"Tem QR Code: {has_qrcode}")

# Obter dados do QR Code
qr_data = verifier.get_qr_data("documento.png")
print(f"Dados do QR Code: {qr_data}")

# Obter posição do QR Code
position = verifier.get_qr_position("documento.png")
print(f"Posição: {position}")
```

### Treinamento Personalizado

```python
import numpy as np
from src.detector import FraudDetector

# Dados de treinamento
X_train = np.array([
    [500, 1, 0],   # [tamanho_texto, tem_qrcode, tem_palavras_suspeitas]
    [300, 0, 1],
    [800, 1, 0],
    [200, 0, 1],
])
y_train = np.array([0, 1, 0, 1])  # 0=autêntico, 1=fraude

# Criar e treinar detector
detector = FraudDetector()
detector.train(X_train, y_train)

# Usar modelo treinado
result = detector.detect("documento.pdf")
```

### Threshold Personalizado

```python
from src.detector import FraudDetector

# Criar detector com threshold personalizado
detector = FraudDetector(threshold=0.7)

# Detectar fraude
result = detector.detect("documento.pdf")

# O threshold personalizado afetará a classificação
print(f"Threshold: {result['threshold']}")
print(f"Classificação: {result['classification']}")
```

### Obter Importância das Características

```python
from src.detector import FraudDetector

detector = FraudDetector()

# Obter importância das características
importance = detector.get_feature_importance()

# Exibir
for feature, value in importance.items():
    print(f"{feature}: {value:.4f}")
```

## 📚 Exemplos Práticos

### Exemplo 1: Validação de Documentos de RH

```python
from src.detector import FraudDetector
from src.logger import FraudDetectionLogger
from pathlib import Path

detector = FraudDetector()
logger = FraudDetectionLogger()

# Diretório com documentos de candidatos
docs_dir = Path("data/rh_documents")

# Processar todos os documentos
for doc_path in docs_dir.glob("*.pdf"):
    result = detector.detect(str(doc_path))

    # Logar resultado
    logger.log_detection(result)
    logger.log_to_csv(result)

    # Ação baseada no resultado
    if result["classification"] == "Suspeito de Fraude":
        print(f"⚠️ Documento suspeito: {doc_path.name}")
        # Enviar para revisão manual
    else:
        print(f"✅ Documento válido: {doc_path.name}")
```

### Exemplo 2: Auditoria de Documentos Financeiros

```python
from src.detector import FraudDetector
from src.logger import FraudDetectionLogger
import pandas as pd

detector = FraudDetector()
logger = FraudDetectionLogger()

# Lista de documentos para auditoria
documents = [
    "fatura_jan.pdf",
    "fatura_fev.pdf",
    "fatura_mar.pdf"
]

# Detectar fraudes
results = detector.batch_detect(documents)

# Criar relatório
report_data = []
for result in results:
    if "error" not in result:
        report_data.append({
            "documento": result["file_path"],
            "score": result["fraud_score"],
            "classificacao": result["classification"],
            "tem_qrcode": result["has_qrcode"]
        })

# Salvar relatório
report_df = pd.DataFrame(report_data)
report_df.to_csv("auditoria_financeira.csv", index=False)
print("📄 Relatório salvo: auditoria_financeira.csv")
```

### Exemplo 3: Monitoramento Contínuo

```python
import time
from pathlib import Path
from src.detector import FraudDetector
from src.logger import FraudDetectionLogger

detector = FraudDetector()
logger = FraudDetectionLogger()

watch_dir = Path("data/novos_documentos")

print("👀 Monitorando diretório...")

while True:
    # Verificar novos arquivos
    for file_path in watch_dir.glob("*"):
        if file_path.is_file() and file_path.suffix in [".pdf", ".png", ".jpg"]:
            print(f"📄 Processando: {file_path.name}")

            result = detector.detect(str(file_path))

            # Logar e mover
            logger.log_detection(result)
            logger.log_to_csv(result)

            # Mover para processado
            processed_dir = watch_dir / "processados"
            processed_dir.mkdir(exist_ok=True)
            file_path.rename(processed_dir / file_path.name)

    # Aguardar antes de verificar novamente
    time.sleep(60)  # 1 minuto
```

## 💡 Dicas e Melhores Práticas

### 1. Validação de Entrada

Sempre valide os arquivos antes de processar:

```python
from pathlib import Path
from src.config import config

def validate_file(file_path: str) -> bool:
    """Valida se o arquivo é suportado."""
    path = Path(file_path)

    if not path.exists():
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False

    if path.suffix.lower() not in config.SUPPORTED_FORMATS:
        print(f"❌ Formato não suportado: {path.suffix}")
        return False

    return True
```

### 2. Tratamento de Erros

Implemente tratamento adequado de erros:

```python
from src.detector import FraudDetector

detector = FraudDetector()

try:
    result = detector.detect("documento.pdf")
    print(f"✅ Análise concluída: {result['classification']}")
except FileNotFoundError:
    print("❌ Arquivo não encontrado")
except ValueError as e:
    print(f"❌ Erro de validação: {e}")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
```

### 3. Logging Adequado

Use o sistema de logging para auditoria:

```python
from src.logger import FraudDetectionLogger

logger = FraudDetectionLogger()

# Logar todas as detecções
logger.log_detection(result)

# Logar para CSV para análise posterior
logger.log_to_csv(result)

# Ver estatísticas periodicamente
stats = logger.get_statistics()
print(f"📊 Total: {stats['total_detections']}")
print(f"🔴 Suspeitos: {stats['fraudulent']}")
print(f"✅ Autênticos: {stats['authentic']}")
```

### 4. Otimização de Performance

Para processar muitos documentos, use batch processing:

```python
from src.detector import FraudDetector
from pathlib import Path

detector = FraudDetector()

# Processar em lotes de 10
batch_size = 10
file_paths = list(Path("data").glob("*.pdf"))

for i in range(0, len(file_paths), batch_size):
    batch = file_paths[i:i + batch_size]
    results = detector.batch_detect([str(f) for f in batch])

    print(f"📦 Processando lote {i//batch_size + 1}")
```

### 5. Configuração de Threshold

Ajuste o threshold conforme suas necessidades:

```python
# Threshold mais conservador (menos falsos positivos)
detector_strict = FraudDetector(threshold=0.7)

# Threshold mais liberal (menos falsos negativos)
detector_liberal = FraudDetector(threshold=0.3)
```

### 6. Manutenção do Modelo

Retreine o modelo periodicamente com novos dados:

```python
import numpy as np
from src.detector import FraudDetector

# Carregar novos dados de treinamento
X_new = np.array([...])
y_new = np.array([...])

# Retreinar modelo
detector = FraudDetector()
detector.train(X_new, y_new)

# Avaliar novo modelo
metrics = detector.evaluate(X_test, y_test)
print(f"Nova acurácia: {metrics['accuracy']:.2f}")
```

## 🔗 Recursos Adicionais

- [API Reference](api-reference.md) - Documentação completa da API
- [Exemplos](../examples/) - Código de exemplo
- [Arquitetura](architecture.md) - Detalhes técnicos do sistema
- [FAQ](faq.md) - Perguntas frequentes

---

**Versão**: 1.0.0 | **Última Atualização**: 2025
