#ifndef STATUS_H
#define STATUS_H

#include <WiFi.h>
#include "gps_module.h"

String getStatus() {
  if (WiFi.status() != WL_CONNECTED) {
    return "WiFi desconectado";
  }
  if (gps.charsProcessed() < 10) {
    return "Ligando GPS";
  }
  if (!gps.location.isValid()) {
    return "Encontrando satelites";
  }
  if (satelites < 4) {
    return "Poucos satelites";
  }
  return "Online e funcionando";
}

#endif
