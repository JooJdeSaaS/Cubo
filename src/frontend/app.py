# src/frontend/app.py
import streamlit as st
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from componentes import card_sensor, exibir_alerta_qualidade_ar
from assistente_ia import AssistenteCubo
from backend.leitor_serial import LeitorCubo

st.set_page_config(page_title="Cubo - Monitoramento Real", page_icon="🧊", layout="wide")

API_KEY = "AQ.Ab8RN6LpcxNv-XCgDRy8w_ZRbuJS5mtRp39Q683d68cT2Hku2A"
PORTA_SERIAL = '/dev/ttyUSB0'
BAUDRATE = 115200


@st.cache_resource
def iniciar_servicos_globais():
    assistente_ia = AssistenteCubo(api_key=API_KEY)
    leitor_hardware = LeitorCubo(porta=PORTA_SERIAL, baudrate=BAUDRATE)
    status_inicial = leitor_hardware.conectar()
    return assistente_ia, leitor_hardware, status_inicial


assistente, leitor, conectado = iniciar_servicos_globais()

st.title("O Cubo - Painel Ambiental & IA")
st.subheader("Monitoramento em tempo real com dados de Hardware (ESP32)")

if conectado:
    st.success(f"Conexão estabelecida com sucesso na porta {PORTA_SERIAL} a {BAUDRATE} bps.")
else:
    st.error(f"Falha ao abrir o barramento {PORTA_SERIAL}. Verifique a conexão USB física da ESP32.")

alerta_container = st.empty()

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1: card_temp = st.empty()
with col2: card_umid = st.empty()
with col3: card_co = st.empty()
with col4: card_pm25 = st.empty()
with col5: card_no2 = st.empty()
with col6: card_mq = st.empty()

st.sidebar.title("🤖 Assistente do Cubo")
pergunta_usuario = st.sidebar.text_input("Ex: Posso sair para uma caminhada?", key="pergunta_ia")
botao_perguntar = st.sidebar.button("Perguntar à IA")
resposta_container = st.sidebar.empty()

dados_ambientais = {
    "temperatura": 0.0,
    "umidade": 0,
    "co": 0,
    "no2": 0,
    "pm25": 0,
    "mq": 0
}

while True:
    if conectado:
        novos_dados = leitor.ler_dados()

        if novos_dados and isinstance(novos_dados, dict):
            dados_ambientais["temperatura"] = novos_dados.get("temperatura", dados_ambientais["temperatura"])
            dados_ambientais["umidade"] = novos_dados.get("umidade", dados_ambientais["umidade"])
            dados_ambientais["co"] = novos_dados.get("co", dados_ambientais["co"])
            dados_ambientais["no2"] = novos_dados.get("no2", dados_ambientais["no2"])
            dados_ambientais["pm25"] = novos_dados.get("pm2.5", dados_ambientais["pm25"])  # Sincronizado com a ESP32
            dados_ambientais["mq"] = novos_dados.get("mq", dados_ambientais["mq"])

    temp = dados_ambientais["temperatura"]
    umid = dados_ambientais["umidade"]
    co = dados_ambientais["co"]
    no2 = dados_ambientais["no2"]
    pm25 = dados_ambientais["pm25"]
    mq = dados_ambientais["mq"]

    card_temp.markdown(card_sensor("🌡️ Temperatura", temp, "°C", "#ffffff"), unsafe_allow_html=True)
    card_umid.markdown(card_sensor("💧 Umidade Relativa", umid, "%", "#00d2ff"), unsafe_allow_html=True)
    card_co.markdown(card_sensor("🚗 Monóxido de Carbono (CO)", co, "ppm", "#ffb703"), unsafe_allow_html=True)

    cor_borda_pm = "#ff4b4b" if pm25 > 50 else "#00cc66"
    card_pm25.markdown(card_sensor("🌫️ Partículas Finas (PM2.5)", pm25, "µg/m³", cor_borda_pm), unsafe_allow_html=True)

    card_no2.markdown(card_sensor("🧪 Dióxido de Nitrogênio (NO₂)", no2, "ppm", "#023e8a", "#90e0ef"),
                      unsafe_allow_html=True)
    card_mq.markdown(card_sensor("🍃 Sensor Geral (MQ-135)", mq, "idx", "#06d6a0"), unsafe_allow_html=True)

    alerta_html = exibir_alerta_qualidade_ar(pm25)
    alerta_container.markdown(alerta_html, unsafe_allow_html=True)

    if botao_perguntar and pergunta_usuario:
        resposta_container.info("A analisar as condições reais do Cubo...")
        resposta_ia = assistente.analisar_condicoes(
            pergunta=pergunta_usuario, temp=temp, umid=umid, pm25=pm25, co=co
        )
        resposta_container.markdown(f"**Resposta:**\n{resposta_ia}")
        botao_perguntar = False

    time.sleep(1.0)