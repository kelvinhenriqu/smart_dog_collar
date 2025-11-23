#include "config.h"
#include "wifi_module.h"
#include "gps_module.h"
#include "battery.h"
#include "sensors.h"
#include "status.h"
#include "api.h"

unsigned long lastSendTime = 0;

void setup() {
  // Inicializa comunicação serial
  Serial.begin(115200);
  Serial.println("Iniciando sistema de rastreamento...");
  
  // Inicializa sistema de bateria (estimativa por tempo)
  iniciarBateria();
  
  // Conecta ao WiFi
  inicializarWiFi();
  
  // Inicializa GPS
  inicializarGPS();
  
  Serial.println("-------------------------------------------");
  Serial.println("Sistema iniciado!");
  Serial.println("Bateria: Estimativa por tempo de uso");
  Serial.println("-------------------------------------------");
}

void loop() {
  // Atualiza GPS
  atualizarGPS();
  
  // Envia dados periodicamente
  if (millis() - lastSendTime >= sendInterval) {
    // Reconecta WiFi se necessário
    reconectarWiFi();
    
    // Atualiza sensores
    atualizarSensores();
    
    // Lê bateria (estimada)
    int bateria = lerBateria();
    float voltagem = lerVoltagem();
    
    // Exibe status e bateria
    Serial.print("\nStatus: ");
    Serial.println(getStatus());
    Serial.print("Bateria: ");
    Serial.print(bateria);
    Serial.print("% (");
    Serial.print(voltagem, 2);
    Serial.println("V) - estimado");
    
    // Envia dados
    enviarDadosCompletos();
    //enviarLocalizacao();
    
    lastSendTime = millis();
  }
  
  // Verifica GPS
  if (!verificarGPS()) {
    while(true);
  }
}

