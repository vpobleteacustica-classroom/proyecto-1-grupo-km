#!/usr/bin/env python3
"""
Script de Configuración y Verificación
Clasificador de Instrumentos Musicales - Hito 3
ACUS220 - Universidad Austral de Chile
"""

import sys
import subprocess
import importlib
from pathlib import Path

def print_header(text):
    """Imprimir encabezado formateado"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_status(status, message):
    """Imprimir estado con emoji"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {message}")

def check_python_version():
    """Verificar versión de Python"""
    print_header("1. Verificando Python")
    version = sys.version_info
    required = (3, 8)
    
    if version >= required:
        print_status(True, f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_status(False, f"Python {version.major}.{version.minor} detectado")
        print(f"   Se requiere Python >= {required[0]}.{required[1]}")
        return False

def check_packages():
    """Verificar paquetes requeridos"""
    print_header("2. Verificando Paquetes")
    
    packages = {
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'matplotlib': 'Matplotlib',
        'sounddevice': 'SoundDevice',
        'soundfile': 'SoundFile',
        'tensorflow': 'TensorFlow',
        'tensorflow_hub': 'TensorFlow Hub'
    }
    
    missing = []
    installed = []
    
    for package, name in packages.items():
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, '__version__', 'N/A')
            print_status(True, f"{name:20} v{version}")
            installed.append(package)
        except ImportError:
            print_status(False, f"{name:20} NO INSTALADO")
            missing.append(package)
    
    return missing, installed

def install_packages(packages):
    """Instalar paquetes faltantes"""
    if not packages:
        return True
    
    print_header("3. Instalando Paquetes Faltantes")
    print(f"\n📦 Instalando: {', '.join(packages)}\n")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '--upgrade'
        ] + packages)
        print_status(True, "Paquetes instalados correctamente")
        return True
    except subprocess.CalledProcessError:
        print_status(False, "Error al instalar paquetes")
        return False

def check_project_structure():
    """Verificar estructura del proyecto"""
    print_header("4. Verificando Estructura del Proyecto")
    
    required_files = {
        'recorder.py': 'Módulo de grabación',
        'analyzer.py': 'Módulo de análisis',
        'classifier.py': 'Módulo de clasificación',
        'instrumentos.py': 'Lista de instrumentos',
        'gui_interface.py': 'Interfaz gráfica',
        'requirements.txt': 'Dependencias'
    }
    
    all_present = True
    for file, description in required_files.items():
        path = Path(file)
        exists = path.exists()
        print_status(exists, f"{file:20} - {description}")
        if not exists:
            all_present = False
    
    return all_present

def test_audio_devices():
    """Probar dispositivos de audio"""
    print_header("5. Verificando Dispositivos de Audio")
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        
        print("\n📢 Dispositivos de audio disponibles:\n")
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"  [{i}] {device['name']}")
                print(f"      Canales entrada: {device['max_input_channels']}")
                print(f"      Frecuencia: {device['default_samplerate']} Hz\n")
        
        # Intentar grabar 1 segundo de prueba
        print("🎙️  Probando grabación de 1 segundo...")
        test_audio = sd.rec(int(1 * 16000), samplerate=16000, channels=1)
        sd.wait()
        print_status(True, "Grabación de prueba exitosa")
        return True
        
    except Exception as e:
        print_status(False, f"Error con audio: {str(e)}")
        return False

def test_yamnet_loading():
    """Probar carga del modelo YAMNet"""
    print_header("6. Verificando Modelo YAMNet")
    
    try:
        import tensorflow_hub as hub
        print("\n🔄 Descargando/cargando YAMNet (puede tardar)...")
        
        model = hub.load('https://tfhub.dev/google/yamnet/1')
        print_status(True, "Modelo YAMNet cargado correctamente")
        
        # Verificar clase map
        import tensorflow as tf
        class_map_path = tf.keras.utils.get_file(
            'yamnet_class_map.csv',
            'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
        )
        print_status(True, "Mapa de clases descargado")
        return True
        
    except Exception as e:
        print_status(False, f"Error al cargar YAMNet: {str(e)}")
        return False

def test_full_pipeline():
    """Probar pipeline completo"""
    print_header("7. Prueba del Pipeline Completo")
    
    try:
        # Importar módulos
        from recorder import grabar_audio
        from analyzer import analizar_espectro
        from classifier import predecir_instrumento
        
        print("\n📝 Módulos importados correctamente")
        
        # Grabar audio de prueba (3 segundos)
        print("🎙️  Grabando 3 segundos de prueba...")
        print("   (Puedes hacer ruido o quedarte en silencio)\n")
        
        archivo = grabar_audio(nombre_archivo="test_setup.wav", duracion=3)
        print_status(True, f"Audio guardado: {archivo}")
        
        # Analizar
        print("\n📊 Analizando espectro...")
        magnitud, freqs = analizar_espectro(archivo)
        print_status(True, "Análisis espectral completado")
        
        # Clasificar
        print("\n🤖 Clasificando con YAMNet...")
        resultado = predecir_instrumento(archivo, umbral_confianza=0.01)
        
        if resultado:
            inst, conf = resultado
            print_status(True, f"Clasificación: {inst} ({conf:.3f})")
        else:
            print_status(True, "Sin detección (normal para audio de prueba)")
        
        # Limpiar archivo de prueba
        Path(archivo).unlink()
        print("\n🗑️  Archivo de prueba eliminado")
        
        return True
        
    except Exception as e:
        print_status(False, f"Error en pipeline: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def print_summary(results):
    """Imprimir resumen final"""
    print_header("RESUMEN DE VERIFICACIÓN")
    
    all_ok = all(results.values())
    
    print("\n📋 Estado de verificaciones:\n")
    for check, status in results.items():
        print_status(status, check)
    
    if all_ok:
        print("\n" + "="*70)
        print("  🎉 ¡TODO LISTO! El sistema está configurado correctamente")
        print("="*70)
        print("\n📝 Próximos pasos:\n")
        print("   1. Ejecuta la interfaz gráfica:")
        print("      python gui_interface.py\n")
        print("   2. O usa el notebook de demostración:")
        print("      jupyter notebook HITO3_Demo.ipynb\n")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("  ⚠️  ATENCIÓN: Hay problemas que requieren solución")
        print("="*70)
        print("\n💡 Sugerencias:\n")
        print("   • Verifica que todos los archivos estén presentes")
        print("   • Instala paquetes faltantes: pip install -r requirements.txt")
        print("   • Revisa que tu micrófono esté conectado")
        print("   • Consulta la documentación en README_HITO3.md\n")
        print("="*70)

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("  🎵 CONFIGURACIÓN Y VERIFICACIÓN - HITO 3")
    print("  Clasificador de Instrumentos Musicales")
    print("  ACUS220 - Universidad Austral de Chile")
    print("="*70)
    
    results = {}
    
    # 1. Python version
    results['Python >= 3.8'] = check_python_version()
    if not results['Python >= 3.8']:
        print("\n❌ Python version insuficiente. Saliendo...")
        return
    
    # 2. Check packages
    missing, installed = check_packages()
    results['Paquetes instalados'] = len(missing) == 0
    
    # 3. Install missing packages
    if missing:
        print(f"\n⚠️  Faltan {len(missing)} paquetes")
        install = input("\n¿Deseas instalarlos ahora? (s/n): ").lower().strip()
        
        if install == 's':
            if install_packages(missing):
                results['Paquetes instalados'] = True
            else:
                print("\n❌ No se pudieron instalar los paquetes")
                results['Paquetes instalados'] = False
        else:
            print("\n⚠️  Continuando sin instalar paquetes faltantes...")
    
    # 4. Project structure
    results['Estructura del proyecto'] = check_project_structure()
    
    # 5. Audio devices
    if results['Paquetes instalados']:
        results['Dispositivos de audio'] = test_audio_devices()
    else:
        print_header("5. Verificando Dispositivos de Audio")
        print("⏭️  Omitido (paquetes no instalados)")
        results['Dispositivos de audio'] = False
    
    # 6. YAMNet loading
    if results['Paquetes instalados']:
        results['Modelo YAMNet'] = test_yamnet_loading()
    else:
        print_header("6. Verificando Modelo YAMNet")
        print("⏭️  Omitido (paquetes no instalados)")
        results['Modelo YAMNet'] = False
    
    # 7. Full pipeline test
    if all([results.get('Paquetes instalados'),
            results.get('Estructura del proyecto'),
            results.get('Dispositivos de audio'),
            results.get('Modelo YAMNet')]):
        
        test = input("\n¿Deseas probar el pipeline completo? (s/n): ").lower().strip()
        if test == 's':
            results['Pipeline completo'] = test_full_pipeline()
        else:
            print_header("7. Prueba del Pipeline Completo")
            print("⏭️  Omitido por el usuario")
            results['Pipeline completo'] = None
    else:
        print_header("7. Prueba del Pipeline Completo")
        print("⏭️  Omitido (verificaciones previas fallaron)")
        results['Pipeline completo'] = False
    
    # Summary
    print_summary(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)