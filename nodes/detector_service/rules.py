def evaluate_traffic_status(sound_class, speed_kmh, air_ppm):
    """ALGORITMA RULE ENGINE:Mengkorelasikan data kelas suara, kecepatan kendaraan, dan polusi udara."""
    status = "LANCAR_AMAN"
    alert_level = "LOW"
    message = "Kondisi jalan raya normal dan aman."

    # Rule 1: Macet Parah & Kebisingan Klakson
    if sound_class == "Klakson" and speed_kmh < 15.0:
        status = "MACET_DAN_BISING"
        alert_level = "HIGH"
        message = "Kemacetan terdeteksi! Suara klakson tinggi dengan kecepatan < 15 km/jam."

    # Rule 2: Polusi Emisi Gas Tinggi
    elif air_ppm > 300.0:
        status = "POLUSI_TINGGI"
        alert_level = "MEDIUM"
        message = "Kualitas udara buruk melebihi ambang batas aman."

    # Rule 3: Kendaraan Darurat Melewatin Jembatan/Jalan
    elif sound_class == "Sirene":
        status = "KENDARAAN_DARURAT"
        alert_level = "MEDIUM"
        message = "Terdeteksi suara sirene ambulans / pemadam kebakaran."

    return {
        "status": status,
        "alert_level": alert_level,
        "message": message,
        "metrics": {
            "sound_class": sound_class,
            "speed_kmh": speed_kmh,
            "air_ppm": air_ppm
        }
    }
