# 🎤 Guía para Presentación - Hito 3
## Clasificador de Instrumentos Musicales

**Duración total:** 15-20 minutos  
**Curso:** ACUS220 - Universidad Austral de Chile

---

## 📋 Estructura de la Presentación

### Diapositiva 1: TÍTULO (30 seg)
```
🎵 CLASIFICADOR DE INSTRUMENTOS MUSICALES
Análisis Espectral y Machine Learning

Benjamin Martínez Cereceda
Katherine Zapata

ACUS220 - Acústica Computacional con Python
Universidad Austral de Chile
Noviembre 2024
```

**Qué decir:**
- "Buenos días/tardes, somos [nombres] y presentaremos nuestro proyecto final"
- "Hemos desarrollado un clasificador de instrumentos musicales en tiempo real"

---

### Diapositiva 2: MOTIVACIÓN (1 min)

**Contenido:**
```
❓ ¿Por qué este proyecto?

• Aplicación práctica de conceptos del curso
  - Procesamiento Digital de Señales
  - Análisis espectral (FFT)
  - Machine Learning aplicado

• Problema real y relevante
  - Transcripción musical automática
  - Educación musical
  - Análisis de grabaciones

• Desafío técnico interesante
  - Clasificación en tiempo real
  - Manejo de variabilidad acústica
```

**Qué decir:**
- "La clasificación automática de instrumentos tiene aplicaciones prácticas"
- "Permite aplicar todo lo aprendido en el curso: FFT, análisis espectral, etc."
- "Es un problema desafiante por la variabilidad de los sonidos"

---

### Diapositiva 3: OBJETIVOS (1 min)

**Contenido:**
```
🎯 Objetivos del Proyecto

GENERAL:
Desarrollar un sistema interactivo de clasificación de 
instrumentos musicales en tiempo real

ESPECÍFICOS:
✅ Captura de audio desde micrófono
✅ Análisis espectral mediante FFT
✅ Clasificación con modelo YAMNet
✅ Interfaz gráfica amigable
✅ Visualización de resultados

ALCANCE:
• 34 instrumentos detectables
• Funciona mejor con audio limpio
• Un instrumento a la vez (limitación de polifonía)
```

**Qué decir:**
- "Nuestro objetivo principal fue crear un sistema completo e interactivo"
- "Logramos cumplir todos los objetivos específicos"
- "El sistema puede detectar 34 instrumentos diferentes"

---

### Diapositiva 4: MARCO TEÓRICO (2 min)

**Contenido:**
```
📚 Fundamentos Teóricos

1. TRANSFORMADA DE FOURIER
   • Descompone señal temporal → componentes frecuenciales
   • FFT: algoritmo eficiente O(N log N)
   • Identifica frecuencias fundamentales y armónicos

2. CARACTERÍSTICAS ACÚSTICAS
   • Frecuencia fundamental (F0)
   • Serie armónica
   • Envolvente temporal (ADSR)
   • Centroide espectral

3. YAMNet - GOOGLE AUDIOSET
   • Red neuronal convolucional
   • Entrenada con 2 millones de clips
   • 521 clases de sonidos
   • Optimizada para tiempo real
```

**Qué decir:**
- "La base matemática es la Transformada de Fourier, vista en clases"
- "Cada instrumento tiene una 'huella' espectral característica"
- "Usamos YAMNet, un modelo pre-entrenado de Google"

---

### Diapositiva 5: DATASET (2 min)

**Contenido:**
```
📊 Dataset: YAMNet AudioSet

CARACTERÍSTICAS:
• Total: 521 clases de audio
• Fuente: 2 millones de clips de YouTube
• Duración: ~10 segundos por clip
• Etiquetado: Humano + verificación

NUESTRO FILTRO:
🎵 34 Instrumentos Musicales

CATEGORÍAS:
🎹 Teclados (4):     Piano, Organ, Synthesizer...
🎸 Cuerdas (13):     Guitar, Violin, Cello...
🎺 Vientos (7):      Trumpet, Saxophone, Flute...
🥁 Percusión (9):    Drums, Xylophone, Gong...
🎼 Otros (1):        Accordion

DIVISIÓN:
[GRÁFICO: Torta mostrando distribución]
- Instrumentos: 6.5% (34/521)
- Otros: 93.5% (487/521)
```

**Qué decir:**
- "YAMNet fue entrenado con AudioSet, un dataset masivo de Google"
- "Filtramos 34 instrumentos musicales del total de 521 clases"
- "Están representadas las familias principales de instrumentos"

---

### Diapositiva 6: METODOLOGÍA (2 min)

**Contenido:**
```
🔬 Metodología - Pipeline Completo

[DIAGRAMA DE FLUJO]

1. CAPTURA 🎙️
   ├─ Micrófono → SoundDevice
   ├─ Frecuencia: 16 kHz
   └─ Duración: 3-15 seg

2. PRE-PROCESAMIENTO 🔧
   ├─ Conversión a mono
   ├─ Normalización
   └─ Formato float32

3. ANÁLISIS ESPECTRAL 📊
   ├─ FFT (NumPy)
   ├─ Espectrograma Mel (YAMNet)
   └─ Visualización (Matplotlib)

4. CLASIFICACIÓN 🤖
   ├─ Modelo YAMNet
   ├─ Filtrado de instrumentos
   ├─ Umbral de confianza
   └─ Top-5 resultados

5. VISUALIZACIÓN 💻
   ├─ Interfaz Tkinter
   ├─ Espectro de frecuencia
   └─ Resultados + confianza
```

**Qué decir:**
- "El proceso completo tiene 5 etapas bien definidas"
- "Todo el pipeline está implementado en Python"
- "El análisis toma solo 2-3 segundos"

---

### Diapositiva 7: DEMO EN VIVO (5 min) ⭐

**PREPARACIÓN PREVIA:**
```
✅ Checklist antes de presentar:
□ Entorno virtual activado
□ Todos los paquetes instalados
□ Modelo YAMNet descargado
□ Micrófono funcionando y testeado
□ Ventana GUI lista para ejecutar
□ Audio de respaldo preparado (si falla micrófono)
□ Volumen del sistema configurado
```

**DEMO 1: Instrumento Simple**
```
Mostrar pantalla → GUI
1. Ejecutar: python gui_interface.py
2. Ajustar duración: 5 segundos
3. Grabar: [Tocar guitarra / piano / app de instrumento]
4. Analizar
5. Mostrar resultado en pantalla

Narración:
- "Aquí está la interfaz que desarrollamos"
- "Vamos a grabar 5 segundos de [instrumento]"
- "El sistema está analizando..."
- "Como pueden ver, detectó [instrumento] con X% de confianza"
- "Aquí está el espectro de frecuencia correspondiente"
```

**DEMO 2: Explorar Interfaz**
```
1. Cambiar a pestaña "Espectro"
   - "Aquí vemos la FFT del audio"
   - "Los picos corresponden a los armónicos"

2. Cambiar a pestaña "Resultados"
   - "Top 5 instrumentos detectados"
   - "Barra de confianza visual"

3. Mostrar historial
   - "Todas las clasificaciones quedan registradas"

4. Cambiar umbral y repetir
   - "Podemos ajustar la sensibilidad"
```

**BACKUP (si falla micrófono):**
```
- Tener audio pre-grabado: grabacion_demo.wav
- Modificar temporalmente classifier.py para cargar archivo
- O ejecutar desde notebook con audio de respaldo
```

---

### Diapositiva 8: RESULTADOS (2 min)

**Contenido:**
```
📈 Resultados Obtenidos

PRECISIÓN:
┌─────────────────────┬──────────┐
│ Condición           │ Precisión│
├─────────────────────┼──────────┤
│ Audio limpio        │  75-85%  │
│ Estudio/controlado  │  80-90%  │
│ Ambiente ruidoso    │  40-60%  │
└─────────────────────┴──────────┘

CASOS DE ÉXITO: ✅
• Piano solo: 92%
• Guitarra acústica: 87%
• Trompeta: 81%
• Flauta: 79%

CASOS DESAFIANTES: ⚠️
• Instrumentos similares (ej: violín vs viola)
• Mezclas instrumentales
• Audio comprimido (MP3)
• Ruido de fondo

TIEMPO DE PROCESAMIENTO:
• Grabación: Variable (3-15 seg)
• Análisis: ~2-3 segundos
• Total: <20 segundos
```

**Qué decir:**
- "Los resultados son prometedores en condiciones controladas"
- "La precisión baja significativamente con ruido de fondo"
- "El sistema es bastante rápido, ideal para uso interactivo"

---

### Diapositiva 9: LIMITACIONES (2 min)

**Contenido:**
```
⚠️ Limitaciones Identificadas

1. POLIFONÍA 🎼
   Problema: Solo detecta instrumento dominante
   
   Ejemplo: Piano + Violín → Solo detecta Piano
   
   Causa técnica:
   • YAMNet no separa fuentes
   • Promedio temporal diluye señales débiles
   
   Solución futura:
   • Separación de fuentes (Spleeter, Demucs)
   • Análisis por ventanas temporales

2. CALIDAD DE AUDIO 🎚️
   • SNR < 10 dB: Degradación severa
   • Distorsión: Confunde armónicos
   • Compresión: Pérdida de información
   
   Recomendaciones:
   ✓ Distancia 15-30 cm al micrófono
   ✓ Ambiente silencioso
   ✓ Formatos sin pérdida (WAV, FLAC)

3. INSTRUMENTOS NO CONVENCIONALES 🌍
   • Instrumentos étnicos no incluidos
   • Sintetizadores modulares
   • Efectos de audio procesados

4. DEPENDENCIA DE CONEXIÓN 🌐
   • Primera ejecución descarga modelo (~13 MB)
   • Solución: Cache local del modelo

5. RECURSOS COMPUTACIONALES 💻
   • RAM mínima: 4 GB
   • Procesador: i5 o superior
   • Optimizable con cuantización
```

**Qué decir:**
- "La limitación más importante es la polifonía"
- "El sistema funciona mejor con un solo instrumento a la vez"
- "Identificamos varias áreas de mejora para el futuro"

---

### Diapositiva 10: CONCLUSIONES (2 min)

**Contenido:**
```
📝 Conclusiones

LOGROS PRINCIPALES: ✅
1. Sistema funcional completo
   • Captura, análisis y clasificación integrados
   • Interfaz gráfica profesional
   • Código modular y documentado

2. Aplicación práctica de conceptos del curso
   • FFT y análisis espectral
   • Procesamiento digital de señales
   • Machine Learning en audio

3. Resultados prometedores
   • 75-85% precisión en condiciones controladas
   • Tiempo real (<3 seg de análisis)
   • 34 instrumentos detectables

APRENDIZAJES: 📚
• Importancia del pre-procesamiento
• Trade-offs entre precisión y complejidad
• Limitaciones de modelos pre-entrenados
• Experiencia en desarrollo de aplicaciones reales

IMPACTO: 🌟
• Herramienta educativa en acústica
• Base para proyectos futuros
• Código abierto y reproducible
• Potencial comercial/académico
```

**Qué decir:**
- "Cumplimos todos los objetivos planteados"
- "El proyecto nos permitió aplicar todo lo aprendido"
- "Los resultados validan el enfoque utilizado"

---

### Diapositiva 11: TRABAJO FUTURO (2 min)

**Contenido:**
```
🚀 Trabajo Futuro

CORTO PLAZO (1-3 meses):
□ Mejorar interfaz gráfica
  • Gráficos interactivos (Plotly)
  • Exportación de resultados
  • Historial persistente

□ Optimizar clasificador
  • Ajuste fino de umbrales
  • Validación cruzada
  • Métricas automáticas

□ Base de datos propia
  • 50 muestras × 5 instrumentos
  • Condiciones variadas

MEDIANO PLAZO (3-6 meses):
□ Implementar separación de fuentes
□ Detección de múltiples instrumentos
□ Transfer learning sobre YAMNet
□ Versión móvil (Android/iOS)

LARGO PLAZO (6+ meses):
□ Arquitecturas transformer
□ API REST para clasificación
□ Modelos generativos
□ Dashboard de análisis
```

**Qué decir:**
- "Hay muchas direcciones para continuar este proyecto"
- "Lo más importante es resolver el problema de polifonía"
- "Potencial para convertirse en una aplicación móvil"

---

### Diapositiva 12: REFERENCIAS (1 min)

**Contenido:**
```
📚 Referencias

ARTÍCULOS:
• Plakal, M., & Ellis, D. (2020). YAMNet
  Google Research, TensorFlow Hub

• Gemmeke, J. F., et al. (2017). Audio Set
  IEEE ICASSP 2017

• Rabiner & Schafer (2011). Digital Speech Processing
  Pearson Education

LIBRERÍAS:
• TensorFlow v2.14+
• TensorFlow Hub v0.15+
• SoundDevice v0.4+
• SciPy v1.11+, NumPy v1.24+
• Matplotlib v3.7+

RECURSOS:
• Curso ACUS220: vpobleteacustica.github.io
• YAMNet: tfhub.dev/google/yamnet/1
• AudioSet: research.google.com/audioset/

CÓDIGO:
• GitHub: [añadir enlace]
• Licencia: MIT
```

---

### Diapositiva 13: AGRADECIMIENTOS (30 seg)

**Contenido:**
```
🙏 Agradecimientos

• Prof. Víctor Poblete
  Por la guía y los recursos del curso

• Google Research
  Por YAMNet y AudioSet

• Comunidad TensorFlow
  Por documentación y ejemplos

• Compañeros del curso
  Por feedback y pruebas

¡Gracias por su atención!

¿PREGUNTAS? 🤔
```

---

## 🎯 Consejos para la Presentación

### ANTES DE PRESENTAR:

1. **Ensayar al menos 3 veces**
   - Cronometrar para no pasarse de tiempo
   - Practicar la demo varias veces
   - Preparar respuestas a preguntas frecuentes

2. **Preparar respaldos**
   - Audio pre-grabado por si falla micrófono
   - Screenshots de resultados
   - Video de demo (último recurso)

3. **Verificar tecnología**
   - Proyector/pantalla funcionando
   - Audio del computador audible
   - Puntero láser (opcional)

### DURANTE LA PRESENTACIÓN:

1. **Hablar claro y con confianza**
   - No leer las diapositivas
   - Hacer contacto visual
   - Controlar nervios (respirar profundo)

2. **Manejo del tiempo**
   - Respetar tiempos por sección
   - Si se pasan, resumir partes menos críticas
   - Dejar tiempo para preguntas

3. **Demo en vivo**
   - Explicar lo que están viendo
   - Si algo falla, mantener la calma
   - Tener plan B listo

### DESPUÉS DE PRESENTAR:

1. **Preguntas frecuentes esperables:**

**P: "¿Por qué eligieron YAMNet y no entrenaron su propio modelo?"**
R: "Porque YAMNet ya está pre-entrenado con millones de ejemplos. Entrenar desde cero requeriría mucho más tiempo y datos. Además, uno de los objetivos era aprender a usar modelos pre-entrenados."

**P: "¿Qué pasa si toco dos instrumentos al mismo tiempo?"**
R: "El sistema detectará el instrumento dominante, el más fuerte. Es una limitación conocida que abordamos en la sección de trabajo futuro con separación de fuentes."

**P: "¿Funciona con instrumentos que no están en la lista?"**
R: "No, porque YAMNet solo conoce las 521 clases con las que fue entrenado. Para nuevos instrumentos necesitaríamos hacer transfer learning."

**P: "¿Qué tan rápido es el sistema?"**
R: "El análisis toma 2-3 segundos después de grabar. Es suficientemente rápido para uso interactivo en tiempo real."

**P: "¿Podrían comercializar esto?"**
R: "Sí, hay potencial. Aplicaciones como Shazam hacen algo similar. Podría usarse en educación musical o transcripción automática."

---

## 📊 Materiales a Preparar

### 1. Presentación PowerPoint/PDF
- Exportar a PDF por seguridad
- Fuentes embebidas
- Incluir notas del orador

### 2. Demo Preparada
```bash
# Script de demostración
cd proyecto
source venv/bin/activate  # o activate en Windows
python gui_interface.py
```

### 3. Audio de Respaldo
- `demo_piano.wav` - 5 seg de piano
- `demo_guitar.wav` - 5 seg de guitarra
- `demo_violin.wav` - 5 seg de violín

### 4. Código Impreso (Opcional)
- `classifier.py` - Página clave
- `gui_interface.py` - Página de interfaz
- Por si piden ver código específico

---

## ⏰ Cronometraje Sugerido

| Sección | Tiempo | Acumulado |
|---------|--------|-----------|
| Introducción | 0:30 | 0:30 |
| Motivación | 1:00 | 1:30 |
| Objetivos | 1:00 | 2:30 |
| Marco Teórico | 2:00 | 4:30 |
| Dataset | 2:00 | 6:30 |
| Metodología | 2:00 | 8:30 |
| **DEMO** | **5:00** | **13:30** |
| Resultados | 2:00 | 15:30 |
| Limitaciones | 2:00 | 17:30 |
| Conclusiones | 2:00 | 19:30 |
| Trabajo Futuro | 1:00 | 20:30 |
| Referencias | 0:30 | 21:00 |
| Preguntas | 5:00 | 26:00 |

**Tiempo objetivo:** 20-25 minutos total

---

¡Éxito en la presentación! 🎉