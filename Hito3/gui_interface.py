"""
GUI Interface para Clasificador de Instrumentos Musicales
ACUS220 - Universidad Austral de Chile
Autores: Benjamin Martínez, Katherine Zapata

VERSIÓN CORREGIDA - Sin problemas de threading
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib
matplotlib.use('TkAgg')  # IMPORTANTE: Configurar backend antes de importar pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
import threading
import queue

# Importar módulos del proyecto
from recorder import grabar_audio
from analyzer import analizar_espectro
from classifier import predecir_instrumento

class InstrumentClassifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Clasificador de Instrumentos Musicales - ACUS220")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.recording = False
        self.last_audio_file = None
        self.history = []
        
        # Cola para comunicación thread-safe
        self.task_queue = queue.Queue()
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Iniciar verificación de cola
        self.check_queue()
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        
        # ============= TÍTULO =============
        title_frame = tk.Frame(self.root, bg='#2C3E50', height=80)
        title_frame.pack(fill='x', padx=0, pady=0)
        
        title_label = tk.Label(title_frame,
                              text="🎵 Clasificador de Instrumentos Musicales",
                              font=('Arial', 20, 'bold'),
                              bg='#2C3E50',
                              fg='white')
        title_label.pack(pady=15)
        
        subtitle = tk.Label(title_frame,
                           text="ACUS220 - Universidad Austral de Chile",
                           font=('Arial', 10),
                           bg='#2C3E50',
                           fg='#ECF0F1')
        subtitle.pack()
        
        # ============= PANEL PRINCIPAL =============
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Columna izquierda: Controles
        left_panel = tk.Frame(main_frame, bg='white', relief='ridge', bd=2)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Columna derecha: Visualización
        right_panel = tk.Frame(main_frame, bg='white', relief='ridge', bd=2)
        right_panel.grid(row=0, column=1, sticky='nsew')
        
        # Configurar pesos de columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
        # ============= PANEL IZQUIERDO =============
        self.create_left_panel(left_panel)
        
        # ============= PANEL DERECHO =============
        self.create_right_panel(right_panel)
        
    def create_left_panel(self, parent):
        """Crear panel de controles"""
        
        # Título del panel
        controls_title = tk.Label(parent,
                                 text="⚙️ Panel de Control",
                                 font=('Arial', 14, 'bold'),
                                 bg='white')
        controls_title.pack(pady=15)
        
        # ===== CONFIGURACIÓN DE GRABACIÓN =====
        config_frame = tk.LabelFrame(parent,
                                     text="Configuración de Grabación",
                                     font=('Arial', 11, 'bold'),
                                     bg='white',
                                     padx=15,
                                     pady=10)
        config_frame.pack(fill='x', padx=15, pady=10)
        
        # Duración
        duration_frame = tk.Frame(config_frame, bg='white')
        duration_frame.pack(fill='x', pady=5)
        
        tk.Label(duration_frame,
                text="Duración (seg):",
                font=('Arial', 10),
                bg='white').pack(side='left')
        
        self.duration_var = tk.IntVar(value=7)
        duration_spinbox = tk.Spinbox(duration_frame,
                                      from_=3,
                                      to=10,
                                      textvariable=self.duration_var,
                                      width=10,
                                      font=('Arial', 10))
        duration_spinbox.pack(side='right')
        
        # Umbral de confianza
        threshold_frame = tk.Frame(config_frame, bg='white')
        threshold_frame.pack(fill='x', pady=5)
        
        tk.Label(threshold_frame,
                text="Umbral confianza:",
                font=('Arial', 10),
                bg='white').pack(side='left')
        
        self.threshold_var = tk.DoubleVar(value=0.025)
        threshold_spinbox = tk.Spinbox(threshold_frame,
                                       from_=0.01,
                                       to=0.5,
                                       increment=0.005,
                                       textvariable=self.threshold_var,
                                       width=10,
                                       font=('Arial', 10),
                                       format="%.3f")
        threshold_spinbox.pack(side='right')
        
        # ===== BOTONES DE ACCIÓN =====
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill='x', padx=15, pady=20)
        
        # Botón Grabar
        self.record_button = tk.Button(buttons_frame,
                                       text="🎙️ GRABAR AUDIO",
                                       command=self.start_recording,
                                       font=('Arial', 12, 'bold'),
                                       bg='#4CAF50',
                                       fg='white',
                                       activebackground='#45a049',
                                       height=2,
                                       cursor='hand2')
        self.record_button.pack(fill='x', pady=5)
        
        # Botón Analizar
        self.analyze_button = tk.Button(buttons_frame,
                                        text="📊 ANALIZAR",
                                        command=self.analyze_audio,
                                        font=('Arial', 12, 'bold'),
                                        bg='#2196F3',
                                        fg='white',
                                        activebackground='#0b7dda',
                                        height=2,
                                        cursor='hand2',
                                        state='disabled')
        self.analyze_button.pack(fill='x', pady=5)
        
        # Botón Limpiar
        clear_button = tk.Button(buttons_frame,
                                text="🗑️ Limpiar Historial",
                                command=self.clear_history,
                                font=('Arial', 10),
                                bg='#f44336',
                                fg='white',
                                activebackground='#da190b',
                                cursor='hand2')
        clear_button.pack(fill='x', pady=5)
        
        # ===== BARRA DE ESTADO =====
        status_frame = tk.LabelFrame(parent,
                                     text="Estado",
                                     font=('Arial', 11, 'bold'),
                                     bg='white',
                                     padx=10,
                                     pady=10)
        status_frame.pack(fill='x', padx=15, pady=10)
        
        self.status_label = tk.Label(status_frame,
                                     text="💤 Esperando...",
                                     font=('Arial', 10),
                                     bg='white',
                                     fg='#666',
                                     wraplength=250,
                                     justify='left')
        self.status_label.pack()
        
        # ===== HISTORIAL =====
        history_frame = tk.LabelFrame(parent,
                                      text="📋 Historial de Clasificaciones",
                                      font=('Arial', 11, 'bold'),
                                      bg='white',
                                      padx=10,
                                      pady=10)
        history_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Lista con scrollbar
        list_frame = tk.Frame(history_frame, bg='white')
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox = tk.Listbox(list_frame,
                                          yscrollcommand=scrollbar.set,
                                          font=('Courier', 9),
                                          bg='#f9f9f9',
                                          selectmode='single')
        self.history_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
    def create_right_panel(self, parent):
        """Crear panel de visualización"""
        
        # Título
        viz_title = tk.Label(parent,
                            text="📈 Visualización y Resultados",
                            font=('Arial', 14, 'bold'),
                            bg='white')
        viz_title.pack(pady=15)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ===== PESTAÑA 1: ESPECTRO =====
        spectrum_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(spectrum_frame, text='🌊 Espectro de Frecuencia')
        
        # Crear figura de matplotlib
        self.fig_spectrum, self.ax_spectrum = plt.subplots(figsize=(8, 5), dpi=80)
        self.ax_spectrum.set_title('Espectro de Frecuencia', fontsize=12, fontweight='bold')
        self.ax_spectrum.set_xlabel('Frecuencia (Hz)', fontsize=10)
        self.ax_spectrum.set_ylabel('Magnitud', fontsize=10)
        self.ax_spectrum.grid(True, alpha=0.3)
        
        self.canvas_spectrum = FigureCanvasTkAgg(self.fig_spectrum, spectrum_frame)
        self.canvas_spectrum.get_tk_widget().pack(fill='both', expand=True)
        
        # ===== PESTAÑA 2: RESULTADOS =====
        results_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(results_frame, text='🎯 Resultados')
        
        # Resultado principal
        self.result_display = tk.Label(results_frame,
                                       text="Sin resultados aún",
                                       font=('Arial', 18, 'bold'),
                                       bg='white',
                                       fg='#333',
                                       pady=30)
        self.result_display.pack()
        
        # Confianza
        self.confidence_label = tk.Label(results_frame,
                                         text="",
                                         font=('Arial', 14),
                                         bg='white',
                                         fg='#666')
        self.confidence_label.pack(pady=10)
        
        # Barra de progreso de confianza
        self.confidence_progress = ttk.Progressbar(results_frame,
                                                    length=400,
                                                    mode='determinate',
                                                    maximum=100)
        self.confidence_progress.pack(pady=10)
        
        # Top 5 instrumentos
        top5_frame = tk.LabelFrame(results_frame,
                                   text="Top 5 Instrumentos Detectados",
                                   font=('Arial', 11, 'bold'),
                                   bg='white',
                                   padx=20,
                                   pady=15)
        top5_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        self.top5_text = scrolledtext.ScrolledText(top5_frame,
                                                    height=10,
                                                    font=('Courier', 11),
                                                    bg='#f9f9f9',
                                                    wrap='word')
        self.top5_text.pack(fill='both', expand=True)
        
        # ===== PESTAÑA 3: INFORMACIÓN =====
        info_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(info_frame, text='ℹ️ Información')
        
        info_text = scrolledtext.ScrolledText(info_frame,
                                               font=('Arial', 10),
                                               wrap='word',
                                               bg='white',
                                               padx=10,
                                               pady=10)
        info_text.pack(fill='both', expand=True)
        
        info_content = """
🎵 CLASIFICADOR DE INSTRUMENTOS MUSICALES
==========================================

📚 Información del Proyecto:
• Curso: ACUS220 - Acústica Computacional con Python
• Universidad Austral de Chile
• Autores: Benjamin Martínez, Katherine Zapata

🔬 Tecnología Utilizada:
• Modelo: YAMNet (Google AudioSet)
• Análisis: Transformada Rápida de Fourier (FFT)
• Framework: TensorFlow + TensorFlow Hub

🎯 Instrumentos Detectables (34):
══════════════════════════════════

🎹 Teclados: Piano, Electric Piano, Organ, Synthesizer
🎸 Cuerdas: Guitar, Electric Guitar, Bass Guitar, Violin, Cello, etc.
🎺 Vientos: Trumpet, Trombone, Saxophone, Flute, Clarinet, etc.
🥁 Percusión: Drum Kit, Snare Drum, Xylophone, Gong, etc.

📊 Cómo Usar:
1. Ajusta la duración de grabación (3-15 seg)
2. Configura el umbral de confianza (0.01-0.5)
3. Presiona "GRABAR AUDIO"
4. Toca o reproduce el instrumento
5. Espera a que termine la grabación
6. Presiona "ANALIZAR"
7. Revisa los resultados en las pestañas

⚠️ Limitaciones:
• Funciona mejor con un solo instrumento
• Ambiente con poco ruido de fondo
• Audio claro y sin distorsión
• Polifonía limitada

💡 Consejos:
• Graba a 15-30 cm del micrófono
• Evita ruidos de fondo
• Toca notas sostenidas
• Si no detecta, aumenta el volumen
        """
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
        
    def check_queue(self):
        """Verificar cola de tareas periódicamente"""
        try:
            while True:
                task = self.task_queue.get_nowait()
                task()
        except queue.Empty:
            pass
        
        # Verificar nuevamente en 100ms
        self.root.after(100, self.check_queue)
        
    def update_status(self, message, color='#666'):
        """Actualizar mensaje de estado (thread-safe)"""
        def _update():
            self.status_label.config(text=message, fg=color)
        self.task_queue.put(_update)
        
    def start_recording(self):
        """Iniciar grabación de audio"""
        if self.recording:
            return
            
        self.recording = True
        self.record_button.config(state='disabled', bg='#999')
        self.analyze_button.config(state='disabled')
        
        duration = self.duration_var.get()
        self.update_status(f"🎙️ Grabando {duration} segundos...", '#FF5722')
        
        # Ejecutar grabación en thread separado
        thread = threading.Thread(target=self._record_thread, args=(duration,), daemon=True)
        thread.start()
        
    def _record_thread(self, duration):
        """Thread de grabación"""
        try:
            # Grabar audio
            self.last_audio_file = grabar_audio(duracion=duration)
            
            # Actualizar UI (thread-safe)
            self.task_queue.put(self._recording_complete)
            
        except Exception as e:
            self.task_queue.put(lambda: self._recording_error(str(e)))
            
    def _recording_complete(self):
        """Callback cuando termina la grabación"""
        self.recording = False
        self.record_button.config(state='normal', bg='#4CAF50')
        self.analyze_button.config(state='normal')
        self.update_status("✅ Grabación completa. Presiona ANALIZAR", '#4CAF50')
        
    def _recording_error(self, error):
        """Callback cuando hay error en grabación"""
        self.recording = False
        self.record_button.config(state='normal', bg='#4CAF50')
        self.update_status(f"❌ Error: {error}", '#f44336')
        messagebox.showerror("Error de Grabación", f"No se pudo grabar el audio:\n{error}")
        
    def analyze_audio(self):
        """Analizar audio grabado"""
        if not self.last_audio_file:
            messagebox.showwarning("Sin Audio", "Primero debes grabar un audio")
            return
            
        self.analyze_button.config(state='disabled')
        self.update_status("🔍 Analizando audio...", '#2196F3')
        
        # Ejecutar análisis en thread
        thread = threading.Thread(target=self._analyze_thread, daemon=True)
        thread.start()
        
    def _analyze_thread(self):
        """Thread de análisis"""
        try:
            # Analizar espectro
            from scipy.io import wavfile
            fs, audio_data = wavfile.read(self.last_audio_file)
            audio_data = audio_data.flatten()
            N = len(audio_data)
            fft_vals = np.fft.fft(audio_data)
            freqs = np.fft.fftfreq(N, 1/fs)
            
            # Solo frecuencias positivas
            idx_pos = freqs > 0
            freqs_pos = freqs[idx_pos]
            magnitud = np.abs(fft_vals[idx_pos])
            
            # Clasificar instrumento
            threshold = self.threshold_var.get()
            resultado = predecir_instrumento(self.last_audio_file, umbral_confianza=threshold)
            
            # Actualizar UI (thread-safe)
            self.task_queue.put(lambda: self._update_results(magnitud, freqs_pos, resultado))
            
        except Exception as e:
            self.task_queue.put(lambda: self._analysis_error(str(e)))
            
    def _update_results(self, magnitud, freqs, resultado):
        """Actualizar resultados en la interfaz"""
        # Actualizar espectro
        self.ax_spectrum.clear()
        self.ax_spectrum.plot(freqs, magnitud, color='#2196F3', linewidth=1.5)
        self.ax_spectrum.set_title('Espectro de Frecuencia', fontsize=12, fontweight='bold')
        self.ax_spectrum.set_xlabel('Frecuencia (Hz)', fontsize=10)
        self.ax_spectrum.set_ylabel('Magnitud', fontsize=10)
        self.ax_spectrum.set_xlim([0, 8000])
        self.ax_spectrum.grid(True, alpha=0.3)
        self.canvas_spectrum.draw()
        
        # Actualizar resultados
        if resultado is None:
            self.result_display.config(
                text="❓ No se detectó instrumento",
                fg='#999'
            )
            self.confidence_label.config(text="Confianza insuficiente")
            self.confidence_progress['value'] = 0
            self.top5_text.delete('1.0', 'end')
            self.top5_text.insert('1.0', "No se detectaron instrumentos válidos.\n\n"
                                         "Posibles causas:\n"
                                         "• Volumen muy bajo\n"
                                         "• Ruido de fondo\n"
                                         "• Instrumento no incluido en el modelo")
        else:
            nombre, confianza = resultado
            
            self.result_display.config(
                text=f"🎵 {nombre.upper()}",
                fg='#4CAF50'
            )
            
            confidence_pct = confianza * 100
            self.confidence_label.config(
                text=f"Confianza: {confidence_pct:.1f}%"
            )
            self.confidence_progress['value'] = confidence_pct
            
            # Agregar al historial
            timestamp = datetime.now().strftime("%H:%M:%S")
            entry = f"{timestamp} | {nombre} ({confidence_pct:.1f}%)"
            self.history.append(entry)
            self.history_listbox.insert(0, entry)
            
            # Actualizar top 5
            self.top5_text.delete('1.0', 'end')
            self.top5_text.insert('1.0', f"1. {nombre}\n   Confianza: {confidence_pct:.2f}%\n\n"
                                         f"(Top 5 completo disponible en consola)")
        
        # Cambiar a pestaña de resultados
        self.notebook.select(1)
        
        # Actualizar estado
        self.analyze_button.config(state='normal')
        self.update_status("✅ Análisis completo", '#4CAF50')
        
    def _analysis_error(self, error):
        """Callback cuando hay error en análisis"""
        self.analyze_button.config(state='normal')
        self.update_status(f"❌ Error en análisis: {error}", '#f44336')
        messagebox.showerror("Error de Análisis", f"No se pudo analizar el audio:\n{error}")
        
    def clear_history(self):
        """Limpiar historial"""
        if messagebox.askyesno("Confirmar", "¿Limpiar todo el historial?"):
            self.history.clear()
            self.history_listbox.delete(0, 'end')
            self.update_status("🗑️ Historial limpiado", '#FF9800')

def main():
    """Función principal"""
    root = tk.Tk()
    app = InstrumentClassifierGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()