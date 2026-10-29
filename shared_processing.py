import numpy as np

def process_audio_energy(pcm_samples):
    """DATA PROCESSING 1:Mengolah sinyal audio mentah (PCM) menjadi nilai RMS Energi Suara."""
    if not pcm_samples:
        return 0.0
    arr = np.array(pcm_samples, dtype=float)
    rms = np.sqrt(np.mean(arr ** 2))
    return round(float(rms), 2)


def process_ema_filter(new_val, prev_val, alpha=0.2):
    """DATA PROCESSING 2:Exponential Moving Average (EMA) untuk filtering noise sensor MQ-135 & Kecepatan.
    """
    if prev_val is None:
        return round(float(new_val), 2)
    filtered = (alpha * float(new_val)) + ((1.0 - alpha) * float(prev_val))
    return round(filtered, 2)
