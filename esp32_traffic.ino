#include <WiFi.h>
#include <PubSubClient.h>

const char* WIFI_SSID     = "WIFI_NAME";
const char* WIFI_PASS     = "WIFI_PASSWORD";
const char* MQTT_SERVER   = "broker.hivemq.com";
const int   MQTT_PORT     = 1883;
const char* TOPIC_TRAFFIC = "iot/smart_traffic_kelompok_07/edge2/traffic";

const int PIN_IR1   = 18;
const int PIN_IR2   = 19;
const int PIN_MQ135 = 34;

const float DISTANCE_M = 0.10; // 10 cm
unsigned long t1 = 0;
bool active_t1 = false;
float filtered_mq = 0.0;
const float ALPHA = 0.2;

WiFiClient espClient;
PubSubClient mqtt(espClient);

void setup() {
  Serial.begin(115200);
  pinMode(PIN_IR1, INPUT_PULLUP);
  pinMode(PIN_IR2, INPUT_PULLUP);
  
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  
  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
  filtered_mq = analogRead(PIN_MQ135);
}

void loop() {
  if (!mqtt.connected()) mqtt.connect("ESP32_Edge2_Node");
  mqtt.loop();

  // 1. Time-Delta Speed Measurement
  if (digitalRead(PIN_IR1) == LOW && !active_t1) {
    t1 = millis();
    active_t1 = true;
  }

  if (digitalRead(PIN_IR2) == LOW && active_t1) {
    unsigned long delta = millis() - t1;
    if (delta > 20) {
      float speed_mps = DISTANCE_M / (delta / 1000.0);
      float speed_kmh = speed_mps * 3.6;

      // Filter MQ135 dengan EMA
      int raw_mq = analogRead(PIN_MQ135);
      filtered_mq = (ALPHA * raw_mq) + ((1.0 - ALPHA) * filtered_mq);

      // JSON Payload
      String json = "{\"speed_kmh\":" + String(speed_kmh) + ",\"air_ppm\":" + String(filtered_mq) + "}";
      mqtt.publish(TOPIC_TRAFFIC, json.c_str());
    }
    active_t1 = false;
    delay(300);
  }
}
