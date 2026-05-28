import pytest
import sys
import os

# Garante que o interpretador ache a pasta 'src' para o teste
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.backend.leitor_serial import LeitorCubo

def test_parse_texto_puro_sucesso():
    # --- Arrange (Preparação do cenário) ---
    # Uma string idêntica ao formato que a sua ESP32 envia no Serial.print
    linha_simulada_esp32 = "Temperatura: 25.50°C | Umidade: 60.00% | MQ: 340 | CO: 120 | NH3: 45 | NO2: 12 | PM1.0: 10 | PM2.5: 15 | PM10: 22 ug/m3"
    leitor = LeitorCubo(porta="PORTA_MOCK", baudrate=9600)

    # --- Act (Ação que queremos testar) ---
    resultado = leitor._parse_texto_puro(linha_simulada_esp32)

    # --- Assert (Verificação dos resultados) ---
    assert resultado is not None
    assert resultado["temperatura"] == 25.50
    assert resultado["umidade"] == 60.00
    assert resultado["mq"] == 340.00
    assert resultado["co"] == 120.00
    assert resultado["pm2.5"] == 15.00