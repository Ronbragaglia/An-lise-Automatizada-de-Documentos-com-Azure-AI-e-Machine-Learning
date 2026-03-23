# API Reference

Documentação completa da API do sistema de detecção de fraudes em documentos.

## 📋 Índice

- [FraudDetector](#frauddetector)
- [DocumentAnalyzer](#documentanalyzer)
- [QRCodeVerifier](#qrverifier)
- [FraudDetectionLogger](#frauddetectionlogger)
- [Config](#config)

---

## FraudDetector

Classe principal para detecção de fraudes em documentos.

### Inicialização

```python
FraudDetector(
    model_path: Optional[str] = None,
    threshold: Optional[float] = None
) -> None
```

**Parâmetros:**
- `model_path` (str, opcional): Caminho para o modelo treinado. Padrão: `models/fraud_model.joblib`
- `threshold` (float, opcional): Limiar para classificação de fraude (0-1). Padrão: 0.5

**Exemplo:**

```python
from src.detector import FraudDetector

detector = FraudDetector(
    model_path="models/meu_modelo.joblib",
    threshold=0.7
)
```

### Métodos

#### `train()`

Treina o modelo de detecção de fraudes.

```python
train(
    X_train: np.ndarray,
    y_train: np.ndarray
) -> None
```

**Parâmetros:**
- `X_train` (np.ndarray): Array de características de treinamento [n_samples, n_features]
- `y_train` (np.ndarray): Array de labels de treinamento [n_samples] (0=autêntico, 1=fraude)

**Exemplo:**

```python
import numpy as np

X_train = np.array([
    [500, 1, 0],   # [tamanho_texto, tem_qrcode, tem_palavras_suspeitas]
    [300, 0, 1],
])
y_train = np.array([0, 1])

detector.train(X_train, y_train)
```

#### `predict()`

Prediz se um documento é fraudulento baseado nas características.

```python
predict(
    features: pd.DataFrame
) -> Dict
```

**Parâmetros:**
- `features` (pd.DataFrame): DataFrame com as características do documento

**Retorna:**
- `Dict`: Dicionário com os resultados da predição:
  - `fraud_score` (float): Score de fraude (0-1)
  - `classification` (str): "Autêntico" ou "Suspeito de Fraude"
  - `threshold` (float): Limiar usado na classificação

**Exemplo:**

```python
import pandas as pd

features = pd.DataFrame({
    "text_length": [500],
    "has_qrcode": [1],
    "has_suspicious_words": [0]
})

result = detector.predict(features)
print(f"Score: {result['fraud_score']}")
print(f"Classificação: {result['classification']}")
```

#### `detect()`

Detecta fraude em um documento completo.

```python
detect(
    file_path: str
) -> Dict
```

**Parâmetros:**
- `file_path` (str): Caminho para o arquivo do documento

**Retorna:**
- `Dict`: Dicionário com os resultados da detecção:
  - `file_path` (str): Caminho do arquivo
  - `text_length` (int): Tamanho do texto extraído
  - `has_qrcode` (bool): Indica se tem QR Code
  - `has_suspicious_words` (bool): Indica se tem palavras suspeitas
  - `fraud_score` (float): Score de fraude (0-1)
  - `classification` (str): "Autêntico" ou "Suspeito de Fraude"
  - `threshold` (float): Limiar usado na classificação

**Exemplo:**

```python
result = detector.detect("documento.pdf")
print(f"Classificação: {result['classification']}")
print(f"Score: {result['fraud_score']:.2f}")
```

#### `batch_detect()`

Detecta fraude em múltiplos documentos.

```python
batch_detect(
    file_paths: List[str]
) -> List[Dict]
```

**Parâmetros:**
- `file_paths` (List[str]): Lista de caminhos para os arquivos

**Retorna:**
- `List[Dict]`: Lista de dicionários com os resultados da detecção

**Exemplo:**

```python
file_paths = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
results = detector.batch_detect(file_paths)

for result in results:
    print(f"{result['file_path']}: {result['classification']}")
```

#### `get_feature_importance()`

Retorna a importância das características do modelo.

```python
get_feature_importance() -> Dict[str, float]
```

**Retorna:**
- `Dict[str, float]`: Dicionário com a importância de cada característica

**Exemplo:**

```python
importance = detector.get_feature_importance()
for feature, value in importance.items():
    print(f"{feature}: {value:.4f}")
```

#### `evaluate()`

Avalia o modelo com dados de teste.

```python
evaluate(
    X_test: np.ndarray,
    y_test: np.ndarray
) -> Dict
```

**Parâmetros:**
- `X_test` (np.ndarray): Array de características de teste
- `y_test` (np.ndarray): Array de labels de teste

**Retorna:**
- `Dict`: Dicionário com métricas de avaliação:
  - `accuracy` (float): Acurácia do modelo
  - `precision` (float): Precisão do modelo
  - `recall` (float): Recall do modelo
  - `f1_score` (float): F1-Score do modelo
  - `confusion_matrix` (List[List[int]]): Matriz de confusão

**Exemplo:**

```python
metrics = detector.evaluate(X_test, y_test)
print(f"Acurácia: {metrics['accuracy']:.2f}")
print(f"F1-Score: {metrics['f1_score']:.2f}")
```

---

## DocumentAnalyzer

Classe para análise de documentos usando Azure AI Document Intelligence.

### Inicialização

```python
DocumentAnalyzer(
    endpoint: Optional[str] = None,
    key: Optional[str] = None
) -> None
```

**Parâmetros:**
- `endpoint` (str, opcional): Endpoint do Azure Form Recognizer
- `key` (str, opcional): Chave de API do Azure Form Recognizer

**Exemplo:**

```python
from src.document_analyzer import DocumentAnalyzer

analyzer = DocumentAnalyzer(
    endpoint="https://seu-resource.cognitiveservices.azure.com/",
    key="sua-chave"
)
```

### Métodos

#### `analyze()`

Analisa um documento completo.

```python
analyze(
    file_path: str
) -> Dict
```

**Parâmetros:**
- `file_path` (str): Caminho para o arquivo do documento

**Retorna:**
- `Dict`: Dicionário contendo os resultados da análise:
  - `file_path` (str): Caminho do arquivo
  - `text` (str): Texto extraído do documento
  - `has_qrcode` (bool): Indica se tem QR Code
  - `features` (Dict): Características extraídas

**Exemplo:**

```python
result = analyzer.analyze("documento.pdf")
print(f"Texto: {result['text'][:100]}...")
print(f"Tem QR Code: {result['has_qrcode']}")
```

#### `extract_text()`

Extrai texto de um documento usando Azure AI.

```python
extract_text(
    file_path: str
) -> str
```

**Parâmetros:**
- `file_path` (str): Caminho para o arquivo do documento

**Retorna:**
- `str`: Texto extraído do documento

**Exemplo:**

```python
text = analyzer.extract_text("documento.pdf")
print(text)
```

#### `extract_features()`

Extrai características do texto do documento.

```python
extract_features(
    text: str,
    has_qrcode: bool
) -> Dict
```

**Parâmetros:**
- `text` (str): Texto extraído do documento
- `has_qrcode` (bool): Indica se o documento tem QR Code

**Retorna:**
- `Dict`: Dicionário com as características extraídas

**Exemplo:**

```python
features = analyzer.extract_features(text, has_qrcode=True)
print(features)
```

#### `batch_analyze()`

Analisa múltiplos documentos em lote.

```python
batch_analyze(
    file_paths: List[str]
) -> List[Dict]
```

**Parâmetros:**
- `file_paths` (List[str]): Lista de caminhos para os arquivos

**Retorna:**
- `List[Dict]`: Lista de dicionários com os resultados da análise

**Exemplo:**

```python
file_paths = ["doc1.pdf", "doc2.pdf"]
results = analyzer.batch_analyze(file_paths)
```

---

## QRCodeVerifier

Classe para verificação de QR Codes em documentos.

### Inicialização

```python
QRCodeVerifier(
    min_qr_size: int = 10
) -> None
```

**Parâmetros:**
- `min_qr_size` (int): Tamanho mínimo do QR Code em pixels. Padrão: 10

**Exemplo:**

```python
from src.qr_verifier import QRCodeVerifier

verifier = QRCodeVerifier(min_qr_size=15)
```

### Métodos

#### `verify()`

Verifica se a imagem contém um QR Code válido.

```python
verify(
    image_path: str
) -> bool
```

**Parâmetros:**
- `image_path` (str): Caminho para o arquivo de imagem

**Retorna:**
- `bool`: True se um QR Code válido foi detectado, False caso contrário

**Exemplo:**

```python
has_qrcode = verifier.verify("documento.png")
print(f"Tem QR Code: {has_qrcode}")
```

#### `get_qr_data()`

Retorna os dados do primeiro QR Code encontrado.

```python
get_qr_data(
    image_path: str
) -> Optional[str]
```

**Parâmetros:**
- `image_path` (str): Caminho para o arquivo de imagem

**Retorna:**
- `Optional[str]`: Dados do QR Code ou None se nenhum for encontrado

**Exemplo:**

```python
qr_data = verifier.get_qr_data("documento.png")
if qr_data:
    print(f"Dados do QR Code: {qr_data}")
```

#### `get_qr_position()`

Retorna a posição do primeiro QR Code encontrado.

```python
get_qr_position(
    image_path: str
) -> Optional[Tuple[int, int, int, int]]
```

**Parâmetros:**
- `image_path` (str): Caminho para o arquivo de imagem

**Retorna:**
- `Optional[Tuple[int, int, int, int]]`: Tupla (x, y, width, height) ou None

**Exemplo:**

```python
position = verifier.get_qr_position("documento.png")
if position:
    x, y, width, height = position
    print(f"Posição: ({x}, {y}), Tamanho: {width}x{height}")
```

#### `count_qrcodes()`

Conta o número de QR Codes na imagem.

```python
count_qrcodes(
    image_path: str
) -> int
```

**Parâmetros:**
- `image_path` (str): Caminho para o arquivo de imagem

**Retorna:**
- `int`: Número de QR Codes encontrados

**Exemplo:**

```python
count = verifier.count_qrcodes("documento.png")
print(f"Número de QR Codes: {count}")
```

---

## FraudDetectionLogger

Classe para logging de detecção de fraudes.

### Inicialização

```python
FraudDetectionLogger(
    log_file: str = None,
    csv_file: str = None
) -> None
```

**Parâmetros:**
- `log_file` (str, opcional): Caminho para o arquivo de log
- `csv_file` (str, opcional): Caminho para o arquivo CSV de auditoria

**Exemplo:**

```python
from src.logger import FraudDetectionLogger

logger = FraudDetectionLogger(
    log_file="logs/app.log",
    csv_file="output/auditoria.csv"
)
```

### Métodos

#### `log_detection()`

Registra uma detecção de fraude.

```python
log_detection(
    result: Dict
) -> None
```

**Parâmetros:**
- `result` (Dict): Dicionário com o resultado da detecção

**Exemplo:**

```python
result = detector.detect("documento.pdf")
logger.log_detection(result)
```

#### `log_to_csv()`

Adiciona o resultado ao arquivo CSV de auditoria.

```python
log_to_csv(
    result: Dict
) -> None
```

**Parâmetros:**
- `result` (Dict): Dicionário com o resultado da detecção

**Exemplo:**

```python
logger.log_to_csv(result)
```

#### `log_batch()`

Registra múltiplas detecções em lote.

```python
log_batch(
    results: List[Dict]
) -> None
```

**Parâmetros:**
- `results` (List[Dict]): Lista de dicionários com os resultados

**Exemplo:**

```python
results = detector.batch_detect(file_paths)
logger.log_batch(results)
```

#### `get_statistics()`

Retorna estatísticas das detecções.

```python
get_statistics() -> Dict
```

**Retorna:**
- `Dict`: Dicionário com estatísticas:
  - `total_detections` (int): Total de detecções
  - `fraudulent` (int): Documentos fraudulentos
  - `authentic` (int): Documentos autênticos
  - `average_fraud_score` (float): Score médio de fraude

**Exemplo:**

```python
stats = logger.get_statistics()
print(f"Total: {stats['total_detections']}")
print(f"Fraudulentos: {stats['fraudulent']}")
```

#### `get_recent_detections()`

Retorna as N detecções mais recentes.

```python
get_recent_detections(
    n: int = 10
) -> pd.DataFrame
```

**Parâmetros:**
- `n` (int): Número de detecções a retornar. Padrão: 10

**Retorna:**
- `pd.DataFrame`: DataFrame com as detecções mais recentes

**Exemplo:**

```python
recent = logger.get_recent_detections(5)
print(recent)
```

#### `clear_logs()`

Limpa os arquivos de log.

```python
clear_logs() -> None
```

**Exemplo:**

```python
logger.clear_logs()
```

---

## Config

Classe de configuração do projeto.

### Métodos de Classe

#### `get_project_root()`

Retorna o diretório raiz do projeto.

```python
Config.get_project_root() -> Path
```

**Retorna:**
- `Path`: Caminho para o diretório raiz do projeto

**Exemplo:**

```python
from src.config import config

root = config.get_project_root()
print(root)
```

#### `get_model_path()`

Retorna o caminho para o diretório de modelos.

```python
Config.get_model_path() -> Path
```

**Retorna:**
- `Path`: Caminho para o diretório de modelos

#### `get_data_path()`

Retorna o caminho para o diretório de dados.

```python
Config.get_data_path() -> Path
```

**Retorna:**
- `Path`: Caminho para o diretório de dados

#### `get_output_path()`

Retorna o caminho para o diretório de saída.

```python
Config.get_output_path() -> Path
```

**Retorna:**
- `Path`: Caminho para o diretório de saída

#### `ensure_directories()`

Cria os diretórios necessários se não existirem.

```python
Config.ensure_directories() -> None
```

**Exemplo:**

```python
config.ensure_directories()
```

#### `validate()`

Valida a configuração.

```python
Config.validate() -> bool
```

**Retorna:**
- `bool`: True se a configuração é válida, False caso contrário

**Exemplo:**

```python
if config.validate():
    print("✅ Configuração válida")
else:
    print("❌ Configuração inválida")
```

---

**Versão**: 1.0.0 | **Última Atualização**: 2025
