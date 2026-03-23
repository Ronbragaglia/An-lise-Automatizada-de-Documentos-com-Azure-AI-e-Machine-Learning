"""Módulo de logging para auditoria e compliance."""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import pandas as pd

from .config import config


class FraudDetectionLogger:
    """Classe para logging de detecção de fraudes."""

    def __init__(
        self,
        log_file: str = None,
        csv_file: str = None
    ) -> None:
        """Inicializa o logger.

        Args:
            log_file: Caminho para o arquivo de log.
            csv_file: Caminho para o arquivo CSV de auditoria.
        """
        self.log_file = log_file or str(config.get_log_path())
        self.csv_file = csv_file or str(config.get_output_path() / "fraud_detection_log.csv")
        self._setup_logger()
        self._ensure_directories()

    def _setup_logger(self) -> None:
        """Configura o logger."""
        self.logger = logging.getLogger("FraudDetection")
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL))

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def _ensure_directories(self) -> None:
        """Cria os diretórios necessários."""
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        Path(self.csv_file).parent.mkdir(parents=True, exist_ok=True)

    def log_detection(self, result: Dict) -> None:
        """Registra uma detecção de fraude.

        Args:
            result: Dicionário com o resultado da detecção.
        """
        if "error" in result:
            self.logger.error(f"Erro em {result['file_path']}: {result['error']}")
        else:
            self.logger.info(
                f"Documento: {result['file_path']} | "
                f"Score: {result['fraud_score']:.2f} | "
                f"Classificação: {result['classification']}"
            )

    def log_to_csv(self, result: Dict) -> None:
        """Adiciona o resultado ao arquivo CSV de auditoria.

        Args:
            result: Dicionário com o resultado da detecção.
        """
        if "error" in result:
            return

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": result.get("file_path", ""),
            "text_length": result.get("text_length", 0),
            "has_qrcode": result.get("has_qrcode", False),
            "has_suspicious_words": result.get("has_suspicious_words", False),
            "fraud_score": result.get("fraud_score", 0.0),
            "classification": result.get("classification", ""),
            "threshold": result.get("threshold", 0.5)
        }

        # Criar DataFrame e salvar
        df = pd.DataFrame([log_entry])

        # Verificar se o arquivo já existe
        csv_path = Path(self.csv_file)
        if csv_path.exists():
            df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)

    def log_batch(self, results: List[Dict]) -> None:
        """Registra múltiplas detecções em lote.

        Args:
            results: Lista de dicionários com os resultados.
        """
        for result in results:
            self.log_detection(result)
            self.log_to_csv(result)

    def get_statistics(self) -> Dict:
        """Retorna estatísticas das detecções.

        Returns:
            Dicionário com estatísticas.
        """
        csv_path = Path(self.csv_file)
        if not csv_path.exists():
            return {
                "total_detections": 0,
                "fraudulent": 0,
                "authentic": 0,
                "average_fraud_score": 0.0
            }

        df = pd.read_csv(csv_path)

        return {
            "total_detections": len(df),
            "fraudulent": len(df[df["classification"] == "Suspeito de Fraude"]),
            "authentic": len(df[df["classification"] == "Autêntico"]),
            "average_fraud_score": df["fraud_score"].mean()
        }

    def get_recent_detections(self, n: int = 10) -> pd.DataFrame:
        """Retorna as N detecções mais recentes.

        Args:
            n: Número de detecções a retornar.

        Returns:
            DataFrame com as detecções mais recentes.
        """
        csv_path = Path(self.csv_file)
        if not csv_path.exists():
            return pd.DataFrame()

        df = pd.read_csv(csv_path)
        return df.tail(n)

    def clear_logs(self) -> None:
        """Limpa os arquivos de log."""
        log_path = Path(self.log_file)
        csv_path = Path(self.csv_file)

        if log_path.exists():
            log_path.unlink()

        if csv_path.exists():
            csv_path.unlink()

        self.logger.info("Logs limpos com sucesso")
