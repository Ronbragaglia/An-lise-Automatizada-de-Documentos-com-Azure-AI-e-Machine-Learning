# Perguntas Frequentes (FAQ)

Perguntas e respostas comuns sobre o sistema de detecção de fraudes em documentos.

## 📋 Índice

- [Geral](#geral)
- [Instalação e Configuração](#instalação-e-configuração)
- [Uso](#uso)
- [Azure](#azure)
- [Machine Learning](#machine-learning)
- [Performance e Escalabilidade](#performance-e-escalabilidade)
- [Troubleshooting](#troubleshooting)

## 🎯 Geral

### O que é o Document Fraud Detection?

É um sistema completo para análise de documentos e detecção de fraudes que combina:
- Azure AI Document Intelligence para extração de texto
- Machine Learning (Random Forest) para classificação
- Verificação de QR Codes para autenticidade
- Sistema de logging para auditoria

### Quais formatos de documento são suportados?

O sistema suporta os seguintes formatos de imagem:
- JPG/JPEG
- PNG
- BMP
- TIFF
- Outros formatos compatíveis com OpenCV

**Nota**: Para PDF, o Azure Document Intelligence processa automaticamente.

### O sistema é gratuito?

O código é open-source e gratuito (licença MIT), mas você precisa de:
- Uma conta do Azure (com camada gratuita F0 disponível)
- Recurso de Azure Form Recognizer

### Posso usar o sistema comercialmente?

Sim! O sistema está licenciado sob a licença MIT, que permite uso comercial. No entanto, você deve cumprir os termos de serviço do Azure.

## 🔧 Instalação e Configuração

### Como instalo o sistema?

Siga o [Guia de Instalação](installation.md) completo. Resumidamente:

```bash
git clone https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning.git
cd An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Preciso do Azure?

Sim, o sistema usa Azure Document Intelligence para extração de texto. Você precisa:
1. Criar uma conta do Azure (gratuita)
2. Criar um recurso de Form Recognizer
3. Obter chave e endpoint

Veja o [Guia de Instalação](installation.md#configurar-o-azure) para detalhes.

### Posso usar sem Azure?

Não diretamente. O sistema foi projetado para usar Azure Document Intelligence. No entanto, você pode modificar o código para usar outros serviços de OCR.

### Como configuro o arquivo .env?

1. Copie o arquivo de exemplo:
   ```bash
   cp .env.example .env
   ```

2. Edite o arquivo `.env` com suas credenciais:
   ```env
   AZURE_FORM_RECOGNIZER_ENDPOINT=https://seu-resource.cognitiveservices.azure.com/
   AZURE_FORM_RECOGNIZER_KEY=sua-chave-aqui
   ```

### O Python 3.9 é obrigatório?

Sim, o sistema requer Python 3.9 ou superior. Recomendamos Python 3.11 para melhor performance.

## 🚀 Uso

### Como uso a CLI?

```bash
# Analisar um documento
python -m src.cli analyze documento.pdf

# Analisar diretório
python -m src.cli analyze-dir ./data

# Ver estatísticas
python -m src.cli stats
```

### Como uso como biblioteca Python?

```python
from src.detector import FraudDetector

detector = FraudDetector()
result = detector.detect("documento.pdf")

print(f"Classificação: {result['classification']}")
print(f"Score: {result['fraud_score']:.2f}")
```

Veja o [Guia de Uso](usage.md) para mais exemplos.

### O que significa o score de fraude?

O score de fraude é um valor entre 0 e 1:
- **0.0 - 0.5**: Documento provavelmente autêntico
- **0.5 - 1.0**: Documento provavelmente fraudulento

O threshold padrão é 0.5, mas pode ser ajustado.

### Como ajusto o threshold de fraude?

```python
# Criar detector com threshold personalizado
detector = FraudDetector(threshold=0.7)
```

- Threshold mais alto (ex: 0.7) = Menos falsos positivos
- Threshold mais baixo (ex: 0.3) = Menos falsos negativos

### Posso treinar meu próprio modelo?

Sim! Veja o [Guia de Uso](usage.md#treinamento-personalizado) para detalhes.

```python
import numpy as np
from src.detector import FraudDetector

X_train = np.array([[500, 1, 0], [300, 0, 1]])
y_train = np.array([0, 1])

detector = FraudDetector()
detector.train(X_train, y_train)
```

## ☁️ Azure

### Quanto custa o Azure Form Recognizer?

A cam gratuita F0 inclui:
- 2 páginas gratuitas por mês
- Após isso: $1.50 por 1.000 páginas

Veja [Preços do Azure Form Recognizer](https://azure.microsoft.com/en-us/pricing/details/form-recognizer/) para detalhes.

### Posso usar outro serviço de OCR?

Sim, mas você precisa modificar o código. O `DocumentAnalyzer` usa Azure SDK, mas você pode substituir por outro serviço de OCR.

### Como crio um recurso do Azure?

1. Acesse o [Portal do Azure](https://portal.azure.com/)
2. Clique em "Criar um recurso"
3. Pesquise por "Form Recognizer"
4. Preencha os campos e crie

Veja o [Guia de Instalação](installation.md) para instruções detalhadas.

### O que fazer se a chave do Azure expirar?

1. Gere uma nova chave no Portal do Azure
2. Atualize o arquivo `.env` com a nova chave
3. Reinicie a aplicação

## 🤖 Machine Learning

### Que algoritmo é usado?

O sistema usa **Random Forest Classifier** do Scikit-learn. Este algoritmo foi escolhido porque:
- Robusto a overfitting
- Lida bem com dados não lineares
- Fornece importância de características
- Rápido para inferência

### Como funciona o modelo?

O modelo é treinado com características:
- **text_length**: Tamanho do texto extraído
- **has_qrcode**: Presença de QR Code (0 ou 1)
- **has_suspicious_words**: Palavras suspeitas detectadas (0 ou 1)

O modelo aprende padrões que indicam fraude.

### Posso melhorar o modelo?

Sim! Você pode:
1. Coletar mais dados de treinamento
2. Adicionar mais características
3. Ajustar hiperparâmetros do modelo
4. Experimentar outros algoritmos

### Como avalio o modelo?

```python
from src.detector import FraudDetector

detector = FraudDetector()
metrics = detector.evaluate(X_test, y_test)

print(f"Acurácia: {metrics['accuracy']:.2f}")
print(f"F1-Score: {metrics['f1_score']:.2f}")
```

### O que são palavras suspeitas?

São palavras que frequentemente aparecem em documentos fraudulentos:
- "falso"
- "teste"
- "fake"
- "invalidado"
- "cancelado"
- "revogado"
- "nulo"
- "sem valor"

Você pode personalizar esta lista no [`src/config.py`](../src/config.py).

## ⚡ Performance e Escalabilidade

### Quantos documentos posso processar por hora?

Depende de vários fatores:
- Tamanho dos documentos
- Latência do Azure
- Hardware disponível

Em média: 100-500 documentos/hora em uma máquina padrão.

### Como melhoro a performance?

1. **Use batch processing**:
   ```python
   results = detector.batch_detect(file_paths)
   ```

2. **Processamento paralelo**:
   ```python
   from concurrent.futures import ThreadPoolExecutor

   with ThreadPoolExecutor(max_workers=4) as executor:
       results = list(executor.map(detector.detect, file_paths))
   ```

3. **Cache de modelos**: O modelo já é cacheado automaticamente

### Posso usar GPU?

O Random Forest não usa GPU por padrão. Para usar GPU, considere:
- Usar XGBoost ou LightGBM
- Implementar com PyTorch/TensorFlow

### Como escalo horizontalmente?

O sistema é stateless, então você pode:
- Executar múltiplas instâncias
- Usar load balancing
- Compartilhar storage para modelos e logs

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'src'"

**Solução**: Instale o pacote em modo de desenvolvimento:
```bash
pip install -e .
```

### Erro: "Azure authentication failed"

**Solução**: Verifique suas credenciais no `.env`:
```env
AZURE_FORM_RECOGNIZER_ENDPOINT=https://seu-resource.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=sua-chave-aqui
```

### Erro: "OpenCV error"

**Solução**: Instale dependências do sistema:

**Ubuntu/Debian**:
```bash
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

**macOS**:
```bash
brew install opencv
```

### O modelo está classificando tudo como fraude

**Causa possível**: Threshold muito baixo ou dados de treinamento desbalanceados.

**Solução**:
1. Ajuste o threshold:
   ```python
   detector = FraudDetector(threshold=0.7)
   ```

2. Retreine com dados balanceados

### O modelo está classificando tudo como autêntico

**Causa possível**: Threshold muito alto ou dados de treinamento insuficientes.

**Solução**:
1. Ajuste o threshold:
   ```python
   detector = FraudDetector(threshold=0.3)
   ```

2. Adicione mais exemplos de fraude ao treinamento

### Como vejo os logs?

Os logs são salvos em:
- **Log de eventos**: `logs/app.log`
- **CSV de auditoria**: `output/fraud_detection_log.csv`

Você também pode usar a CLI:
```bash
python -m src.cli stats
```

### Como limpo os logs?

```bash
python -m src.cli clear-logs
```

Ou manualmente:
```bash
rm logs/app.log
rm output/fraud_detection_log.csv
```

### O documento não está sendo detectado

**Possíveis causas**:
1. Formato não suportado
2. Arquivo corrompido
3. Problemas com Azure

**Solução**:
1. Verifique o formato do arquivo
2. Teste com um documento diferente
3. Verifique os logs para erros

## 📞 Ainda precisa de ajuda?

1. Verifique a [Documentação](index.md)
2. Leia o [Guia de Uso](usage.md)
3. Consulte a [API Reference](api-reference.md)
4. Abra uma [issue no GitHub](https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning/issues)

---

**Versão**: 1.0.0 | **Última Atualização**: 2025
