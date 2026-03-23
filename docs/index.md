# Documentação - Document Fraud Detection

Bem-vindo à documentação do sistema de detecção de fraudes em documentos usando Azure AI e Machine Learning.

## 📚 Índice

- [Introdução](#introdução)
- [Instalação](installation.md)
- [Guia de Uso](usage.md)
- [API Reference](api-reference.md)
- [Arquitetura](architecture.md)
- [Contribuindo](../CONTRIBUTING.md)
- [FAQ](faq.md)

## 🎯 Introdução

O **Document Fraud Detection** é uma solução completa para análise de documentos e detecção de fraudes, combinando:

- **Azure AI Document Intelligence** para extração de texto
- **Machine Learning (Random Forest)** para classificação de fraudes
- **Verificação de QR Codes** para autenticidade
- **Sistema de logging** para auditoria e compliance

### Características Principais

- ✅ Extração automática de texto de documentos
- ✅ Detecção de QR Codes para verificação de autenticidade
- ✅ Classificação de documentos como autênticos ou suspeitos
- ✅ Score de fraude (0-1) para análise de risco
- ✅ Logging detalhado em CSV para auditoria
- ✅ Suporte a múltiplos formatos de imagem
- ✅ Interface de linha de comando (CLI)
- ✅ API Python modular e extensível

### Casos de Uso

- **Bancos e Instituições Financeiras**: Validação de documentos de clientes
- **Seguros**: Verificação de apólices e comprovantes
- **RH**: Validação de documentos de candidatos
- **Compliance**: Auditoria e conformidade regulatória
- **Governo**: Validação de documentos oficiais

## 🚀 Começando Rápido

### 1. Clone o Repositório

```bash
git clone https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning.git
cd An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning
```

### 2. Configure o Ambiente

```bash
# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configure o Azure

Copie o arquivo de exemplo de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do Azure:

```env
AZURE_FORM_RECOGNIZER_ENDPOINT=https://seu-resource.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=sua-chave-aqui
```

### 4. Use a CLI

```bash
# Analisar um documento
python -m src.cli analyze documento.pdf

# Analisar todos os documentos de um diretório
python -m src.cli analyze-dir ./data

# Ver estatísticas
python -m src.cli stats
```

## 📖 Próximos Passos

- Leia o [Guia de Instalação](installation.md) para instruções detalhadas
- Consulte o [Guia de Uso](usage.md) para exemplos e tutoriais
- Explore a [API Reference](api-reference.md) para detalhes técnicos
- Entenda a [Arquitetura](architecture.md) do sistema

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o [Guia de Contribuição](../CONTRIBUTING.md) antes de começar.

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.

## 🔗 Links Úteis

- [Repositório GitHub](https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning)
- [Azure Document Intelligence](https://azure.microsoft.com/en-us/services/ai-services/form-recognizer/)
- [Scikit-learn](https://scikit-learn.org/)
- [OpenCV](https://opencv.org/)

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique a [FAQ](faq.md)
2. Abra uma [issue](https://github.com/Ronbragaglia/An-lise-Automatizada-de-Documentos-com-Azure-AI-e-Machine-Learning/issues)
3. Entre em contato com os mantenedores

---

**Versão**: 1.0.0 | **Última Atualização**: 2025
