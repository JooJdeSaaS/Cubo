#include "DHT11.h"

// --- Definições de Pinos ---
#define DHTPIN 4
#define MQ135PIN 34
#define CO_PIN 35
#define NH3_PIN 32
#define NO2_PIN 33

// Pinos da Serial2 para o PMS5003 (Corrigidos para a placa física)
#define PMS_RX 16
#define PMS_TX 17

DHT11 dht(DHTPIN);

// Buffer e variáveis para leitura manual do PMS5003
uint8_t pmsBuffer[32];
uint16_t pm1 = 0;
uint16_t pm25 = 0;
uint16_t pm10 = 0;

void setup() {
  // Inicializa a Serial nativa a 115200 bps para o Monitor Serial
  Serial.begin(115200);

  // Inicializa a Serial2 para comunicação com o PMS5003 (9600 baud padrão do sensor)
  Serial2.begin(9600, SERIAL_8N1, PMS_RX, PMS_TX);

  // Configuração dos pinos dos sensores analógicos como entrada
  pinMode(MQ135PIN, INPUT);
  pinMode(CO_PIN, INPUT);
  pinMode(NH3_PIN, INPUT);
  pinMode(NO2_PIN, INPUT);

  Serial.println("Sistema 'Climatempo da Qualidade do Ar' Iniciado...");
}

void loop() {
  // --- Leitura do DHT11 ---
  int h = dht.readHumidity();
  float t = dht.readTemperature();

  // --- Leitura dos Sensores Analógicos ---
  int mq_val = analogRead(MQ135PIN);
  int co_val = analogRead(CO_PIN);
  int nh3_val = analogRead(NH3_PIN);
  int no2_val = analogRead(NO2_PIN);

  // --- Leitura Robusta do PMS5003 (Sem travar/atrasar o fluxo) ---
  if (Serial2.available() >= 32) {
    // peek() espia o primeiro byte sem tirá-lo da fila.
    // O pacote correto do PMS sempre começa com o byte de cabeçalho 0x42
    if (Serial2.peek() == 0x42) {

      // Lê os 32 bytes de uma vez para o buffer
      Serial2.readBytes(pmsBuffer, 32);

      // Valida se o segundo byte de cabeçalho é o esperado (0x4D)
      if (pmsBuffer[1] == 0x4D) {
        // Monta os valores de 16 bits combinando o High Byte e Low Byte
        pm1  = (pmsBuffer[10] << 8) | pmsBuffer[11];
        pm25 = (pmsBuffer[12] << 8) | pmsBuffer[13];
        pm10 = (pmsBuffer[14] << 8) | pmsBuffer[15];
      }
    } else {
      // Se o primeiro byte não for 0x42, descarta apenas ele para alinhar o fluxo de dados
      Serial2.read();
    }
  }

  // --- Exibição dos Dados formatados no Monitor Serial ---
  if (isnan(h) || isnan(t)) {
    Serial.print("Erro DHT11 | ");
  } else {
    Serial.print("Temperatura: ");
    Serial.print(t);
    Serial.print("°C | Umidade: ");
    Serial.print(h);
    Serial.print("% | ");
  }

  // Sensores de Gás (Formatado via printf)
  Serial.printf(
    "MQ: %d | CO: %d | NH3: %d | NO2: %d",
    mq_val,
    co_val,
    nh3_val,
    no2_val
  );

  // Material Particulado (PMS5003)
  Serial.printf(
    " | PM1.0: %d | PM2.5: %d | PM10: %d ug/m3",
    pm1,
    pm25,
    pm10
  );

  Serial.println();

  // Mantém o delay de 2 segundos exigido para a estabilização do DHT11
  delay(2000);
}