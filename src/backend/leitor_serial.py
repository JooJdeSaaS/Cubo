import serial
import json
import time


class LeitorCubo:
    def __init__(self, porta='/dev/ttyUSB0', baudrate=9600):
        """
        No Ubuntu, a porta geralmente é '/dev/ttyUSB0' ou '/dev/ttyACM0'.
        No Windows, seria algo como 'COM3'.
        """
        self.porta = porta
        self.baudrate = baudrate
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = serial.Serial(self.porta, self.baudrate, timeout=2)
            time.sleep(2)  # Aguarda o reboot automático da ESP32 ao abrir a serial
            return True
        except Exception as e:
            print(f"Erro ao conectar na porta {self.porta}: {e}")
            return False

    def ler_dados(self):
        if self.conexao and self.conexao.in_waiting > 0:
            try:
                # Lê a linha da serial e decodifica
                linha = self.conexao.readline().decode('utf-8').strip()

                # Se você alterou a ESP32 para JSON:
                if linha.startswith("{") and list(linha)[-1] == "}":
                    return json.loads(linha)

                # Caso use o código antigo da ESP32 (Texto Puro), fazemos o parse manual:
                else:
                    return self._parse_texto_puro(linha)

            except Exception:
                return None
        return None

    def _parse_texto_puro(self, linha):
        """Traduz a string antiga com '|' e ':' para um dicionário Python"""
        dados = {}
        try:
            partes = linha.split('|')
            for parte in partes:
                if ':' in parte:
                    chave_valor = parte.strip().split(':')
                    chave = chave_valor[0].strip().lower().replace("°c", "").replace("%", "")
                    valor = float(chave_valor[1].strip().split()[0])  # Pega só o número, ignora 'ug/m3'
                    dados[chave] = valor
            return dados
        except Exception:
            return None