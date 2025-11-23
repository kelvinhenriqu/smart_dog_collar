#ifndef CONFIG_H
#define CONFIG_H

// Configuração WiFi
const char* ssid = "KELVIN-JTIP";
const char* password = "123321123";

// Endpoints
const char* endpoint = "https://dashboard.kelvinhenrique.dev/data/update"; //https://dashboard.kelvinhenrique.dev/data/update
const char* map_endpoint = "https://dashboard.kelvinhenrique.dev/map/update";

// Pinos do ESP32
#define GPS_RX 18  // RX do ESP32 conectado ao TX do GPS
#define GPS_TX 19  // TX do ESP32 conectado ao RX do GPS
// BATTERY_PIN removido - TTGO T1 não tem medição de bateria via ADC

// Configurações
const unsigned long sendInterval = 1000; // Envia a cada 1 segundo

#endif
