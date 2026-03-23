"""Módulo para verificação de QR Codes em documentos."""

import cv2
from pathlib import Path
from typing import Optional, Tuple
from pyzbar.pyzbar import decode, Decoded


class QRCodeVerifier:
    """Classe para verificação de QR Codes em documentos."""

    def __init__(self, min_qr_size: int = 10) -> None:
        """Inicializa o verificador de QR Codes.

        Args:
            min_qr_size: Tamanho mínimo do QR Code em pixels.
        """
        self.min_qr_size = min_qr_size

    def verify(self, image_path: str) -> bool:
        """Verifica se a imagem contém um QR Code válido.

        Args:
            image_path: Caminho para o arquivo de imagem.

        Returns:
            bool: True se um QR Code válido foi detectado, False caso contrário.
        """
        try:
            qrcodes = self._detect_qrcodes(image_path)
            return len(qrcodes) > 0
        except Exception as e:
            print(f"⚠️ Erro ao verificar QR Code: {e}")
            return False

    def detect(self, image_path: str) -> list[Decoded]:
        """Detecta QR Codes na imagem.

        Args:
            image_path: Caminho para o arquivo de imagem.

        Returns:
            Lista de QR Codes detectados.
        """
        return self._detect_qrcodes(image_path)

    def _detect_qrcodes(self, image_path: str) -> list[Decoded]:
        """Detecta QR Codes na imagem (método interno).

        Args:
            image_path: Caminho para o arquivo de imagem.

        Returns:
            Lista de QR Codes detectados.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            ValueError: Se o arquivo não puder ser lido.
        """
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")

        img = cv2.imread(str(path))
        if img is None:
            raise ValueError(f"Não foi possível ler a imagem: {image_path}")

        qrcodes = decode(img)
        return qrcodes

    def get_qr_data(self, image_path: str) -> Optional[str]:
        """Retorna os dados do primeiro QR Code encontrado.

        Args:
            image_path: Caminho para o arquivo de imagem.

        Returns:
            Dados do QR Code ou None se nenhum for encontrado.
        """
        try:
            qrcodes = self._detect_qrcodes(image_path)
            if qrcodes:
                return qrcodes[0].data.decode("utf-8")
            return None
        except Exception as e:
            print(f"⚠️ Erro ao obter dados do QR Code: {e}")
            return None

    def get_qr_position(self, image_path: str) -> Optional[Tuple[int, int, int, int]]:
        """Retorna a posição do primeiro QR Code encontrado.

        Args:
            image_path: Caminho para o arquivo de imagem.

        Returns:
            Tupla (x, y, width, height) ou None se nenhum QR Code for encontrado.
        """
        try:
            qrcodes = self._detect_qrcodes(image_path)
            if qrcodes:
                rect = qrcodes[0].rect
                return (rect.left, rect.top, rect.width, rect.height)
            return None
        except Exception as e:
            print(f"⚠️ Erro ao obter posição do QR Code: {e}")
            return None

    def count_qrcodes(self, image_path: str) -> int:
        """Conta o número de QR Codes na imagem.

        Args:
            image_path: Caminho para o arquivo de imagem.

        Returns:
            Número de QR Codes encontrados.
        """
        try:
            qrcodes = self._detect_qrcodes(image_path)
            return len(qrcodes)
        except Exception as e:
            print(f"⚠️ Erro ao contar QR Codes: {e}")
            return 0

    def is_valid_size(self, image_path: str) -> bool:
        """Verifica se o QR Code tem o tamanho mínimo.

        Args:
            image_path: Caminho para o arquivo de imagem.

        Returns:
            bool: True se o QR Code tem o tamanho mínimo, False caso contrário.
        """
        try:
            position = self.get_qr_position(image_path)
            if position:
                _, _, width, height = position
                return width >= self.min_qr_size and height >= self.min_qr_size
            return False
        except Exception as e:
            print(f"⚠️ Erro ao verificar tamanho do QR Code: {e}")
            return False
