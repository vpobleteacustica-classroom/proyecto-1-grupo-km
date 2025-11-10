# clasificador.py
# modelo (YAMNet o similar)
# Usaremos TensorFlow Hub para cargar un modelo preentrenado

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import soundfile as sf
from instrumentos import INSTRUMENTOS_VALIDOS, es_instrumento  # <-- NUEVO

# Cargar modelo YAMNet
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

# Cargar etiquetas de AudioSet (una sola vez)
class_map_path = tf.keras.utils.get_file(
    'yamnet_class_map.csv',
    'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
)
class_names = [line.split(',')[2].strip() for line in open(class_map_path).readlines()[1:]]

def predecir_instrumento(archivo):
    wav_data, sr = sf.read(archivo, dtype=np.float32)
    scores, embeddings, spectrogram = yamnet_model(wav_data)
    mean_scores = np.mean(scores, axis=0)

    # ------------------- NUEVA LÓGICA DE FILTRADO -------------------
    # 1. Crear lista de tuplas (índice, score, nombre) solo para instrumentos válidos
    candidatos = []
    for i, score in enumerate(mean_scores):
        nombre = class_names[i]
        if es_instrumento(nombre):  # Solo si está en tu lista
            candidatos.append((i, score, nombre))

    # 2. Si no hay ningún instrumento válido → devolver mensaje claro
    if not candidatos:
        print("\n🎵 No se detectó ningún instrumento de la lista permitida.")
        return None

    # 3. Ordenar por score descendente
    candidatos.sort(key=lambda x: x[1], reverse=True)

    # 4. Mostrar top 5 (o menos si hay menos)
    print("\n🔊 Instrumentos detectados (solo de la lista permitida):")
    for i, (idx, score, nombre) in enumerate(candidatos[:5]):
        print(f"{i+1}. {nombre} ({score:.3f})")

    # 5. Devolver el instrumento con mayor score
    mejor_instrumento = candidatos[0][2]
    print(f"\n🎯 Instrumento clasificado: {mejor_instrumento.upper()}")
    return mejor_instrumento
    # ---------------------------------------------------------------

    # El código anterior (sin filtro) queda comentado por si quieres compararlo:
    """
    top5_i = np.argsort(mean_scores)[::-1][:5]
    print("\n🔊 Posibles instrumentos detectados (sin filtro):")
    for i in top5_i:
        print(f"- {class_names[i]} ({mean_scores[i]:.3f})")
    return class_names[top5_i[0]]
    """