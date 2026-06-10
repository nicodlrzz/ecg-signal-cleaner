import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

st.set_page_config(page_title="ECG Signal Processor", layout="wide")

st.title("🔬 Procesador Interactivo de Señales ECG")
st.markdown("Esta aplicación simula una señal ECG contaminada con ruido de movimiento (baja frecuencia) y temblor muscular (alta frecuencia), aplicando un filtro Butterworth adaptativo.")

# --- Barra Lateral de Controles (Sidebar) ---
st.sidebar.header("🎛️ Configuración del Filtro")

# Sliders interactivas para que el usuario juegue con las frecuencias
lowcut = st.sidebar.slider("Frecuencia de corte baja (Filtra respiración/movimiento)", 0.1, 5.0, 0.5, 0.1)
highcut = st.sidebar.slider("Frecuencia de corte alta (Filtra ruido de red/músculo)", 20.0, 100.0, 45.0, 1.0)
order = st.sidebar.slider("Orden del Filtro", 1, 8, 4)

st.sidebar.header("⏱️ Detección de Picos R")
prominence = st.sidebar.slider("Prominencia mínima del Pico R", 0.1, 2.0, 0.4, 0.05)

# --- Funciones de Procesamiento (Mismo Core Fisiológico) ---
@st.cache_data
def generate_noisy_ecg(fs, duration):
    t = np.linspace(0, duration, fs * duration)
    ecg_clean = np.zeros_like(t)
    picos_true = np.arange(fs, len(t), int(fs * 0.8)) # ~75 lpm
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

# --- Pipeline de Ejecución ---
fs = 250  # Hz
duracion = 10  # segundos
t, ecg_raw = generate_noisy_ecg(fs, duracion)

# Filtrado dinámico usando los valores de los sliders
ecg_filtered = butter_bandpass_filter(ecg_raw, lowcut, highcut, fs, order=order)

# Detección dinámica de picos usando el slider de prominencia
min_distancia_muestras = int(fs * 0.3)
picos, _ = find_peaks(ecg_filtered, distance=min_distancia_muestras, prominence=prominence)

# --- Renderizado en la Interfaz ---
# Métricas rápidas en pantalla
col1, col2 = st.columns(2)
col1.metric("Frecuencia Cardíaca Estimada", f"{int(len(picos) * (60/duracion))} lpm")
col2.metric("Picos R Detectados", f"{len(picos)} picos")

# Dibujar los gráficos en un contenedor de Matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

ax1.plot(t, ecg_raw, color='salmon', label='Señal Cruda (Con Ruido)')
ax1.set_title('Señal ECG Original vs. Filtrada en Tiempo Real')
ax1.ylabel('Voltaje (mV)')
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--')

ax2.plot(t, ecg_filtered, color='teal', label=f'Filtro Pasabanda ({lowcut} - {highcut} Hz)')
ax2.plot(t[picos], ecg_filtered[picos], "x", color='red', markersize=10, label='Picos R (QRS) Detectados')
ax2.set_xlabel('Tiempo (segundos)')
ax2.set_ylabel('Voltaje (mV)')
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--')

plt.tight_layout()

# EL TRUCO: st.pyplot mapea el objeto 'fig' de matplotlib directamente a la web
st.pyplot(fig)