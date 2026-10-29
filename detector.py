import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from nodes.detector_service.rules import evaluate_traffic_status
from shared.dashboard_server import start_dashboard_server

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "smart_traffic_kelompok_07")
MQTT_HOST = os.getenv("MQTT_HOST", "broker.hivemq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Memory data ter-update
state = {
    "sound_class": "Quiet",
    "speed_kmh": 40.0,
    "air_ppm": 120.0
}

def on_message(client, userdata, msg):
    global state
    try:
        data = json.loads(msg.payload.decode())
        if "edge1" in msg.topic:
            state["sound_class"] = data.get("sound_class", "Quiet")
        elif "edge2" in msg.topic:
            state["speed_kmh"] = data.get("speed_kmh", 0.0)
            state["air_ppm"] = data.get("air_ppm", 0.0)

        # Evaluasi dengan Rule Engine AI
        result = evaluate_traffic_status(
            state["sound_class"],
            state["speed_kmh"],
            state["air_ppm"]
        )

        print("\n=================== [SYSTEM DETECTOR STATUS] ===================")
        print(f"STATUS  : {result['status']} (Alert Level: {result['alert_level']})")
        print(f"DETAIL  : {result['message']}")
        print(f"METRICS : Speed={result['metrics']['speed_kmh']} km/h | Air={result['metrics']['air_ppm']} PPM | Sound={result['metrics']['sound_class']}")

    except Exception as e:
        print(f"[ERROR] Parsing message failed: {e}")

def run():
    server, thread, url = start_dashboard_server()
    print(f"\n[DASHBOARD] Buka Dashboard di Laptop: {url}")
    print(f"[CONFIG] PROJECT_ID: {PROJECT_ID}")

    client = mqtt.Client(client_id="Laptop_Detector_Node3")
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    
    # Subscribe ke semua topik project kelompok
    client.subscribe(f"iot/{PROJECT_ID}/#")
    print("[DETECTOR] Listening for MQTT data from Edge 1 & Edge 2...\n")

    try:
        client.loop_forever()
    finally:
        server.shutdown()

if __name__ == "__main__":
    run()
