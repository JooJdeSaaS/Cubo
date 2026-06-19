import serial
import json
import time


class LeitorCubo:
    """
    Classe de abstração da camada de hardware responsável pela comunicação
    ponto a ponto (UART) via protocolo Serial entre a ESP32 e o Streamlit.
    """

    def __init__(self, porta='/dev/ttyUSB0', baudrate=115200):
        self.porta = porta
        self.baudrate = baudrate
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = serial.Serial(self.porta, self.baudrate, timeout=2)
            time.sleep(2)  # Justificativa Técnica: Tempo para o reboot de setup da ESP32
            return True
        except Exception as e:
            print(f"Erro ao conectar na porta {self.porta}: {e}")
            return False

    def ler_dados(self):
        if self.conexao and self.conexao.in_waiting > 0:
            try:
                linha = self.conexao.readline().decode('utf-8').strip()

                if linha.startswith("{") and linha.endswith("}"):
                    return json.loads(linha)
                else:
                    return self._parse_texto_puro(linha)
            except Exception:
                return None
        return None

    def _parse_texto_puro(self, linha):
        dados = {}
        try:
            # Separa o pacote bruto usando o caractere '|' enviado pela ESP32
            partes = linha.split('|')
            for parte in partes:
                if ':' in parte:
                    chave_valor = parte.strip().split(':')

                    # Chave normalizada em caixa baixa (ex: 'temperatura', 'umidade', 'pm2.5')
                    chave = chave_valor[0].strip().lower()

                    # Isolamento do valor numérico limpando strings de unidade adjacentes
                    valor_str = chave_valor[1].strip().lower()
                    valor_str = valor_str.replace("°c", "").replace("%", "").replace("ug/m3", "")

                    # Converte de forma limpa o valor numérico isolado
                    valor_limpo = valor_str.split()[0]
                    dados[chave] = float(valor_limpo)
            return dados
        except Exception:
            return None