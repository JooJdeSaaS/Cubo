import serial
import json
import time


class LeitorCubo:
    """
    Classe de abstração da camada de hardware responsável pela comunicação
    ponto a ponto (UART) via protocolo Serial entre o sistema embarcado (ESP32)
    e a aplicação de monitoramento em tempo real.
    """

    def __init__(self, porta='/dev/ttyUSB0', baudrate=9600):
        """
        Inicializa as especificações da interface de comunicação serial.

        Parâmetros:
            porta (str): Diretório do descritor de arquivo do barramento serial no ecossistema Linux POSIX.
            baudrate (int): Taxa de modulação/transmissão de dados (bits por segundo). Default: 9600 bps.
        """
        self.porta = porta
        self.baudrate = baudrate
        self.conexao = None

    def conectar(self):
        """
        Tenta estabelecer uma conexão persistente com a porta serial configurada.
        Inclui uma salvaguarda temporal para acomodar o ciclo de boot do hardware.
        """
        try:
            # Instancia o objeto serial com timeout para evitar o bloqueio por tempo indeterminado da thread principal
            self.conexao = serial.Serial(self.porta, self.baudrate, timeout=2)

            # JUSTIFICATIVA TÉCNICA (Hardware Reset): A abertura da comunicação UART via DTR/RTS
            # provoca um reset automático na ESP32. O delay de 2 segundos garante que o firmware
            # do microcontrolador finalize sua rotina de setup antes do envio dos primeiros bytes.
            time.sleep(2)
            return True
        except Exception as e:
            # Tratamento genérico de exceções de IO para capturar falhas de permissão ou porta inexistente
            print(f"Erro ao conectar na porta {self.porta}: {e}")
            return False

    def ler_dados(self):
        """
        Monitora o buffer de entrada e executa a leitura assíncrona orientada a eventos.
        Suporta de forma híbrida tanto pacotes estruturados em JSON quanto strings planas (texto puro).
        """
        # Verifica se o barramento está ativo e se há bytes pendentes no buffer de recepção (Rx)
        if self.conexao and self.conexao.in_waiting > 0:
            try:
                # Ingestão de linha física: lê o fluxo de bytes até o caractere delimitador '\n',
                # decodifica usando o padrão universal UTF-8 e remove espaços em branco periféricos.
                linha = self.conexao.readline().decode('utf-8').strip()

                # FLUXO A: Detecção e processamento de dados estruturados em formato nativo JSON
                if linha.startswith("{") and list(linha)[-1] == "}":
                    return json.loads(linha)

                # FLUXO B: Retrocompatibilidade e resiliência de software. Se o firmware da ESP32
                # enviar strings concatenadas por caracteres delimitadores, aciona o parser manual.
                else:
                    return self._parse_texto_puro(linha)

            except Exception:
                # Bloco try-catch protege o laço contínuo do sistema contra pacotes de dados
                # corrompidos ou falhas de ruído eletromagnético no barramento UART.
                return None
        return None

    def _parse_texto_puro(self, linha):
        """
        Processamento e normalização de strings desestruturadas (Legacy Parse).
        Aplica técnicas de Tokenização para segmentar variáveis textuais e convertê-las
        em tipos primitivos numéricos do Python de forma determinística.
        """
        dados = {}
        try:
            # Tokenização primária: separa as leituras dos sensores utilizando o delimitador pipe '|'
            partes = linha.split('|')
            for parte in partes:
                if ':' in parte:
                    # Tokenização secundária: isola a chave identificadora do valor correspondente
                    chave_valor = parte.strip().split(':')

                    # Normalização de strings: padroniza chaves em caixa baixa e remove unidades de
                    # medida físicas para evitar incompatibilidades na inserção do dicionário científico.
                    chave = chave_valor[0].strip().lower().replace("°c", "").replace("%", "")

                    # Extração do float: captura o valor numérico puro, isolando e descartando sufixos (ex: 'ug/m3')
                    valor = float(chave_valor[1].strip().split()[0])

                    dados[chave] = valor
            return dados
        except Exception:
            # Previne falhas catastróficas por ValueError ou IndexError caso a string de dados chegue truncada
            return None