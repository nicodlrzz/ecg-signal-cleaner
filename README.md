# Interactive ECG Signal Processor & QRS Detector

A Python-based digital signal processing (DSP) pipeline and interactive dashboard designed to clean raw electrocardiogram (ECG) data and detect cardiac events in real-time.

## 🔬 Clinical Context & Rationale
Biopotential signals collected from wearable devices are highly susceptible to physiological and environmental noise. This repository addresses two major clinical artifacts:
1. **Baseline Wander (< 0.5 Hz):** Caused by patient respiration, thermal drift, and body movement.
2. **High-Frequency Noise (> 40 Hz):** Dominated by electromyographic (EMG) interference from muscle tremors and 50/60 Hz powerline grid interference.

The core algorithm applies a zero-phase **Butterworth Bandpass Filter** to isolate the specific frequency spectrum of the ventricular depolarization (**QRS complex**), followed by a prominence-based peak detection algorithm to isolate R-peaks for subsequent Heart Rate Variability (HRV) analysis.

## 🛠️ Technical Stack
* **Language:** Python 3.9+
* **DSP Framework:** `SciPy` (Signal module)
* **Data Visualization:** `Matplotlib`
* **Interactive UI:** `Streamlit`

## 🚀 Deployment & Local Execution

1. Clone the repository:
```bash
git clone [https://github.com/YOUR_USERNAME/ecg-signal-cleaner.git](https://github.com/YOUR_USERNAME/ecg-signal-cleaner.git)
cd ecg-signal-cleaner