# main.py
# interfaz y flujo principal

from recorder import grabar_audio
from analyzer import analizar_espectro
from classifier import predecir_instrumento

def main():
    archivo = grabar_audio(duracion=3)
    analizar_espectro(archivo)
    instrumento = predecir_instrumento(archivo)
    print(f"\n🎵 Instrumento detectado: {instrumento}")

if __name__ == "__main__":
    main()