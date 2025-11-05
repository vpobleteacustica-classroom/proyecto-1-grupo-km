# recorder.py
# grabación de audio en tiempo real
# Usaremos sounddevice y scipy para grabar y guardar el audio
# (install sounddevice y scipy si no están instalados)

import sounddevice as sd
from scipy.io.wavfile import write

def grabar_audio(nombre_archivo="grabacion.wav", duracion=3, fs=16000):
    print(f"Grabando {duracion} segundos...")
    audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1)
    sd.wait()
    write(nombre_archivo, fs, audio)
    print(f"Grabación guardada como {nombre_archivo}")
    return nombre_archivo