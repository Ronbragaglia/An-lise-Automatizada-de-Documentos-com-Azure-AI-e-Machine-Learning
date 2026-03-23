"""Configuração e fixtures para os testes."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def sample_features():
    """Fixture para fornecer características de exemplo."""
    return pd.DataFrame({
        "text_length": [500, 300, 800, 200, 1000],
        "has_qrcode": [1, 0, 1, 0, 1],
        "has_suspicious_words": [0, 1, 0, 1, 0]
    })


@pytest.fixture
def sample_labels():
    """Fixture para fornecer labels de exemplo."""
    return np.array([0, 1, 0, 1, 0])


@pytest.fixture
def sample_text():
    """Fixture para fornecer texto de exemplo."""
    return "Este é um documento de teste com informações importantes."


@pytest.fixture
def temp_dir():
    """Fixture para criar um diretório temporário."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Limpeza após o teste
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def sample_image(temp_dir):
    """Fixture para criar uma imagem de teste."""
    import cv2
    import numpy as np

    image_path = temp_dir / "test_image.png"
    # Criar uma imagem simples
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    cv2.imwrite(str(image_path), img)
    return str(image_path)


@pytest.fixture
def mock_azure_client(mocker):
    """Fixture para mockar o cliente do Azure."""
    mock_client = mocker.patch("src.document_analyzer.DocumentAnalysisClient")
    return mock_client


@pytest.fixture
def mock_logger(temp_dir):
    """Fixture para criar um logger temporário."""
    from src.logger import FraudDetectionLogger

    log_file = temp_dir / "test.log"
    csv_file = temp_dir / "test.csv"

    return FraudDetectionLogger(
        log_file=str(log_file),
        csv_file=str(csv_file)
    )
