"""Document Fraud Detection with Azure AI and Machine Learning.

Este pacote fornece uma solução completa para análise de documentos
e detecção de fraudes usando Azure AI Document Intelligence e Machine Learning.
"""

__version__ = "1.0.0"
__author__ = "Rone Bragaglia"
__email__ = "ronbragaglia@gmail.com"

from .detector import FraudDetector
from .document_analyzer import DocumentAnalyzer
from .qr_verifier import QRCodeVerifier

__all__ = [
    "FraudDetector",
    "DocumentAnalyzer",
    "QRCodeVerifier",
]
