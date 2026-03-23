"""Módulo para análise de documentos usando Azure AI Document Intelligence."""

from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from .config import config
from .qr_verifier import QRCodeVerifier


class DocumentAnalyzer:
    """Classe para análise de documentos usando Azure AI Document Intelligence."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        key: Optional[str] = None
    ) -> None:
        """Inicializa o analisador de documentos.

        Args:
            endpoint: Endpoint do Azure Form Recognizer.
            key: Chave de API do Azure Form Recognizer.
        """
        self.endpoint = endpoint or config.AZURE_FORM_RECOGNIZER_ENDPOINT
        self.key = key or config.AZURE_FORM_RECOGNIZER_KEY
        self.client = self._create_client()
        self.qr_verifier = QRCodeVerifier()

    def _create_client(self) -> DocumentAnalysisClient:
        """Cria o cliente do Azure Document Intelligence.

        Returns:
            Instância do DocumentAnalysisClient.
        """
        return DocumentAnalysisClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )

    def analyze(self, file_path: str) -> Dict:
        """Analisa um documento completo.

        Args:
            file_path: Caminho para o arquivo do documento.

        Returns:
            Dicionário contendo os resultados da análise.
        """
        # Extrair texto
        text = self.extract_text(file_path)

        # Verificar QR Code
        has_qrcode = self.qr_verifier.verify(file_path)

        # Extrair características
        features = self.extract_features(text, has_qrcode)

        return {
            "file_path": file_path,
            "text": text,
            "has_qrcode": has_qrcode,
            "features": features
        }

    def extract_text(self, file_path: str) -> str:
        """Extrai texto de um documento usando Azure AI.

        Args:
            file_path: Caminho para o arquivo do documento.

        Returns:
            Texto extraído do documento.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            ValueError: Se houver erro na análise do documento.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        try:
            with open(file_path, "rb") as fd:
                poller = self.client.begin_analyze_document(
                    "prebuilt-document",
                    document=fd
                )
                result = poller.result()

            # Extrair texto de todas as páginas
            text = " ".join([
                line.content
                for page in result.pages
                for line in page.lines
            ])

            return text

        except Exception as e:
            raise ValueError(f"Erro ao analisar documento: {e}")

    def extract_features(
        self,
        text: str,
        has_qrcode: bool
    ) -> Dict:
        """Extrai características do texto do documento.

        Args:
            text: Texto extraído do documento.
            has_qrcode: Indica se o documento tem QR Code.

        Returns:
            Dicionário com as características extraídas.
        """
        features = {
            "text_length": len(text),
            "has_qrcode": int(has_qrcode),
            "has_suspicious_words": 0,
            "word_count": len(text.split()),
            "line_count": text.count('\n') + 1,
        }

        # Verificar palavras suspeitas
        suspicious_count = sum(
            1 for word in config.SUSPICIOUS_WORDS
            if word.lower() in text.lower()
        )
        features["has_suspicious_words"] = int(suspicious_count > 0)
        features["suspicious_word_count"] = suspicious_count

        return features

    def extract_features_dataframe(
        self,
        text: str,
        has_qrcode: bool
    ) -> pd.DataFrame:
        """Extrai características e retorna como DataFrame.

        Args:
            text: Texto extraído do documento.
            has_qrcode: Indica se o documento tem QR Code.

        Returns:
            DataFrame com as características extraídas.
        """
        features = self.extract_features(text, has_qrcode)
        return pd.DataFrame([features])

    def get_document_info(self, file_path: str) -> Dict:
        """Obtém informações básicas do documento.

        Args:
            file_path: Caminho para o arquivo do documento.

        Returns:
            Dicionário com informações do documento.
        """
        path = Path(file_path)
        return {
            "file_name": path.name,
            "file_size": path.stat().st_size if path.exists() else 0,
            "file_extension": path.suffix,
            "is_supported": path.suffix.lower() in config.SUPPORTED_FORMATS
        }

    def batch_analyze(self, file_paths: List[str]) -> List[Dict]:
        """Analisa múltiplos documentos em lote.

        Args:
            file_paths: Lista de caminhos para os arquivos.

        Returns:
            Lista de dicionários com os resultados da análise.
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.analyze(file_path)
                results.append(result)
            except Exception as e:
                print(f"⚠️ Erro ao analisar {file_path}: {e}")
                results.append({
                    "file_path": file_path,
                    "error": str(e)
                })
        return results
