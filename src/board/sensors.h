#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

// Variáveis de sensores (simuladas por enquanto)
int heart_rate = 120;
float pet_body_temperature = 37.5;

// Simula leitura de batimentos cardíacos
int lerBatimentosCardiacos() {
  // TODO: Implementar leitura real do sensor de batimentos
  return random(80, 181);
}

// Simula leitura de temperatura corporal
float lerTemperaturaCorporal() {
  // TODO: Implementar leitura real do sensor de temperatura
  return random(300, 391) / 10.0;
}

void atualizarSensores() {
  heart_rate = lerBatimentosCardiacos();
  pet_body_temperature = lerTemperaturaCorporal();
}

#endif
