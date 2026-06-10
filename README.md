# ECG Signal Cleaner

Este repositorio contiene un pipeline en Python para la limpieza y procesamiento de señales electrocardiográficas (ECG) crudas obtenidas potencialmente de dispositivos wearables.

## 🔬 Justificación Clínica
Las señales de biopotenciales suelen verse contaminadas por artefactos de alta frecuencia (temblores musculares o interferencia de red a 50/60 Hz) y bajas frecuencias (vaivén de la respiración o cambios de posición del sensor). Este script aplica un filtro pasabanda Butterworth (0.5 - 45 Hz) diseñado para preservar el complejo QRS y aislar los picos R para el posterior análisis de HRV.

## 🛠️ Instalación
```bash
pip install -r requirements.txt
python src/cleaner.py