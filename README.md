
# 🧊 O Cubo - Estação de Monitoramento Ambiental & IA

O **Cubo** é um ecossistema físico-digital integrado voltado para a monitoração em tempo real da qualidade do ar e de parâmetros ambientais. Utilizando um microcontrolador ESP32 conectado a múltiplos sensores analógicos e digitais, o sistema realiza a coleta local de dados, transmite-os via comunicação serial (UART) para uma aplicação reativa em Python (Streamlit) e utiliza inteligência artificial baseada em LLMs (Gemini) para fornecer análises preditivas e recomendações de saúde personalizadas com base nas diretrizes da Organização Mundial da Saúde (OMS).

---

## 🚀 Arquitetura do Sistema

O projeto é dividido em três camadas principais:
1. **Firmware (Cubo ESP32):** Ingestão assíncrona orientada a eventos para leitura física dos sensores sem bloqueio de fluxo do loop principal.
2. **Camada de Hardware (Python Backend):** Abstração POSIX para comunicação ponto a ponto através de barramento serial (`/dev/ttyUSB*` no Linux).
3. **Interface e Cognição (Frontend & IA):** Painel reativo construído em Streamlit injetado com prompts dinâmicos contextualizados com os parâmetros capturados em tempo real.

---

## 🛠️ Componentes e Sensores Utilizados

* **Microcontrolador:** ESP32 (NodeMCU / WROOM)
* **Temperatura e Umidade:** Sensor DHT11
* **Material Particulado (PM1.0, PM2.5, PM10):** Sensor Plantower PMS5003 (Via UART/Serial2)
* **Gases Voláteis e Poluentes:** * Sensor Geral MQ-135 (Qualidade Geral do Ar / Compostos Orgânicos Voláteis)
  * Monóxido de Carbono (CO)
  * Amônia ($NH_3$)
  * Dióxido de Nitrogênio ($NO_2$)

---

## 📂 Estrutura de Pastas do Repositório

```text
├── src/
│   ├── frontend/
│   │   ├── app.py            # Loop de vida e interface reativa do Streamlit
│   │   └── componentes.py    # Renderização HTML/CSS inline dos cards e alertas OMS
│   ├── backend/
│   │   └── leitor_serial.py  # Parser determinístico e tokenizador UART
│   └── assistente_ia.py      # Motor de inferência cognitiva (Google GenAI)
├── firmware/
│   └── cubo_esp32/
│       └── cubo_esp32.ino    # Código C++ embarcado para controle da ESP32
└── README.md                 # Documentação do projeto

```

---

## ⚙️ Instalação e Configuração

### 1. Requisitos Prévios (Linux / Ubuntu)

Certifique-se de que o seu ambiente de desenvolvimento possui o Python 3 instalado, além de garantir o acesso de leitura/escrita ao barramento de hardware USB:

```bash
# Adiciona o usuário atual ao grupo dialout para liberar acesso às portas seriais
sudo usermod -aG dialout $USER

# ATENÇÃO: Após rodar o comando acima, reinicie a sessão do seu sistema para aplicar as alterações.

```

### 2. Clonar o Repositório e Configurar o Ambiente

```bash
git clone [https://github.com/SEU_USUARIO/O-Cubo.git](https://github.com/SEU_USUARIO/O-Cubo.git)
cd O-Cubo

# Criar e ativar um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar as dependências oficiais do ecossistema
pip install streamlit pyserial google-genai

```

### 3. Configuração de Chaves e Portas

No arquivo `src/frontend/app.py`, insira suas credenciais de acesso locais e valide o diretório do barramento:

* **API_KEY:** Substitua com o seu token privado obtido no Google AI Studio.
* **PORTA_SERIAL:** O padrão para sistemas Linux Ubuntu utilizando chips CH340/CP2102 é `/dev/ttyUSB0`. Caso utilize outra variação, altere para `/dev/ttyACM0`.

---

## 💻 Como Executar o Projeto

1. **Upload do Firmware:** Compile e grave o arquivo `firmware/cubo_esp32/cubo_esp32.ino` na sua placa física ESP32 através da Arduino IDE.
2. **Liberar a Porta Serial:** **Feche o Monitor Serial da Arduino IDE** antes de prosseguir. A comunicação serial é exclusiva e causará um erro de dispositivo ocupado (`Device or resource busy`) se compartilhada.
3. **Iniciar a Aplicação Web:** Com o ambiente virtual ativado no seu terminal, execute o comando:

```bash
streamlit run src/frontend/app.py

```

---

## 🛡️ Protocolo de Parsing e Normalização de Dados

Para garantir a resiliência contra ruídos eletromagnéticos e pacotes truncados na UART, o backend implementa um mecanismo de tokenização secundária (Legacy Parse):

* **Formato de Transmissão Bruta:** `Temperatura: 25.00°C | Umidade: 60% | MQ: 350 | CO: 120 | NH3: 10 | NO2: 5 | PM1.0: 0 | PM2.5: 12 | PM10: 15 ug/m3`
* **Tratamento no Python:** O interpretador divide a string pelos delimitadores físicos pipe (`|`), padroniza os identificadores em caixa baixa, expurga as unidades físicas adjacentes (`°C`, `%`, `ug/m3`) e executa de forma limpa o casting para ponto flutuante (`float`), assegurando o preenchimento contínuo e estável da interface.

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e de pesquisa em Internet das Coisas (IoT) e Inteligência Artificial. Todos os direitos reservados.

```

```
