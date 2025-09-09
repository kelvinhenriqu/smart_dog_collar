import requests
import time
import random

ENDPOINT = "http://localhost:8050/data/update"  # Altere para o endereço correto do seu servidor

# Valores base para simulação
BASE_LAT = -23.1865
BASE_LON = -46.8845

while True:
    payload = {
        "lat": BASE_LAT + random.uniform(-0.0001, 0.0001),
        "lon": BASE_LON + random.uniform(-0.0001, 0.0001),
        "battery_level": random.randint(20, 100),
        "heart_rate": random.randint(80, 180),
        "pet_body_temperature": round(random.uniform(30.0, 39.0), 1)
    }
    try:
        response = requests.post(ENDPOINT, json=payload)
        print(f"Enviado: {payload} | Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")
    time.sleep(0.5)  # Atualiza a cada 0.5 segundo
