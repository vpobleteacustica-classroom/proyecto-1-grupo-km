# classifier.py
# Modelo de clasificación con YAMNet
# Versión mejorada con mejor visualización y manejo de errores

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import soundfile as sf
from instrumentos import INSTRUMENTOS_VALIDOS, es_instrumento

# Cargar modelo YAMNet (se descarga una sola vez)
print("🔄 Cargando modelo YAMNet...")
yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
print("✅ Modelo YAMNet cargado correctamente")

# Cargar etiquetas de AudioSet
class_map_path = tf.keras.utils.get_file(
    'yamnet_class_map.csv',
    'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
)
class_names = [line.split(',')[2].strip() for line in open(class_map_path).readlines()[1:]]
print(f"✅ {len(class_names)} clases de AudioSet cargadas")

def predecir_instrumento(archivo, umbral_confianza=0.025, mostrar_top5=True):
    """
    Predice el instrumento musical en un archivo de audio.
    
    Parámetros:
    -----------
    archivo : str
        Ruta al archivo de audio (.wav)
    umbral_confianza : float
        Umbral mínimo de confianza para aceptar predicción (default: 0.025)
    mostrar_top5 : bool
        Si True, muestra los top 5 instrumentos en consola
        
    Retorna:
    --------
    tuple or None
        (nombre_instrumento, confianza) si se detecta algo,
        None si no hay detección válida
    """
    try:
        # Leer archivo de audio
        wav_data, sr = sf.read(archivo, dtype=np.float32)
        
        # Convertir a mono si es estéreo
        if wav_data.ndim > 1:
            wav_data = np.mean(wav_data, axis=1)
        
        # Ejecutar modelo YAMNet
        scores, embeddings, spectrogram = yamnet_model(wav_data)
        
        # Promediar scores temporales
        mean_scores = np.mean(scores, axis=0)
        
        # Filtrar solo instrumentos válidos
        candidatos = []
        for i, score in enumerate(mean_scores):
            nombre = class_names[i]
            if es_instrumento(nombre):
                candidatos.append((nombre, float(score)))
        
        # Si no hay candidatos válidos
        if not candidatos:
            print("\n❌ No se detectó ningún instrumento válido")
            print("💡 Posibles causas:")
            print("   • El audio no contiene instrumentos musicales")
            print("   • Volumen muy bajo")
            print("   • Demasiado ruido de fondo")
            return None
        
        # Ordenar por score descendente
        candidatos.sort(key=lambda x: x[1], reverse=True)
        
        # Mostrar top 5 si se solicita
        if mostrar_top5:
            print("\n" + "="*50)
            print("🎵 TOP 5 INSTRUMENTOS DETECTADOS")
            print("="*50)
            for i, (nombre, score) in enumerate(candidatos[:5], start=1):
                barra = "█" * int(score * 100)
                print(f"{i}. {nombre:20} | {score:6.4f} | {barra}")
            print("="*50)
        
        # Obtener mejor predicción
        mejor_instrumento, confianza = candidatos[0]
        
        # Verificar umbral
        if confianza < umbral_confianza:
            print(f"\n⚠️  Confianza insuficiente: {confianza:.4f} < {umbral_confianza}")
            print(f"💡 Umbral actual: {umbral_confianza}")
            print("   Puedes ajustarlo en la configuración")
            return None
        
        # Resultado exitoso
        print(f"\n✅ RESULTADO FINAL:")
        print(f"   🎯 Instrumento: {mejor_instrumento.upper()}")
        print(f"   📊 Confianza: {confianza:.4f} ({confianza*100:.1f}%)")
        
        return mejor_instrumento, confianza
        
    except Exception as e:
        print(f"\n❌ Error al procesar audio: {str(e)}")
        return None

def obtener_todos_instrumentos():
    """
    Retorna la lista de todos los instrumentos que puede detectar el sistema.
    
    Retorna:
    --------
    list
        Lista de nombres de instrumentos
    """
    return sorted(list(INSTRUMENTOS_VALIDOS))

def info_modelo():
    """
    Imprime información sobre el modelo YAMNet y los instrumentos detectables.
    """
    print("\n" + "="*60)
    print("📚 INFORMACIÓN DEL MODELO")
    print("="*60)
    print(f"Modelo: YAMNet (Google AudioSet)")
    print(f"Total de clases AudioSet: {len(class_names)}")
    print(f"Instrumentos detectables: {len(INSTRUMENTOS_VALIDOS)}")
    print("="*60)
    
    print("\n🎵 INSTRUMENTOS DETECTABLES:")
    print("-" * 60)
    
    # Agrupar por categoría
    categorias = {
        "🎹 Teclados": ["Piano", "Electric piano", "Organ", "Synthesizer"],
        "🎸 Cuerdas": ["Guitar", "Electric guitar", "Bass guitar", "Acoustic guitar",
                      "Violin, fiddle", "Cello", "Double bass", "Harp",
                      "Banjo", "Mandolin", "Ukulele"],
        "🎺 Vientos": ["Trumpet", "Trombone", "French horn", "Tuba",
                      "Saxophone", "Flute", "Clarinet"],
        "🥁 Percusión": ["Drum kit", "Drum", "Snare drum", "Timpani",
                        "Hi-hat", "Tambourine", "Maraca",
                        "Xylophone", "Steel drum", "Gong"],
        "🎼 Otros": ["Accordion"]
    }
    
    for categoria, instrumentos in categorias.items():
        print(f"\n{categoria}:")
        for inst in instrumentos:
            if inst in INSTRUMENTOS_VALIDOS:
                print(f"  ✓ {inst}")
    
    print("\n" + "="*60)

# Código de prueba
if __name__ == "__main__":
    print("🎵 Módulo de Clasificación de Instrumentos")
    print("="*60)
    
    # Mostrar información del modelo
    info_modelo()
    
    # Ejemplo de uso
    print("\n💡 Ejemplo de uso:")
    print("-" * 60)
    print("from classifier import predecir_instrumento")
    print()
    print("resultado = predecir_instrumento('grabacion.wav')")
    print("if resultado:")
    print("    instrumento, confianza = resultado")
    print("    print(f'Detectado: {instrumento} ({confianza:.2%})')")
    print("="*60)