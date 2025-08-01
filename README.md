# 🔹 Document Fraud Detection with Azure AI & Machine Learning

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Azure-Document%20Intelligence-blue.svg" alt="Azure Badge"/>
  <img src="https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green.svg" alt="ML Badge"/>
  <img src="https://img.shields.io/badge/Status-Advanced%20Prototype-success.svg" alt="Status Badge"/>
</p>

---

## 📌 Projeto

🚀 Este projeto implementa uma **solução completa de análise de documentos** para **detecção de fraudes**, combinando:

- **Azure AI Document Intelligence (Form Recognizer)** para extração de texto
- **Machine Learning (Random Forest)** para score de fraude
- **Verificação de autenticidade via QR Code**
- **Geração de logs CSV para auditoria e compliance**

## 🛠 Tecnologias Utilizadas
Python 3.9+

Google Colab (execução em nuvem)

Azure Cognitive Services

Document Intelligence (Form Recognizer)

OpenCV + Pyzbar (detecção de QR Codes)

Pandas (tratamento de dados e logs)

Scikit-learn (modelo de Machine Learning)



---

## ⚡ Pipeline da Solução

```mermaid
flowchart TD
    A[📄 Upload Documento] --> B[☁️ Azure Document Intelligence]
    B --> C[🔹 Extração de Texto e Features]
    C --> D[✅ Validação QR Code]
    D --> E[🤖 Modelo de Machine Learning]
    E --> F[📊 Score de Fraude + Log CSV]


