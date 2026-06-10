import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

def generate_noisy_ecg(fs, duration):
    t = np.linspace(0, duration, fs * duration)
    ecg_clean = np.zeros_like(t)
    picos_true = np.arange(fs, len(t), int(fs * 0.8))
    for p in picos_true:
        ecg_clean[p:p+10] = [0.2, 0.5, 1.2, -0.4, 0.1, 0.2, 0.1, 0, 0, 0]
    ruido_alta = 0.15 * np.sin(2 * np.pi * 50 * t)
    ruido_baja = 0.4 * np.sin(2 * np.pi * 0.3 * t)
    return t, ecg_clean + ruido_alta + ruido_baja

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

def main():
    fs = 250
    duracion = 10
    t, ecg_raw = generate_noisy_ecg(fs, duracion)
    ecg_filtered = butter_bandpass_filter(ecg_raw, lowcut=0.5, highcut=45.0, fs=fs, order=4)

    min_distancia_muestras = int(fs * 0.3)
    picos, _ = find_peaks(ecg_filtered, distance=min_distancia_muestras, prominence=0.4)

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t, ecg_raw, color='salmon', label='Señal Cruda (Ruido)')
    plt.title('Procesamiento de ECG y Detección de Picos R')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t, ecg_filtered, color='teal', label='Señal Filtrada (0.5 - 45 Hz)')
    plt.plot(t[picos], ecg_filtered[picos], "x", color='red', markersize=10, label='Picos R')
    plt.xlabel('Tiempo (segundos)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('ecg_processing_result.png')
    plt.show()

if __name__ == "__main__":
    main()