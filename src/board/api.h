#ifndef API_H
#define API_H

#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include "config.h"
#include "gps_module.h"
#include "battery.h"
#include "sensors.h"
#include "status.h"

void enviarDadosCompletos() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    http.begin(endpoint);
    http.addHeader("Content-Type", "application/json");
    
    // Cria JSON com todos os dados
    StaticJsonDocument<300> doc;
    doc["lat"] = latitude;
    doc["lon"] = longitude;
    doc["battery_level"] = lerBateria();
    doc["heart_rate"] = heart_rate;
    doc["pet_body_temperature"] = pet_body_temperature;
    doc["velocidade"] = velocidade;
    doc["satelites"] = satelites;
    doc["status"] = getStatus();
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    Serial.println("\n[DATA] Enviando dados completos:");
    Serial.println(jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      Serial.print("Resposta HTTP: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Erro no envio: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("WiFi desconectado!");
  }
}

void enviarLocalizacao() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    http.begin(map_endpoint);
    http.addHeader("Content-Type", "application/json");
    
    // Cria JSON apenas com localização
    StaticJsonDocument<128> doc;
    doc["lat"] = latitude;
    doc["lon"] = longitude;
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    Serial.println("\n[MAP] Enviando localizacao:");
    Serial.println(jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if (httpResponseCode > 0) {
      Serial.print("Resposta HTTP Map: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Erro no envio Map: ");
      Serial.println(httpResponseCode);
    }
    
    http.end();
  }
}

#endif
