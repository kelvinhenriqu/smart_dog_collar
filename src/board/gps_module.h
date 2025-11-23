#ifndef GPS_MODULE_H
#define GPS_MODULE_H

#include <HardwareSerial.h>
#include <TinyGPSPlus.h>
#include "config.h"

// Configuração do GPS no Serial2
HardwareSerial gpsSerial(2);
TinyGPSPlus gps;

// Variáveis GPS
double latitude = 0.0;
double longitude = 0.0;
int satelites = 0;
double altitude = 0.0;
double velocidade = 0.0;

void inicializarGPS() {
  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  Serial.println("GPS configurado nos pinos 18 (RX) e 19 (TX)");
  Serial.println("Aguardando dados do GPS...");
}

void exibirDadosGPS() {
  Serial.println("========================================");
  Serial.print("Latitude: ");
  Serial.println(latitude, 6);
  
  Serial.print("Longitude: ");
  Serial.println(longitude, 6);
  
  Serial.print("Satelites conectados: ");
  Serial.println(satelites);
  
  Serial.print("Altitude: ");
  Serial.print(altitude);
  Serial.println(" m");
  
  Serial.print("Velocidade: ");
  Serial.print(velocidade);
  Serial.println(" km/h");
  
  Serial.print("Data: ");
  if (gps.date.isValid()) {
    Serial.print(gps.date.day());
    Serial.print("/");
    Serial.print(gps.date.month());
    Serial.print("/");
    Serial.println(gps.date.year());
  } else {
    Serial.println("Invalida");
  }
  
  Serial.print("Hora: ");
  if (gps.time.isValid()) {
    if (gps.time.hour() < 10) Serial.print("0");
    Serial.print(gps.time.hour());
    Serial.print(":");
    if (gps.time.minute() < 10) Serial.print("0");
    Serial.print(gps.time.minute());
    Serial.print(":");
    if (gps.time.second() < 10) Serial.print("0");
    Serial.println(gps.time.second());
  } else {
    Serial.println("Invalida");
  }
  
  Serial.println("========================================\n");
}

void atualizarGPS() {
  while (gpsSerial.available() > 0) {
    char c = gpsSerial.read();
    
    // Print valores brutos NMEA enquanto não tiver fix GPS
    if (!gps.location.isValid()) {
      Serial.print(c);
    }
    
    gps.encode(c);
  }
  
  // Atualiza variáveis quando houver nova informação
  if (gps.location.isUpdated()) {
    latitude = gps.location.lat();
    longitude = gps.location.lng();
    satelites = gps.satellites.value();
    altitude = gps.altitude.meters();
    velocidade = gps.speed.kmph();
    
    //exibirDadosGPS();
  }
}

bool verificarGPS() {
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println("Nenhum dado GPS detectado. Verifique as conexoes!");
    return false;
  }
  return true;
}

#endif
