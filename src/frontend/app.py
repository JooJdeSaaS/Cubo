import streamlit as st
import random
import time

from componentes import card_sensor, exibir_alerta_qualidade_ar
from assistente_ia import AssistenteCubo

# CONFIGURAÇÃO DE AMBIENTE
st.set_page_config(page_title="Cubo - Clima & IA", page_icon="🧊", layout="wide")

# --- CREDENCIAIS DE ACESSO (API KEY) ---
# Chave de autenticação criptográfica necessária para o protocolo de handshake com os servidores da Google AI Studio.
API_KEY = "AQ.Ab8RN6LpcxNv-XCgDRy8w_ZRbuJS5mtRp39Q683d68cT2Hku2A"


# JUSTIFICATIVA TÉCNICA (Otimização de Recursos): O decorador @st.cache_resource
# garante que a classe de conexão com a API seja instanciada uma única vez (Padrão Singleton).
# Isso evita o overhead de rede e novas alocações de memória a cada ciclo do loop principal.
@st.cache_resource
def configurar_ia():
    return AssistenteCubo(api_key=API_KEY)


# Instanciação estática do motor de processamento de linguagem natural
assistente = configurar_ia()

# ELEMENTOS TEXTUAIS ESTÁTICOS: Renderizados apenas uma vez para evitar consumo desnecessário de CPU
st.title("O Cubo - Painel Ambiental & IA")
st.subheader("Monitoramento em tempo real com assistente inteligente")

# CONTAINER DE ESTADO DINÂMICO: Instancia um espaço vazio (placeholder) mutável no topo.
# Permite a substituição assíncrona de alertas de saúde da OMS sem quebrar a estrutura da página.
alerta_container = st.empty()

# MACRO-ARQUITETURA DA INTERFACE (Layout de Grelha): Cria uma matriz bidimensional 2x3.
# Organiza a exibição espacial dos cards dos sensores de forma simétrica e responsiva.
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# ALOCAÇÃO DE MEMÓRIA VISUAL: Vincula blocos vazios reativos (.empty()) a cada coordenada da coluna.
# Garante que o Streamlit re-renderize exclusivamente o valor interno de cada card, sem recarregar a tela inteira.
with col1: card_temp = st.empty()
with col2: card_umid = st.empty()
with col3: card_co = st.empty()
with col4: card_pm25 = st.empty()
with col5: card_no2 = st.empty()
with col6: card_mq = st.empty()

# --- CONFIGURAÇÃO DA SIDEBAR (INTERAÇÃO DE CONTEXTO E PROMPT) ---
# Interface lateral dedicada à captura de inputs de texto sem causar interferência visual na matriz de sensores.
st.sidebar.title("🤖 Assistente do Cubo")
st.sidebar.write("Pergunte à IA se é seguro realizar atividades com base nos sensores atuais.")

# Captura de strings arbitrárias do usuário. A chave "pergunta_ia" vincula o input ao estado da sessão (Session State).
pergunta_usuario = st.sidebar.text_input("Ex: Posso sair para uma caminhada?", key="pergunta_ia")
botao_perguntar = st.sidebar.button("Perguntar à IA")
resposta_container = st.sidebar.empty()

# --- LOOP PRINCIPAL DO APP (Ciclo de Vida do Monitoramento) ---
while True:
    # --- SIMULAÇÃO ESTOCÁSTICA DOS SENSORES (MOCK DE HARDWARE) ---
    # Intervalos numéricos baseados estritamente nos limites operacionais físicos dos sensores REAIS:
    temp = round(random.uniform(15.0, 38.0), 2)
    umid = random.randint(40, 90)
    co = random.randint(100, 600)
    no2 = random.randint(5, 40)
    pm25 = random.randint(5, 120)
    mq = random.randint(200, 800)

    card_temp.markdown(card_sensor("🌡️ Temperatura", temp, "°C", "#ffffff"), unsafe_allow_html=True)
    card_umid.markdown(card_sensor("💧 Umidade Relativa", umid, "%", "#00d2ff"), unsafe_allow_html=True)
    card_co.markdown(card_sensor("🚗 Monóxido de Carbono (CO)", co, "ppm", "#ffb703"), unsafe_allow_html=True)

    cor_borda_pm = "#ff4b4b" if pm25 > 50 else "#00cc66"
    card_pm25.markdown(card_sensor("🌫️ Partículas Finas (PM2.5)", pm25, "µg/m³", cor_borda_pm), unsafe_allow_html=True)

    card_no2.markdown(card_sensor("🧪 Dióxido de Nitrogênio (NO₂)", no2, "ppm", "#023e8a", "#90e0ef"), unsafe_allow_html=True)
    card_mq.markdown(card_sensor("🍃 Sensor Geral (MQ-135)", mq, "idx", "#06d6a0"), unsafe_allow_html=True)

    alerta_html = exibir_alerta_qualidade_ar(pm25)
    alerta_container.markdown(alerta_html, unsafe_allow_html=True)

    if botao_perguntar and pergunta_usuario:
        if API_KEY == "SUA_CHAVE_API_AQUI":
            resposta_container.error("Por favor, configure uma API Key válida da Google no código.")
        else:
            resposta_container.info("A analisar as condições do Cubo...")

            resposta_ia = assistente.analisar_condicoes(
                pergunta=pergunta_usuario,
                temp=temp,
                umid=umid,
                pm25=pm25,
                co=co
            )

            resposta_container.markdown(f"**Resposta:**\n{resposta_ia}")

            botao_perguntar = False

    time.sleep(1.5)