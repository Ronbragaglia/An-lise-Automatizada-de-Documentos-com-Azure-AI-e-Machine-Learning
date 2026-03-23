"""Módulo para detecção de fraudes em documentos."""

from pathlib import Path
from typing import Dict, Optional
import pandas as pd
import joblib
import numpy as np

from sklearn.ensemble import RandomForestClassifier

from .config import config
from .document_analyzer import DocumentAnalyzer


class FraudDetector:
    """Classe para detecção de fraudes em documentos."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        threshold: Optional[float] = None
    ) -> None:
        """Inicializa o detector de fraudes.

        Args:
            model_path: Caminho para o modelo treinado.
            threshold: Limiar para classificação de fraude.
        """
        self.model_path = model_path or str(config.get_model_path() / "fraud_model.joblib")
        self.threshold = threshold or config.FRAUD_THRESHOLD
        self.model = self._load_or_create_model()
        self.analyzer = DocumentAnalyzer()

    def _load_or_create_model(self) -> RandomForestClassifier:
        """Carrega o modelo ou cria um novo se não existir.

        Returns:
            Instância do RandomForestClassifier.
        """
        model_file = Path(self.model_path)
        if model_file.exists():
            try:
                return joblib.load(model_file)
            except Exception as e:
                print(f"⚠️ Erro ao carregar modelo: {e}")
                return self._create_model()
        return self._create_model()

    def _create_model(self) -> RandomForestClassifier:
        """Cria um novo modelo de detecção de fraudes.

        Returns:
            Instância do RandomForestClassifier.
        """
        return RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5
        )

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> None:
        """Treina o modelo de detecção de fraudes.

        Args:
            X_train: Array de características de treinamento.
            y_train: Array de labels de treinamento (0=autêntico, 1=fraude).
        """
        self.model.fit(X_train, y_train)
        self._save_model()

    def _save_model(self) -> None:
        """Salva o modelo treinado."""
        model_file = Path(self.model_path)
        model_file.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, model_file)

    def predict(self, features: pd.DataFrame) -> Dict:
        """Prediz se um documento é fraudulento.

        Args:
            features: DataFrame com as características do documento.

        Returns:
            Dicionário com os resultados da predição.
        """
        # Preparar características
        feature_columns = [
            "text_length",
            "has_qrcode",
            "has_suspicious_words"
        ]

        # Verificar se todas as colunas necessárias existem
        missing_cols = [col for col in feature_columns if col not in features.columns]
        if missing_cols:
            raise ValueError(f"Colunas faltando: {missing_cols}")

        X = features[feature_columns].values

        # Obter probabilidade de fraude
        fraud_probability = self.model.predict_proba(X)[0][1]

        # Classificar
        classification = "Suspeito de Fraude" if fraud_probability > self.threshold else "Autêntico"

        return {
            "fraud_score": float(fraud_probability),
            "classification": classification,
            "threshold": self.threshold
        }

    def detect(self, file_path: str) -> Dict:
        """Detecta fraude em um documento.

        Args:
            file_path: Caminho para o arquivo do documento.

        Returns:
            Dicionário com os resultados da detecção.
        """
        # Analisar documento
        analysis = self.analyzer.analyze(file_path)

        # Extrair características como DataFrame
        features_df = self.analyzer.extract_features_dataframe(
            analysis["text"],
            analysis["has_qrcode"]
        )

        # Predizer fraude
        prediction = self.predict(features_df)

        # Combinar resultados
        return {
            "file_path": file_path,
            "text_length": analysis["features"]["text_length"],
            "has_qrcode": analysis["has_qrcode"],
            "has_suspicious_words": analysis["features"]["has_suspicious_words"],
            "fraud_score": prediction["fraud_score"],
            "classification": prediction["classification"],
            "threshold": prediction["threshold"]
        }

    def batch_detect(self, file_paths: list[str]) -> list[Dict]:
        """Detecta fraude em múltiplos documentos.

        Args:
            file_paths: Lista de caminhos para os arquivos.

        Returns:
            Lista de dicionários com os resultados da detecção.
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.detect(file_path)
                results.append(result)
            except Exception as e:
                print(f"⚠️ Erro ao detectar fraude em {file_path}: {e}")
                results.append({
                    "file_path": file_path,
                    "error": str(e)
                })
        return results

    def get_feature_importance(self) -> Dict[str, float]:
        """Retorna a importância das características do modelo.

        Returns:
            Dicionário com a importância de cada característica.
        """
        feature_names = [
            "text_length",
            "has_qrcode",
            "has_suspicious_words"
        ]

        importances = self.model.feature_importances_

        return dict(zip(feature_names, importances))

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Avalia o modelo com dados de teste.

        Args:
            X_test: Array de características de teste.
            y_test: Array de labels de teste.

        Returns:
            Dicionário com métricas de avaliação.
        """
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            confusion_matrix
        )

        y_pred = self.model.predict(X_test)

        return {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average='weighted', zero_division=0),
            "recall": recall_score(y_test, y_pred, average='weighted', zero_division=0),
            "f1_score": f1_score(y_test, y_pred, average='weighted', zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
        }
