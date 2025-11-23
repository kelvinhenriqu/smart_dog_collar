#ifndef BATTERY_H
#define BATTERY_H

#include <Arduino.h>

// TTGO T1 não possui circuito de medição de bateria via ADC
// Implementa estimativa baseada em tempo de uso

unsigned long tempoInicio = 0;
// Bateria 900mAh com consumo de ~100mA = ~7 horas de autonomia
const unsigned long TEMPO_BATERIA_TOTAL = 7 * 60 * 60 * 1000; // 7 horas

void iniciarBateria() {
  tempoInicio = millis();
}

// Retorna porcentagem estimada da bateria
int lerBateria() {
  unsigned long tempoDecorrido = millis() - tempoInicio;
  
  // Calcula porcentagem: 100% no início, decai linearmente até 0%
  int percentage = 100 - ((tempoDecorrido * 100) / TEMPO_BATERIA_TOTAL);
  
  if (percentage < 0) percentage = 0;
  if (percentage > 100) percentage = 100;
  
  return percentage;
}

// Retorna voltagem estimada baseada na porcentagem
float lerVoltagem() {
  int percentage = lerBateria();
  // LiPo: 4.2V (100%) até 3.0V (0%)
  float voltage = 3.0 + (percentage / 100.0) * 1.2;
  return voltage;
}

// Debug: mostra tempo de uso
void debugBateria() {
  unsigned long segundos = (millis() - tempoInicio) / 1000;
  int horas = segundos / 3600;
  int minutos = (segundos % 3600) / 60;
  int segs = segundos % 60;
  
  Serial.print("Tempo de uso: ");
  Serial.print(horas);
  Serial.print("h ");
  Serial.print(minutos);
  Serial.print("m ");
  Serial.print(segs);
  Serial.print("s | Estimado: ");
  Serial.print(lerBateria());
  Serial.println("%");
}

#endif
