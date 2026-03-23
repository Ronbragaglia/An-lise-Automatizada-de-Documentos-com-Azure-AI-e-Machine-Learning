"""Módulo de configuração do projeto."""

import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class Config:
    """Classe de configuração do projeto."""

    # Azure Configuration
    AZURE_FORM_RECOGNIZER_ENDPOINT: str = os.getenv(
        "AZURE_FORM_RECOGNIZER_ENDPOINT",
        "https://your-resource.cognitiveservices.azure.com/"
    )
    AZURE_FORM_RECOGNIZER_KEY: str = os.getenv(
        "AZURE_FORM_RECOGNIZER_KEY", ""
    )

    # Application Configuration
    APP_NAME: str = os.getenv("APP_NAME", "Document Fraud Detection")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV: str = os.getenv("APP_ENV", "development")

    # Model Configuration
    MODEL_NAME: str = os.getenv("MODEL_NAME", "fraud_detection_model")
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "1.0.0")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

    # Data Configuration
    DATA_DIR: str = os.getenv("DATA_DIR", "data/")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output/")

    # Thresholds
    FRAUD_THRESHOLD: float = float(os.getenv("FRAUD_THRESHOLD", "0.5"))
    QR_CODE_REQUIRED: bool = os.getenv("QR_CODE_REQUIRED", "true").lower() == "true"

    # Suspicious words
    SUSPICIOUS_WORDS: List[str] = [
        "falso", "teste", "fake", "invalidado",
        "cancelado", "revogado", "nulo", "sem valor"
    ]

    # Supported image formats
    SUPPORTED_FORMATS: List[str] = [
        ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"
    ]

    @classmethod
    def get_project_root(cls) -> Path:
        """Retorna o diretório raiz do projeto.

        Returns:
            Path: Caminho para o diretório raiz do projeto.
        """
        return Path(__file__).parent.parent

    @classmethod
    def get_model_path(cls) -> Path:
        """Retorna o caminho para o diretório de modelos.

        Returns:
            Path: Caminho para o diretório de modelos.
        """
        return cls.get_project_root() / cls.MODEL_PATH

    @classmethod
    def get_data_path(cls) -> Path:
        """Retorna o caminho para o diretório de dados.

        Returns:
            Path: Caminho para o diretório de dados.
        """
        return cls.get_project_root() / cls.DATA_DIR

    @classmethod
    def get_output_path(cls) -> Path:
        """Retorna o caminho para o diretório de saída.

        Returns:
            Path: Caminho para o diretório de saída.
        """
        return cls.get_project_root() / cls.OUTPUT_DIR

    @classmethod
    def get_log_path(cls) -> Path:
        """Retorna o caminho para o arquivo de log.

        Returns:
            Path: Caminho para o arquivo de log.
        """
        return cls.get_project_root() / cls.LOG_FILE

    @classmethod
    def ensure_directories(cls) -> None:
        """Cria os diretórios necessários se não existirem."""
        directories = [
            cls.get_model_path(),
            cls.get_data_path(),
            cls.get_output_path(),
            cls.get_log_path().parent
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate(cls) -> bool:
        """Valida a configuração.

        Returns:
            bool: True se a configuração é válida, False caso contrário.
        """
        if not cls.AZURE_FORM_RECOGNIZER_KEY:
            print("⚠️ AVISO: AZURE_FORM_RECOGNIZER_KEY não configurado")
            return False
        return True


# Instância global de configuração
config = Config()
