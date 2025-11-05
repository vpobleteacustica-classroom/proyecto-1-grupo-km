# clasificador.py
# modelo (YAMNet o similar)
# Usaremos TensorFlow Hub para cargar un modelo preentrenado
# (install tensorflow and tensorflow-hub if not installed)

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import soundfile as sf

# Cargar modelo YAMNet
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

def predecir_instrumento(archivo):
    wav_data, sr = sf.read(archivo, dtype=np.float32)
    scores, embeddings, spectrogram = yamnet_model(wav_data)
    mean_scores = np.mean(scores, axis=0)

    # Cargar etiquetas de AudioSet
    class_map_path = tf.keras.utils.get_file(
        'yamnet_class_map.csv',
        'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
    )
    class_names = [line.split(',')[2].strip() for line in open(class_map_path).readlines()[1:]]
    top5_i = np.argsort(mean_scores)[::-1][:5]
    print("\n🔊 Posibles instrumentos detectados:")
    for i in top5_i:
        print(f"- {class_names[i]} ({mean_scores[i]:.3f})")
    return class_names[top5_i[0]]

# comentar todo con "ctrl + /"
# Alternativa simple basada en similitud espectral
# import numpy as np
# from scipy.io import wavfile
# import os

# def calcular_espectro(archivo):
#     """Calcula el espectro de magnitud normalizado de un archivo .wav"""
#     fs, data = wavfile.read(archivo)
#     data = data.astype(float)
#     data = data / np.max(np.abs(data))  # normalización de amplitud
#     N = len(data)
#     espectro = np.abs(np.fft.fft(data)[:N//2])
#     espectro = espectro / np.sum(espectro)  # normalización espectral
#     return espectro

# def similitud_espectral(espectro1, espectro2):
#     """Calcula la similitud entre dos espectros (1 = idénticos, 0 = distintos)"""
#     min_len = min(len(espectro1), len(espectro2))
#     espectro1 = espectro1[:min_len]
#     espectro2 = espectro2[:min_len]
#     # correlación normalizada
#     return np.dot(espectro1, espectro2) / (np.linalg.norm(espectro1) * np.linalg.norm(espectro2))

# def clasificar_instrumento(audio_usuario, carpeta_sonidos="sounds"):
#     """Compara el audio grabado con la base de sonidos y retorna el más similar"""
#     espectro_usuario = calcular_espectro(audio_usuario)
#     similitudes = {}

#     for archivo in os.listdir(carpeta_sonidos):
#         if archivo.endswith(".wav"):
#             ruta = os.path.join(carpeta_sonidos, archivo)
#             espectro_ref = calcular_espectro(ruta)
#             similitud = similitud_espectral(espectro_usuario, espectro_ref)
#             similitudes[archivo.replace(".wav", "")] = similitud

#     instrumento_predicho = max(similitudes, key=similitudes.get)

#     print("\n🎵 Resultados de similitud espectral:")
#     for inst, score in similitudes.items():
#         print(f"  {inst:<12} → {score:.3f}")

#     print(f"\n🎯 Instrumento más parecido: {instrumento_predicho.upper()}")
#     return instrumento_predicho