import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

st.set_page_config(page_title="ECG Signal Processor", layout="wide")

st.title("🔬 Interactive ECG Signal Processor")
st.markdown("This application simulates a raw ECG signal contaminated with motion artifacts (low-frequency drift) and muscle tremor (high-frequency noise), applying an adaptive Butterworth bandpass filter.")

# --- Sidebar Controls ---
st.sidebar.header("🎛️ Filter Configuration")

# Interactive sliders for signal processing tuning
lowcut = st.sidebar.slider("Low cutoff frequency (Removes baseline wander/respiration)", 0.1, 5.0, 0.5, 0.1)
highcut = st.sidebar.slider("High cutoff frequency (Removes powerline/muscle noise)", 20.0, 100.0, 45.0, 1.0)
order = st.sidebar.slider("Filter Order", 1, 8, 4)

st.sidebar.header("⏱️ R-Peak Detection")
prominence = st.sidebar.slider("Minimum R-peak prominence", 0.1, 2.0, 0.4, 0.05)

# --- Signal Processing Core Functions ---
@st.cache_data
def generate_noisy_ecg(fs, duration):
    """Simulates a synthetic ECG signal with added clinical and physical noise artifacts."""
    t = np.linspace(0, duration, fs * duration)
    ecg_clean = np.zeros_like(t)
    true_peaks = np.arange(fs, len(t), int(fs * 0.8)) # Target: ~75 bpm
    for p in true_peaks:
        ecg_clean[p:p+10] = [0.2, 0.5, 1.2, -0.4, 0.1, 0.2, 0.1, 0, 0, 0]
    
    high_freq_noise = 0.15 * np.sin(2 * np.pi * 50 * t)   # 50 Hz powerline interference
    low_freq_noise = 0.4 * np.sin(2 * np.pi * 0.3 * t)    # Baseline wander from respiration
    return t, ecg_clean + high_freq_noise + low_freq_noise

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    """Designs and applies a zero-phase Butterworth bandpass filter."""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data) # filtfilt prevents phase shift, crucial for clinical timing

# --- Execution Pipeline ---
fs = 250  # Sampling frequency (Hz)
duration = 10  # Seconds
t, ecg_raw = generate_noisy_ecg(fs, duration)

# Dynamic filtering based on user input
ecg_filtered = butter_bandpass_filter(ecg_raw, lowcut, highcut, fs, order=order)

# Dynamic R-peak (QRS complex) detection
min_distance_samples = int(fs * 0.3) # Refractory period constraint (~200 bpm max)
picos, _ = find_peaks(ecg_filtered, distance=min_distance_samples, prominence=prominence)

# --- UI Dashboard Rendering ---
col1, col2 = st.columns(2)
col1.metric("Estimated Heart Rate", f"{int(len(picos) * (60/duration))} BPM")
col2.metric("Detected R-Peaks", f"{len(picos)} peaks")

# Visualization setup using Matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Subplot 1: Raw Signal
ax1.plot(t, ecg_raw, color='salmon', label='Raw Signal (Contaminated)')
ax1.set_title('Original vs. Filtered ECG Signal in Real-Time')
ax1.set_ylabel('Voltage (mV)')
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--')

# Subplot 2: Filtered Signal + Peak Detection
ax2.plot(t, ecg_filtered, color='teal', label=f'Bandpass Filter ({lowcut} - {highcut} Hz)')
ax2.plot(t[picos], ecg_filtered[picos], "x", color='red', markersize=10, label='Detected R-Peaks (QRS)')
ax2.set_xlabel('Time (seconds)')
ax2.set_ylabel('Voltage (mV)')
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--')

plt.tight_layout()
st.pyplot(fig)