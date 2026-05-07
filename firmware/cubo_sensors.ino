#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT11.h"
#include <PMS.h>

// --- Configurações de Rede ---
const char* ssid = "CAMPUS_MACK";
const char* password = "Mackenzie";
const char* serverUrl = "http://168.197.92.40:5000/update"; // Troque pelo IP do seu PC

// --- Definições de Pinos (ADC1 - Estáveis) ---
#define DHTPIN 4
#define MQ135PIN 34
#define CO_PIN 35
#define NH3_PIN 32
#define NO2_PIN 33
#define PMS_RX 17
#define PMS_TX 16

DHT11 dht(DHTPIN);
PMS pms(Serial2); [cite: 2]
PMS::DATA data;

void setup() {
  Serial.begin(115200);

  // Conexão WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Conectado!");

  // Inicializa Sensores
  Serial2.begin(9600, SERIAL_8N1, PMS_RX, PMS_TX);
  pinMode(MQ135PIN, INPUT); [cite: 3]
  pinMode(CO_PIN, INPUT); [cite: 3]
  pinMode(NH3_PIN, INPUT); [cite: 3]
  pinMode(NO2_PIN, INPUT); [cite: 3]

  Serial.println("Sistema 'Cubo' Online - Enviando para API...");
}

void loop() {
  // 1. Leitura dos Sensores
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int mq_val = analogRead(MQ135PIN); [cite: 5]
  int co_val = analogRead(CO_PIN); [cite: 5]
  int nh3_val = analogRead(NH3_PIN); [cite: 5]
  int no2_val = analogRead(NO2_PIN); [cite: 6]

  int pm25 = 0;
  if (pms.read(data)) { [cite: 9]
    pm25 = data.PM_AE_UG_2_5; [cite: 10]
  }

  // 2. Envio para o Backend (Flask)
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Monta o JSON completo com todos os dados do Cubo
    String jsonPayload = "{";
    jsonPayload += "\"temp\":" + String(t) + ",";
    jsonPayload += "\"hum\":" + String(h) + ",";
    jsonPayload += "\"mq135\":" + String(mq_val) + ",";
    jsonPayload += "\"co\":" + String(co_val) + ",";
    jsonPayload += "\"nh3\":" + String(nh3_val) + ",";
    jsonPayload += "\"no2\":" + String(no2_val) + ",";
    jsonPayload += "\"pm25\":" + String(pm25);
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);

    // Debug no Monitor Serial
    Serial.print("HTTP Code: "); Serial.println(httpResponseCode);
    Serial.println("Payload: " + jsonPayload);

    http.end();
  } else {
    Serial.println("WiFi Desconectado");
  }

  delay(5000); // Envia dados a cada 5 segundos
}