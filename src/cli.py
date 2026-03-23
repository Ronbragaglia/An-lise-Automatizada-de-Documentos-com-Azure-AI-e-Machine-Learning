"""Interface de linha de comando para detecção de fraudes em documentos."""

import argparse
import sys
from pathlib import Path
from typing import List

from .config import config
from .detector import FraudDetector
from .logger import FraudDetectionLogger


def parse_args() -> argparse.Namespace:
    """Parse os argumentos da linha de comando.

    Returns:
        Namespace com os argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description="Sistema de Detecção de Fraudes em Documentos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Analisar um documento
  python -m src.cli analyze documento.pdf

  # Analisar múltiplos documentos
  python -m src.cli analyze doc1.pdf doc2.pdf doc3.pdf

  # Analisar todos os documentos de um diretório
  python -m src.cli analyze-dir ./data/documents

  # Treinar um novo modelo
  python -m src.cli train

  # Ver estatísticas
  python -m src.cli stats

  # Limpar logs
  python -m src.cli clear-logs
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analisar documento(s)")
    analyze_parser.add_argument(
        "files",
        nargs="+",
        help="Caminho(s) para o(s) arquivo(s) de documento"
    )

    # Comando analyze-dir
    analyze_dir_parser = subparsers.add_parser(
        "analyze-dir",
        help="Analisar todos os documentos de um diretório"
    )
    analyze_dir_parser.add_argument(
        "directory",
        help="Caminho para o diretório"
    )

    # Comando train
    train_parser = subparsers.add_parser("train", help="Treinar modelo")
    train_parser.add_argument(
        "--data",
        default=None,
        help="Caminho para o arquivo de dados de treinamento"
    )

    # Comando stats
    subparsers.add_parser("stats", help="Mostrar estatísticas")

    # Comando clear-logs
    subparsers.add_parser("clear-logs", help="Limpar logs")

    return parser.parse_args()


def analyze_documents(file_paths: List[str]) -> None:
    """Analisa documentos para detecção de fraudes.

    Args:
        file_paths: Lista de caminhos para os arquivos.
    """
    print(f"🚀 Iniciando análise de {len(file_paths)} documento(s)...")
    print("=" * 60)

    # Validar configuração
    if not config.validate():
        print("❌ Configuração inválida. Verifique o arquivo .env")
        sys.exit(1)

    # Criar diretórios necessários
    config.ensure_directories()

    # Inicializar detector e logger
    detector = FraudDetector()
    logger = FraudDetectionLogger()

    # Analisar documentos
    results = detector.batch_detect(file_paths)

    # Exibir resultados
    print("\n📊 Resultados da Análise:")
    print("=" * 60)

    for i, result in enumerate(results, 1):
        if "error" in result:
            print(f"\n{i}. ❌ {result['file_path']}")
            print(f"   Erro: {result['error']}")
        else:
            emoji = "🔴" if result["classification"] == "Suspeito de Fraude" else "✅"
            print(f"\n{i}. {emoji} {result['file_path']}")
            print(f"   Score de Fraude: {result['fraud_score']:.2f}")
            print(f"   Classificação: {result['classification']}")
            print(f"   Tem QR Code: {'Sim' if result['has_qrcode'] else 'Não'}")
            print(f"   Palavras Suspeitas: {'Sim' if result['has_suspicious_words'] else 'Não'}")

    # Logar resultados
    logger.log_batch(results)

    # Estatísticas
    print("\n" + "=" * 60)
    stats = logger.get_statistics()
    print(f"📈 Estatísticas:")
    print(f"   Total: {stats['total_detections']}")
    print(f"   Autênticos: {stats['authentic']}")
    print(f"   Suspeitos: {stats['fraudulent']}")
    print(f"   Score Médio: {stats['average_fraud_score']:.2f}")
    print("=" * 60)


def analyze_directory(directory: str) -> None:
    """Analisa todos os documentos de um diretório.

    Args:
        directory: Caminho para o diretório.
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"❌ Diretório não encontrado: {directory}")
        sys.exit(1)

    # Encontrar todos os arquivos suportados
    file_paths = [
        str(f) for f in dir_path.rglob("*")
        if f.is_file() and f.suffix.lower() in config.SUPPORTED_FORMATS
    ]

    if not file_paths:
        print(f"⚠️ Nenhum arquivo suportado encontrado em: {directory}")
        sys.exit(0)

    print(f"📁 Encontrados {len(file_paths)} arquivo(s) em {directory}")
    analyze_documents(file_paths)


def train_model(data_file: str = None) -> None:
    """Treina o modelo de detecção de fraudes.

    Args:
        data_file: Caminho para o arquivo de dados de treinamento.
    """
    print("🤖 Treinando modelo de detecção de fraudes...")

    # Se não houver arquivo de dados, usar dados de exemplo
    if data_file is None:
        print("⚠️ Nenhum arquivo de dados fornecido. Usando dados de exemplo.")
        import numpy as np

        X_train = np.array([
            [500, 1, 0],   # Autêntico
            [300, 0, 1],   # Fraude
            [800, 1, 0],   # Autêntico
            [200, 0, 1],   # Fraude
            [1000, 1, 0],  # Autêntico
            [150, 0, 1],   # Fraude
            [600, 1, 0],   # Autêntico
            [250, 0, 1],   # Fraude
        ])
        y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    else:
        # Carregar dados do arquivo (implementação futura)
        print(f"📂 Carregando dados de: {data_file}")
        # TODO: Implementar carregamento de dados
        print("❌ Carregamento de arquivo ainda não implementado")
        sys.exit(1)

    # Treinar modelo
    detector = FraudDetector()
    detector.train(X_train, y_train)

    print("✅ Modelo treinado com sucesso!")
    print(f"📁 Modelo salvo em: {detector.model_path}")


def show_statistics() -> None:
    """Mostra estatísticas das detecções."""
    logger = FraudDetectionLogger()
    stats = logger.get_statistics()

    print("📊 Estatísticas de Detecção de Fraudes")
    print("=" * 60)
    print(f"Total de Detecções: {stats['total_detections']}")
    print(f"Documentos Autênticos: {stats['authentic']}")
    print(f"Documentos Suspeitos: {stats['fraudulent']}")
    print(f"Score Médio de Fraude: {stats['average_fraud_score']:.2f}")
    print("=" * 60)

    # Mostrar detecções recentes
    print("\n📋 Últimas Detecções:")
    print("=" * 60)
    recent = logger.get_recent_detections(5)
    if not recent.empty:
        print(recent.to_string(index=False))
    else:
        print("Nenhuma detecção registrada ainda.")
    print("=" * 60)


def clear_logs() -> None:
    """Limpa os arquivos de log."""
    logger = FraudDetectionLogger()
    logger.clear_logs()
    print("✅ Logs limpos com sucesso!")


def main() -> None:
    """Função principal da CLI."""
    args = parse_args()

    if args.command == "analyze":
        analyze_documents(args.files)
    elif args.command == "analyze-dir":
        analyze_directory(args.directory)
    elif args.command == "train":
        train_model(args.data)
    elif args.command == "stats":
        show_statistics()
    elif args.command == "clear-logs":
        clear_logs()
    else:
        print("❌ Comando não reconhecido. Use --help para ver os comandos disponíveis.")
        sys.exit(1)


if __name__ == "__main__":
    main()
