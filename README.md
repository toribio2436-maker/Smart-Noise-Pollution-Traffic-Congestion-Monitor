# Smart-Noise-Pollution-Traffic-Congestion-Monitor
Sistem pemantauan kebisingan lalu lintas, kepadatan kendaraan, dan kualitas udara secara real-time berbasis Edge AI dan IoT.

Proyek ini dikembangkan untuk memenuhi kriteria tugas IoT terdistribusi dengan memanfaatkan 2 Edge Devices (HP Android + ESP32), 2 Jenis Data Processing, 3 Sensor Fisik, serta Protokol Komunikasi Cloud MQTT.

# Gambaran Umum Sistem
Sistem mengintegrasikan analisis sinyal suara berbasis kecerdasan buatan (Edge AI) pada HP Android dengan pengukuran kinetik & polusi udara pada mikrokontroler ESP32. Data dari kedua edge device dikirimkan secara asinkron ke Cloud Broker (MQTT), lalu diolah oleh Sensor Fusion Rule Engine di laptop (Node 3) untuk menentukan tingkat kemacetan dan bahaya lingkungan secara real-time.

<img width="324" height="156" alt="image" src="https://github.com/user-attachments/assets/cf67af7d-19d7-498e-9d7e-3dafc1dc656e" />


  Cara Menjalankan Proyek

1. Persiapan Laptop (Node 3 - Detector)
  1. Clone Repository & Masuk ke Folder:
  git clone https://github.com/toribio2436-maker/Smart-Noise-Pollution-Traffic-Congestion-Monitor.git
  cd Smart-Noise-Pollution-Traffic-Congestion-Monitor
  
  2. Buat File .env Konfigurasi:
  Windows PowerShell:
  Copy-Item .env.example .env
  
  3. Install Dependensi Library:
  pip install -r requirements.txt
  
  4. Jalankan Detector Server:
  python detector.py
  Akses Dashboard di Browser Laptop: http://localhost:8000
  
2. Jalankan Edge 1 (HP Android)
Di aplikasi Termux HP Android (atau terminal kedua di laptop):
python hp_kebisingan.py

3. Upload Program Edge 2 (ESP32)
  1. Buka file esp32_traffic/esp32_traffic.ino di Arduino IDE.
  2. Install library PubSubClient via Library Manager.
  3. Sesuaikan SSID dan Password Wi-Fi:
  
  const char* WIFI_SSID     = "NAMA_WIFI_KAMU";
  const char* WIFI_PASS     = "PASSWORD_WIFI_KAMU";
  
  4. Hubungkan ESP32 ke laptop, pilih Port yang sesuai, lalu klik Upload.


#Logic Algoritma Rule Engine

Sistem mengkorelasikan telemetri dari Edge 1 dan Edge 2 menggunakan aturan keputusan berikut:

# Kondisi 1: Macet Parah & Kebisingan Klakson
if sound_class == "Klakson" and speed_kmh < 15.0:
    status = "MACET_DAN_BISING"

# Kondisi 2: Polusi Emisi Udara Tinggi
elif air_ppm > 300.0:
    status = "POLUSI_TINGGI"

# Kondisi 3: Terdeteksi Kendaraan Darurat
elif sound_class == "Sirene":
    status = "KENDARAAN_DARURAT"

# Kondisi 4: Normal
else:
    status = "LANCAR_AMAN"

