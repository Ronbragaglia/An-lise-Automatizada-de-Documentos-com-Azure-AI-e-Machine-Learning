"""Exemplo básico de uso do sistema de detecção de fraudes."""

from src.detector import FraudDetector
from src.logger import FraudDetectionLogger
from src.config import config


def main():
    """Função principal do exemplo básico."""
    print("=" * 60)
    print("🚀 Exemplo Básico de Detecção de Fraudes")
    print("=" * 60)

    # Configurar diretórios
    config.ensure_directories()

    # Inicializar detector e logger
    detector = FraudDetector()
    logger = FraudDetectionLogger()

    # Exemplo 1: Detectar fraude em um documento
    print("\n📄 Exemplo 1: Detectar fraude em um documento")
    print("-" * 60)

    file_path = "data/documento_exemplo.png"

    try:
        result = detector.detect(file_path)

        print(f"📁 Arquivo: {result['file_path']}")
        print(f"📏 Tamanho do Texto: {result['text_length']} caracteres")
        print(f"🔲 Tem QR Code: {'Sim' if result['has_qrcode'] else 'Não'}")
        print(f"⚠️ Palavras Suspeitas: {'Sim' if result['has_suspicious_words'] else 'Não'}")
        print(f"📊 Score de Fraude: {result['fraud_score']:.2f}")
        print(f"🎯 Classificação: {result['classification']}")

        # Logar resultado
        logger.log_detection(result)
        logger.log_to_csv(result)

    except FileNotFoundError:
        print(f"⚠️ Arquivo não encontrado: {file_path}")
        print("💡 Coloque um documento na pasta data/ para testar")
    except Exception as e:
        print(f"❌ Erro: {e}")

    # Exemplo 2: Detectar fraude em múltiplos documentos
    print("\n📁 Exemplo 2: Detectar fraude em múltiplos documentos")
    print("-" * 60)

    file_paths = [
        "data/documento1.png",
        "data/documento2.png",
        "data/documento3.png"
    ]

    results = detector.batch_detect(file_paths)

    for i, result in enumerate(results, 1):
        if "error" in result:
            print(f"{i}. ❌ {result['file_path']}: {result['error']}")
        else:
            emoji = "🔴" if result["classification"] == "Suspeito de Fraude" else "✅"
            print(f"{i}. {emoji} {result['file_path']}: {result['classification']} (Score: {result['fraud_score']:.2f})")

    # Logar resultados em lote
    logger.log_batch(results)

    # Exemplo 3: Ver estatísticas
    print("\n📊 Exemplo 3: Estatísticas de Detecção")
    print("-" * 60)

    stats = logger.get_statistics()
    print(f"Total de Detecções: {stats['total_detections']}")
    print(f"Documentos Autênticos: {stats['authentic']}")
    print(f"Documentos Suspeitos: {stats['fraudulent']}")
    print(f"Score Médio de Fraude: {stats['average_fraud_score']:.2f}")

    # Exemplo 4: Obter importância das características
    print("\n🔍 Exemplo 4: Importância das Características")
    print("-" * 60)

    importance = detector.get_feature_importance()
    for feature, value in importance.items():
        print(f"{feature}: {value:.4f}")

    print("\n" + "=" * 60)
    print("✅ Exemplo concluído!")
    print("=" * 60)


if __name__ == "__main__":
    main()
