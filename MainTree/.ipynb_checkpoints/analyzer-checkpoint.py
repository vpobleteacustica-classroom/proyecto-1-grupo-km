# analizador.py
# análisis espectral y extracción de características
# Usaremos numpy + matplotlib para visualizar y obtener el espectro
# (install numpy y matplotlib si no están instalados)

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def analizar_espectro(archivo):
    fs, data = wavfile.read(archivo)
    data = data.flatten()
    N = len(data)
    fft = np.fft.fft(data)
    freqs = np.fft.fftfreq(N, 1/fs)
    magnitud = np.abs(fft[:N//2])

    plt.figure(figsize=(8,4))
    plt.plot(freqs[:N//2], magnitud)
    plt.title("Espectro de Frecuencia")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Magnitud")
    plt.show()

    return magnitud, freqs