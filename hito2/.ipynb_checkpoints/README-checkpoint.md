# 🎧 Proyecto: Clasificación de Instrumentos Musicales mediante Análisis Espectral

### Integrantes:
- Benjamin Martínez Cereceda  
- Katherine Zapata  

---

## 🎯 Descripción General

Este proyecto busca desarrollar una **aplicación interactiva** capaz de:

1. 🎙️ **Grabar audio en tiempo real.**  
2. 🔊 **Realizar un análisis espectral** del sonido obtenido.  
3. 🎵 **Determinar el instrumento musical más similar** entre una base de sonidos de referencia preexistente.  

El enfoque combina **procesamiento digital de señales (PDS)** y **comparación espectral**, inspirándose en modelos de clasificación acústica como **YAMNet**, pero implementado de forma **original y explicable**.

---

## 🧩 Objetivos del Proyecto

### Objetivo General
Desarrollar un sistema reproducible que integre captura, análisis y clasificación de audio, aplicando conceptos de procesamiento de señales y aprendizaje automático clásico.

### Objetivos Específicos
1. Implementar un módulo que permita grabar audios en tiempo real desde micrófono. ✅  
2. Analizar el espectro de frecuencias de una señal grabada y visualizarlo. ✅  
3. Desarrollar un clasificador propio basado en **comparación espectral**. ✅  
4. Organizar la base de datos de sonidos de referencia (instrumentos). ✅  
5. (Etapa siguiente) Crear una interfaz visual o notebook con resultados explicativos. ⏳  

---

## 🗂️ Estructura del Repositorio

proyecto_audio/
│
├── main.py # flujo principal del programa
├── recorder.py # módulo de grabación de audio
├── analyzer.py # análisis espectral y visualización
├── classifier.py # comparación espectral entre audios
├── sounds/ # base de sonidos de instrumentos
│ ├── guitarra.wav
│ ├── piano.wav
│ ├── violin.wav
│ └── ...
├── proyecto_audio.ipynb # notebook demostrativo (análisis y figuras)
├── requirements.txt # dependencias del entorno
└── README.md # descripción del proyecto

yaml
Copiar código

---

## ⚙️ Requisitos e Instalación

### Dependencias principales
sounddevice
scipy
numpy
matplotlib
soundfile

go
Copiar código

Instalación rápida:
```bash
pip install -r requirements.txt
▶️ Ejecución del Proyecto
Ejecutar el archivo principal:

bash
Copiar código
python main.py
El programa:

Graba 3 s de audio.

Muestra el espectro de frecuencias.

Compara el espectro con los sonidos de referencia.

Imprime el instrumento más similar.

Ejemplo de salida:

yaml
Copiar código
Grabando 3 segundos...
🎵 Resultados de similitud espectral:
  guitarra     → 0.876
  piano        → 0.645
  violin       → 0.512

🎯 Instrumento más parecido: GUITARRA
📊 Análisis y Visualizaciones
El análisis espectral se realiza mediante la Transformada Rápida de Fourier (FFT).
El notebook proyecto_audio.ipynb incluye:

Figura del espectro de frecuencia.

Comparaciones entre espectros grabados y de referencia.

Explicaciones interpretativas sobre los resultados obtenidos.

Ejemplo de gráfico:


🧠 Metodología del Clasificador
El clasificador implementado se basa en similitud espectral:

Se calcula el espectro de magnitud de cada audio (FFT).

Se normaliza el espectro (para eliminar efectos de volumen).

Se calcula la correlación normalizada entre la grabación y cada sonido base.

El instrumento con mayor correlación se considera el más similar.

Matemáticamente:

similitud
(
𝑥
,
𝑦
)
=
𝑥
⋅
𝑦
∣
∣
𝑥
∣
∣
 
∣
∣
𝑦
∣
∣
similitud(x,y)= 
∣∣x∣∣∣∣y∣∣
x⋅y
​
 
Este método permite distinguir patrones de frecuencia característicos de cada instrumento sin depender de modelos externos.

📈 Avances Concretos (Hito Actual)
✅ Grabación funcional y estable de audio.

✅ Visualización de espectros.

✅ Clasificador propio basado en correlación espectral.

✅ Estructura modular y organizada del código.

⏳ Próximo paso: interfaz visual y ampliación de la base de datos de sonidos.

💬 Reflexión y Trabajo Futuro
El sistema demuestra que es posible identificar instrumentos musicales mediante procesamiento digital de señales simple pero efectivo.
En futuras etapas se planea:

Añadir métricas de precisión y validación cruzada.

Implementar una interfaz gráfica (Tkinter / PyQt).

Experimentar con embeddings de audio para mejorar la clasificación.

👨‍🔬 Créditos y Referencias
Inspirado en:

YAMNet: Sound classification using TF-Hub

AudioSet: A large-scale dataset for audio classification

Implementación original basada en técnicas de procesamiento digital de señales (FFT, correlación espectral).