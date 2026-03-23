"""Exemplo avançado de uso do sistema de detecção de fraudes."""

from pathlib import Path
import numpy as np
import pandas as pd

from src.detector import FraudDetector
from src.document_analyzer import DocumentAnalyzer
from src.qr_verifier import QRCodeVerifier
from src.logger import FraudDetectionLogger
from src.config import config


def main():
    """Função principal do exemplo avançado."""
    print("=" * 60)
    print("🚀 Exemplo Avançado de Detecção de Fraudes")
    print("=" * 60)

    # Configurar diretórios
    config.ensure_directories()

    # Exemplo 1: Treinar um modelo personalizado
    print("\n🤖 Exemplo 1: Treinar Modelo Personalizado")
    print("-" * 60)

    # Dados de treinamento de exemplo
    X_train = np.array([
        [500, 1, 0],   # Autêntico
        [300, 0, 1],   # Fraude
        [800, 1, 0],   # Autêntico
        [200, 0, 1],   # Fraude
        [1000, 1, 0],  # Autêntico
        [150, 0, 1],   # Fraude
        [600, 1, 0],   # Autêntico
        [250, 0, 1],   # Fraude
        [700, 1, 0],   # Autêntico
        [180, 0, 1],   # Fraude
    ])
    y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

    # Criar detector e treinar
    detector = FraudDetector()
    detector.train(X_train, y_train)

    print(f"✅ Modelo treinado com {len(X_train)} exemplos")
    print(f"📁 Modelo salvo em: {detector.model_path}")

    # Exemplo 2: Avaliar o modelo
    print("\n📊 Exemplo 2: Avaliar Modelo")
    print("-" * 60)

    X_test = np.array([
        [550, 1, 0],   # Deve ser autêntico
        [220, 0, 1],   # Deve ser fraude
    ])
    y_test = np.array([0, 1])

    metrics = detector.evaluate(X_test, y_test)

    print(f"Acurácia: {metrics['accuracy']:.2f}")
    print(f"Precisão: {metrics['precision']:.2f}")
    print(f"Recall: {metrics['recall']:.2f}")
    print(f"F1-Score: {metrics['f1_score']:.2f}")

    # Exemplo 3: Usar o analisador de documentos
    print("\n📄 Exemplo 3: Analisar Documento")
    print("-" * 60)

    analyzer = DocumentAnalyzer()

    file_path = "data/documento_exemplo.png"

    try:
        analysis = analyzer.analyze(file_path)

        print(f"📁 Arquivo: {analysis['file_path']}")
        print(f"📝 Texto extraído: {analysis['text'][:100]}...")
        print(f"🔲 Tem QR Code: {analysis['has_qrcode']}")
        print(f"📊 Características: {analysis['features']}")

    except FileNotFoundError:
        print(f"⚠️ Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

    # Exemplo 4: Verificar QR Code
    print("\n🔲 Exemplo 4: Verificar QR Code")
    print("-" * 60)

    qr_verifier = QRCodeVerifier()

    try:
        has_qrcode = qr_verifier.verify(file_path)
        print(f"📁 Arquivo: {file_path}")
        print(f"🔲 Tem QR Code: {'Sim' if has_qrcode else 'Não'}")

        if has_qrcode:
            qr_data = qr_verifier.get_qr_data(file_path)
            qr_position = qr_verifier.get_qr_position(file_path)

            print(f"📱 Dados do QR Code: {qr_data}")
            print(f"📍 Posição: {qr_position}")

    except FileNotFoundError:
        print(f"⚠️ Arquivo não encontrado: {file_path}")
    except Exception as e:
        print(f"❌ Erro: {e}")

    # Exemplo 5: Análise em lote de diretório
    print("\n📁 Exemplo 5: Análise em Lote de Diretório")
    print("-" * 60)

    data_dir = Path("data")
    if data_dir.exists():
        file_paths = [
            str(f) for f in data_dir.glob("*")
            if f.is_file() and f.suffix.lower() in config.SUPPORTED_FORMATS
        ]

        if file_paths:
            print(f"📂 Encontrados {len(file_paths)} arquivos em {data_dir}")

            results = detector.batch_detect(file_paths)

            for i, result in enumerate(results, 1):
                if "error" in result:
                    print(f"{i}. ❌ {result['file_path']}: {result['error']}")
                else:
                    emoji = "🔴" if result["classification"] == "Suspeito de Fraude" else "✅"
                    print(f"{i}. {emoji} {result['file_path']}: {result['classification']} (Score: {result['fraud_score']:.2f})")
        else:
            print("⚠️ Nenhum arquivo suportado encontrado")
    else:
        print(f"⚠️ Diretório não encontrado: {data_dir}")

    # Exemplo 6: Logging e auditoria
    print("\n📋 Exemplo 6: Logging e Auditoria")
    print("-" * 60)

    logger = FraudDetectionLogger()

    # Criar resultados de exemplo
    sample_results = [
        {
            "file_path": "doc1.pdf",
            "text_length": 500,
            "has_qrcode": True,
            "has_suspicious_words": False,
            "fraud_score": 0.25,
            "classification": "Autêntico",
            "threshold": 0.5
        },
        {
            "file_path": "doc2.pdf",
            "text_length": 300,
            "has_qrcode": False,
            "has_suspicious_words": True,
            "fraud_score": 0.75,
            "classification": "Suspeito de Fraude",
            "threshold": 0.5
        }
    ]

    logger.log_batch(sample_results)

    # Mostrar estatísticas
    stats = logger.get_statistics()
    print(f"Total de Detecções: {stats['total_detections']}")
    print(f"Documentos Autênticos: {stats['authentic']}")
    print(f"Documentos Suspeitos: {stats['fraudulent']}")

    # Mostrar detecções recentes
    recent = logger.get_recent_detections(5)
    print(f"\n📋 Últimas {len(recent)} Detecções:")
    print(recent.to_string(index=False))

    # Exemplo 7: Threshold personalizado
    print("\n🎯 Exemplo 7: Threshold Personalizado")
    print("-" * 60)

    custom_threshold = 0.7
    detector_custom = FraudDetector(threshold=custom_threshold)

    features = pd.DataFrame({
        "text_length": [400],
        "has_qrcode": [1],
        "has_suspicious_words": [0]
    })

    result = detector_custom.predict(features)

    print(f"Threshold Personalizado: {custom_threshold}")
    print(f"Score de Fraude: {result['fraud_score']:.2f}")
    print(f"Classificação: {result['classification']}")

    # Exemplo 8: Importância das características
    print("\n🔍 Exemplo 8: Importância das Características")
    print("-" * 60)

    importance = detector.get_feature_importance()

    print("Características mais importantes:")
    sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    for feature, value in sorted_importance:
        print(f"  {feature}: {value:.4f}")

    print("\n" + "=" * 60)
    print("✅ Exemplo avançado concluído!")
    print("=" * 60)


if __name__ == "__main__":
    main()
