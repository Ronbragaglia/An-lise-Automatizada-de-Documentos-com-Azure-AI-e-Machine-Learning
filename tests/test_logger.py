"""Testes para o módulo de logging."""

import pytest
import pandas as pd
from pathlib import Path

from src.logger import FraudDetectionLogger


@pytest.mark.unit
class TestFraudDetectionLogger:
    """Testes para a classe FraudDetectionLogger."""

    def test_logger_initialization(self, temp_dir):
        """Testa a inicialização do logger."""
        log_file = temp_dir / "test.log"
        csv_file = temp_dir / "test.csv"

        logger = FraudDetectionLogger(
            log_file=str(log_file),
            csv_file=str(csv_file)
        )

        assert logger.log_file == str(log_file)
        assert logger.csv_file == str(csv_file)
        assert logger.logger is not None

    def test_log_detection_success(self, mock_logger):
        """Testa o logging de detecção bem-sucedida."""
        result = {
            "file_path": "test.pdf",
            "fraud_score": 0.25,
            "classification": "Autêntico"
        }

        # Não deve lançar exceção
        mock_logger.log_detection(result)

    def test_log_detection_error(self, mock_logger):
        """Testa o logging de detecção com erro."""
        result = {
            "file_path": "test.pdf",
            "error": "Arquivo não encontrado"
        }

        # Não deve lançar exceção
        mock_logger.log_detection(result)

    def test_log_to_csv(self, mock_logger):
        """Testa o logging para CSV."""
        result = {
            "file_path": "test.pdf",
            "text_length": 500,
            "has_qrcode": True,
            "has_suspicious_words": False,
            "fraud_score": 0.25,
            "classification": "Autêntico",
            "threshold": 0.5
        }

        mock_logger.log_to_csv(result)

        # Verificar se o arquivo foi criado
        csv_path = Path(mock_logger.csv_file)
        assert csv_path.exists()

        # Verificar o conteúdo
        df = pd.read_csv(csv_path)
        assert len(df) == 1
        assert df.iloc[0]["file_path"] == "test.pdf"
        assert df.iloc[0]["fraud_score"] == 0.25

    def test_log_batch(self, mock_logger):
        """Testa o logging em lote."""
        results = [
            {
                "file_path": "test1.pdf",
                "text_length": 500,
                "has_qrcode": True,
                "has_suspicious_words": False,
                "fraud_score": 0.25,
                "classification": "Autêntico",
                "threshold": 0.5
            },
            {
                "file_path": "test2.pdf",
                "text_length": 300,
                "has_qrcode": False,
                "has_suspicious_words": True,
                "fraud_score": 0.75,
                "classification": "Suspeito de Fraude",
                "threshold": 0.5
            }
        ]

        mock_logger.log_batch(results)

        # Verificar se o arquivo foi criado
        csv_path = Path(mock_logger.csv_file)
        assert csv_path.exists()

        # Verificar o conteúdo
        df = pd.read_csv(csv_path)
        assert len(df) == 2

    def test_get_statistics_empty(self, mock_logger):
        """Testa obter estatísticas quando não há dados."""
        stats = mock_logger.get_statistics()

        assert stats["total_detections"] == 0
        assert stats["fraudulent"] == 0
        assert stats["authentic"] == 0
        assert stats["average_fraud_score"] == 0.0

    def test_get_statistics_with_data(self, mock_logger):
        """Testa obter estatísticas com dados."""
        results = [
            {
                "file_path": "test1.pdf",
                "text_length": 500,
                "has_qrcode": True,
                "has_suspicious_words": False,
                "fraud_score": 0.25,
                "classification": "Autêntico",
                "threshold": 0.5
            },
            {
                "file_path": "test2.pdf",
                "text_length": 300,
                "has_qrcode": False,
                "has_suspicious_words": True,
                "fraud_score": 0.75,
                "classification": "Suspeito de Fraude",
                "threshold": 0.5
            }
        ]

        mock_logger.log_batch(results)
        stats = mock_logger.get_statistics()

        assert stats["total_detections"] == 2
        assert stats["fraudulent"] == 1
        assert stats["authentic"] == 1
        assert stats["average_fraud_score"] == 0.5

    def test_get_recent_detections_empty(self, mock_logger):
        """Testa obter detecções recentes quando não há dados."""
        recent = mock_logger.get_recent_detections(5)

        assert isinstance(recent, pd.DataFrame)
        assert len(recent) == 0

    def test_get_recent_detections_with_data(self, mock_logger):
        """Testa obter detecções recentes com dados."""
        results = [
            {
                "file_path": "test1.pdf",
                "text_length": 500,
                "has_qrcode": True,
                "has_suspicious_words": False,
                "fraud_score": 0.25,
                "classification": "Autêntico",
                "threshold": 0.5
            },
            {
                "file_path": "test2.pdf",
                "text_length": 300,
                "has_qrcode": False,
                "has_suspicious_words": True,
                "fraud_score": 0.75,
                "classification": "Suspeito de Fraude",
                "threshold": 0.5
            }
        ]

        mock_logger.log_batch(results)
        recent = mock_logger.get_recent_detections(5)

        assert isinstance(recent, pd.DataFrame)
        assert len(recent) == 2

    def test_clear_logs(self, mock_logger):
        """Testa limpar os logs."""
        result = {
            "file_path": "test.pdf",
            "text_length": 500,
            "has_qrcode": True,
            "has_suspicious_words": False,
            "fraud_score": 0.25,
            "classification": "Autêntico",
            "threshold": 0.5
        }

        mock_logger.log_to_csv(result)

        # Verificar que os arquivos existem
        log_path = Path(mock_logger.log_file)
        csv_path = Path(mock_logger.csv_file)

        assert log_path.exists()
        assert csv_path.exists()

        # Limpar logs
        mock_logger.clear_logs()

        # Verificar que os arquivos não existem mais
        assert not log_path.exists()
        assert not csv_path.exists()
