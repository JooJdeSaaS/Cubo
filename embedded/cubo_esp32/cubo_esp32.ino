#include "DHT11.h"
#include <PMS.h>

// --- Definições de Pinos (ADC1 - Estáveis) ---
#define DHTPIN 4
#define MQ135PIN 34
#define CO_PIN 35
#define NH3_PIN 32
#define NO2_PIN 33

// Pinos para o PMS5003
#define PMS_RX 17
#define PMS_TX 16

DHT11 dht(DHTPIN);
PMS pms(Serial2);
PMS::DATA data;

void setup() {
  // Inicializa a Serial principal (USB) a 9600 bps para conversar com o PyCharm
  Serial.begin(9600);

  // Inicializa a Serial2 para o PMS5003 a 9600 bps
  Serial2.begin(9600, SERIAL_8N1, PMS_RX, PMS_TX);

  pinMode(MQ135PIN, INPUT);
  pinMode(CO_PIN, INPUT);
  pinMode(NH3_PIN, INPUT);
  pinMode(NO2_PIN, INPUT);
}

void loop() {
  // --- Leitura DHT11 ---
  int h = dht.readHumidity();
  float t = dht.readTemperature();

  // --- Leitura Analógica (Gases) ---
  int mq_val = analogRead(MQ135PIN);
  int co_val = analogRead(CO_PIN);
  int nh3_val = analogRead(NH3_PIN);
  int no2_val = analogRead(NO2_PIN);

  // --- Montagem e Envio da String JSON via Serial ---
  Serial.print("{");

  // Se o DHT falhar, envia 0 para não quebrar o formato numérico do JSON
  if (isnan(h) || isnan(t)) {
    Serial.print("\"temp\":0.0,\"umid\":0,");
  } else {
    Serial.print("\"temp\":"); Serial.print(t); Serial.print(",");
    Serial.print("\"umid\":"); Serial.print(h); Serial.print(",");
  }

  // Envia os dados dos sensores de gás
  Serial.print("\"mq135\":"); Serial.print(mq_val); Serial.print(",");
  Serial.print("\"co\":");    Serial.print(co_val);  Serial.print(",");
  Serial.print("\"nh3\":");   Serial.print(nh3_val); Serial.print(",");
  Serial.print("\"no2\":");   Serial.print(no2_val); Serial.print(",");

  // --- Leitura do PMS5003 (Particulados) ---
  if (pms.read(data)) {
    // Se o sensor responder, envia os valores reais
    Serial.print("\"pm10\":");  Serial.print(data.PM_AE_UG_1_0);  Serial.print(",");
    Serial.print("\"pm25\":");  Serial.print(data.PM_AE_UG_2_5);  Serial.print(",");
    Serial.print("\"pm100\":"); Serial.print(data.PM_AE_UG_10_0);
  } else {
    // Caso esteja aguardando estabilização, envia 0
    Serial.print("\"pm10\":0,\"pm25\":0,\"pm100\":0");
  }

  // Fecha o objeto JSON e pula uma linha (\n), indicando fim da mensagem
  Serial.println("}");

  // Mantém o delay de 2 segundos para estabilidade dos sensores
  delay(2000);
}