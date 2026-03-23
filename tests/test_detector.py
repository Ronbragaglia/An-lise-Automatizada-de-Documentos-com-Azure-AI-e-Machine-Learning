"""Testes para o módulo de detecção de fraudes."""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path

from src.detector import FraudDetector
from src.config import config


@pytest.mark.unit
class TestFraudDetector:
    """Testes para a classe FraudDetector."""

    def test_detector_initialization(self, temp_dir):
        """Testa a inicialização do detector."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        assert detector.model_path == str(model_path)
        assert detector.threshold == config.FRAUD_THRESHOLD
        assert detector.model is not None

    def test_create_model(self, temp_dir):
        """Testa a criação de um novo modelo."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        assert isinstance(detector.model, type(detector._create_model()))

    def test_train_model(self, temp_dir, sample_features, sample_labels):
        """Testa o treinamento do modelo."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        X_train = sample_features[["text_length", "has_qrcode", "has_suspicious_words"]].values
        y_train = sample_labels

        detector.train(X_train, y_train)

        # Verificar se o modelo foi salvo
        assert Path(model_path).exists()

    def test_predict_authentic(self, temp_dir):
        """Testa a predição de documento autêntico."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        # Treinar com dados de exemplo
        X_train = np.array([
            [500, 1, 0],
            [800, 1, 0],
            [1000, 1, 0]
        ])
        y_train = np.array([0, 0, 0])
        detector.train(X_train, y_train)

        # Predizer documento autêntico
        features = pd.DataFrame({
            "text_length": [600],
            "has_qrcode": [1],
            "has_suspicious_words": [0]
        })

        result = detector.predict(features)

        assert "fraud_score" in result
        assert "classification" in result
        assert 0 <= result["fraud_score"] <= 1

    def test_predict_fraudulent(self, temp_dir):
        """Testa a predição de documento fraudulento."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        # Treinar com dados de exemplo
        X_train = np.array([
            [300, 0, 1],
            [200, 0, 1],
            [150, 0, 1]
        ])
        y_train = np.array([1, 1, 1])
        detector.train(X_train, y_train)

        # Predizer documento fraudulento
        features = pd.DataFrame({
            "text_length": [250],
            "has_qrcode": [0],
            "has_suspicious_words": [1]
        })

        result = detector.predict(features)

        assert "fraud_score" in result
        assert "classification" in result
        assert 0 <= result["fraud_score"] <= 1

    def test_predict_missing_columns(self, temp_dir):
        """Testa predição com colunas faltando."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        # Features sem todas as colunas necessárias
        features = pd.DataFrame({
            "text_length": [500],
            "has_qrcode": [1]
        })

        with pytest.raises(ValueError, match="Colunas faltando"):
            detector.predict(features)

    def test_get_feature_importance(self, temp_dir, sample_features, sample_labels):
        """Testa a obtenção da importância das características."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        X_train = sample_features[["text_length", "has_qrcode", "has_suspicious_words"]].values
        y_train = sample_labels

        detector.train(X_train, y_train)

        importance = detector.get_feature_importance()

        assert isinstance(importance, dict)
        assert "text_length" in importance
        assert "has_qrcode" in importance
        assert "has_suspicious_words" in importance

        # Verificar se os valores são números
        for value in importance.values():
            assert isinstance(value, (int, float))
            assert 0 <= value <= 1

    def test_evaluate_model(self, temp_dir, sample_features, sample_labels):
        """Testa a avaliação do modelo."""
        model_path = temp_dir / "test_model.joblib"
        detector = FraudDetector(model_path=str(model_path))

        X_train = sample_features[["text_length", "has_qrcode", "has_suspicious_words"]].values
        y_train = sample_labels

        detector.train(X_train, y_train)

        # Avaliar com os mesmos dados (apenas para teste)
        metrics = detector.evaluate(X_train, y_train)

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1_score" in metrics
        assert "confusion_matrix" in metrics

        # Verificar se os valores estão no intervalo correto
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["precision"] <= 1
        assert 0 <= metrics["recall"] <= 1
        assert 0 <= metrics["f1_score"] <= 1

    def test_custom_threshold(self, temp_dir):
        """Testa detector com threshold personalizado."""
        model_path = temp_dir / "test_model.joblib"
        custom_threshold = 0.7
        detector = FraudDetector(model_path=str(model_path), threshold=custom_threshold)

        assert detector.threshold == custom_threshold
