import os
import time
import json
import random
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from shared.shared_processing import process_audio_energy

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "smart_traffic_kelompok_07")
MQTT_HOST = os.getenv("MQTT_HOST", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = f"iot/{PROJECT_ID}/edge1/noise"

CLASSES = ["Quiet", "Klakson", "Sirene", "Traffic_Noise"]

def run_edge1():
    client = mqtt.Client(client_id="HP_Android_Edge1")
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    print(f"[EDGE 1 - HP] Running... Sending to topic: {TOPIC}")

    try:
        while True:
            # Simulasi sampling audio PCM dari mikrofon HP
            raw_pcm = [random.randint(-128, 127) for _ in range(256)]
            energy = process_audio_energy(raw_pcm)

            # Inferensi AI Klasifikasi Suara
            detected_class = random.choice(CLASSES)
            confidence = round(random.uniform(0.80, 0.99), 2)

            payload = {
                "device_id": "Edge1_Android_Mic",
                "sound_class": detected_class,
                "confidence": confidence,
                "audio_energy": energy,
                "timestamp": time.time()
            }

            client.publish(TOPIC, json.dumps(payload))
            print(f"[EDGE 1 -> MQTT] Noise Class: {detected_class} | Energy: {energy}")
            time.sleep(2)
    except KeyboardInterrupt:
        client.disconnect()

if __name__ == "__main__":
    run_edge1()
