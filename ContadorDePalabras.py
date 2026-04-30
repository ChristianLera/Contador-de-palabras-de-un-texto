import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from collections import Counter
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from langdetect import detect, DetectorFactory
from textblob import TextBlob
import numpy as np

DetectorFactory.seed = 0

class ContadorPalabrasAvanzado:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Analizador de Textos")
        self.root.geometry("900x1200")
        
        # 🎨 PALETA CLÁSICA LIMPIA (Estilo Word/Google Docs)
        self.colores = {
            "bg_principal": "#f0f0f0",       # Gris claro clásico
            "bg_frame": "#ffffff",           # Blanco
            "bg_texto": "#ffffff",           # Blanco para texto
            "texto_principal": "#333333",    # Negro suave
            "texto_secundario": "#666666",   # Gris medio
            "acento": "#2c3e50",             # Gris oscuro elegante
            "acento_hover": "#1a252f",       # Gris más oscuro
            "boton_secundario": "#bdc3c7",   # Gris plata
            "border": "#dcdde1",             # Gris borde suave
            "exito": "#27ae60",              # Verde para éxito
            "advertencia": "#e67e22"         # Naranja para advertencias
        }
        
        self.root.configure(bg=self.colores["bg_principal"])
        
        # Variables para comparar textos
        self.texto1 = None
        self.texto2 = None
        self.modo_comparacion = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_container = tk.Frame(self.root, bg=self.colores["bg_principal"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Canvas con scroll para toda la interfaz
        canvas = tk.Canvas(main_container, bg=self.colores["bg_principal"], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.colores["bg_principal"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        titulo_frame = tk.Frame(self.scrollable_frame, bg=self.colores["bg_principal"])
        titulo_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = tk.Label(
            titulo_frame,
            text="🔬 ANALIZADOR DE TEXTOS",
            font=("Segoe UI", 18, "bold"),
            bg=self.colores["bg_principal"],
            fg=self.colores["texto_principal"]
        )
        titulo.pack()
        
        subtitulo = tk.Label(
            titulo_frame,
            text="Análisis completo de métricas, estadísticas y comparación de textos",
            font=("Segoe UI", 10),
            bg=self.colores["bg_principal"],
            fg=self.colores["texto_secundario"]
        )
        subtitulo.pack()
        
        # Frame para selector de modo
        frame_modo = tk.Frame(self.scrollable_frame, bg=self.colores["bg_principal"])
        frame_modo.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            frame_modo,
            text="Modo de análisis:",
            font=("Segoe UI", 10),
            bg=self.colores["bg_principal"],
            fg=self.colores["texto_principal"]
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.modo_var = tk.StringVar(value="simple")
        
        # Radiobuttons personalizados
        rb_simple = tk.Radiobutton(
            frame_modo, text="📝 Texto Único", variable=self.modo_var,
            value="simple", bg=self.colores["bg_principal"],
            fg=self.colores["texto_principal"],
            selectcolor=self.colores["bg_frame"],
            activebackground=self.colores["bg_principal"],
            command=self.cambiar_modo
        )
        rb_simple.pack(side=tk.LEFT, padx=(0, 15))
        
        rb_comparar = tk.Radiobutton(
            frame_modo, text="🔄 Comparar Textos", variable=self.modo_var,
            value="comparar", bg=self.colores["bg_principal"],
            fg=self.colores["texto_principal"],
            selectcolor=self.colores["bg_frame"],
            activebackground=self.colores["bg_principal"],
            command=self.cambiar_modo
        )
        rb_comparar.pack(side=tk.LEFT)
        
        # Frame para áreas de texto
        self.frame_textos = tk.Frame(self.scrollable_frame, bg=self.colores["bg_principal"])
        self.frame_textos.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Área de texto simple
        self.frame_simple = tk.Frame(self.frame_textos, bg=self.colores["bg_principal"])
        
        # Label para texto simple
        tk.Label(
            self.frame_simple,
            text="Ingrese su texto:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colores["bg_principal"],
            fg=self.colores["texto_principal"],
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))
        
        self.texto_area = scrolledtext.ScrolledText(
            self.frame_simple,
            wrap=tk.WORD,
            width=50,
            height=12,
            font=("Consolas", 10),
            bg=self.colores["bg_texto"],
            fg=self.colores["texto_principal"],
            insertbackground=self.colores["texto_principal"],
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightcolor=self.colores["acento"],
            highlightbackground=self.colores["border"]
        )
        self.texto_area.pack(fill=tk.BOTH, expand=True)
        self.texto_area.insert("1.0", "Escribe o pega tu texto aquí...")
        self.texto_area.bind("<FocusIn>", self.limpiar_placeholder)
        self.frame_simple.pack(fill=tk.BOTH, expand=True)
        
        # Frame para comparación (inicialmente oculto)
        self.frame_comparacion = tk.Frame(self.frame_textos, bg=self.colores["bg_principal"])
        
        # Texto 1
        frame_texto1 = tk.Frame(self.frame_comparacion, bg=self.colores["bg_principal"])
        frame_texto1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            frame_texto1,
            text="📄 Texto 1:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colores["bg_principal"],
            fg=self.colores["texto_principal"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.texto_area1 = scrolledtext.ScrolledText(
            frame_texto1,
            wrap=tk.WORD,
            width=45,
            height=12,
            font=("Consolas", 10),
            bg=self.colores["bg_texto"],
            fg=self.colores["texto_principal"],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.texto_area1.pack(fill=tk.BOTH, expand=True)
        
        # Texto 2
        frame_texto2 = tk.Frame(self.frame_comparacion, bg=self.colores["bg_principal"])
        frame_texto2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(
            frame_texto2,
            text="📄 Texto 2:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colores["bg_principal"],
            fg=self.colores["texto_principal"]
        ).pack(anchor="w", pady=(0, 5))
        
        self.texto_area2 = scrolledtext.ScrolledText(
            frame_texto2,
            wrap=tk.WORD,
            width=45,
            height=12,
            font=("Consolas", 10),
            bg=self.colores["bg_texto"],
            fg=self.colores["texto_principal"],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.texto_area2.pack(fill=tk.BOTH, expand=True)
        
        # Frame para botones
        frame_botones = tk.Frame(self.scrollable_frame, bg=self.colores["bg_principal"])
        frame_botones.pack(fill=tk.X, pady=(0, 15))
        
        self.boton_analizar = tk.Button(
            frame_botones,
            text="🔍 ANALIZAR TEXTO",
            font=("Segoe UI", 11, "bold"),
            bg=self.colores["acento"],
            fg="white",
            padx=25,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
            command=self.analizar_texto
        )
        self.boton_analizar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.boton_limpiar = tk.Button(
            frame_botones,
            text="🗑️ LIMPIAR TODO",
            font=("Segoe UI", 11),
            bg=self.colores["boton_secundario"],
            fg="white",
            padx=25,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
            command=self.limpiar_todo
        )
        self.boton_limpiar.pack(side=tk.LEFT)
        
        # Efectos hover
        self.boton_analizar.bind("<Enter>", lambda e: self.boton_analizar.config(bg=self.colores["acento_hover"]))
        self.boton_analizar.bind("<Leave>", lambda e: self.boton_analizar.config(bg=self.colores["acento"]))
        self.boton_limpiar.bind("<Enter>", lambda e: self.boton_limpiar.config(bg="#a0a0a0"))
        self.boton_limpiar.bind("<Leave>", lambda e: self.boton_limpiar.config(bg=self.colores["boton_secundario"]))
        
        # Notebook para resultados (pestañas)
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configurar estilo del notebook
        style = ttk.Style()
        style.configure("TNotebook", background=self.colores["bg_principal"])
        style.configure("TNotebook.Tab", padding=[10, 5], font=("Segoe UI", 10))
        
        # Pestaña de estadísticas
        self.frame_stats = tk.Frame(self.notebook, bg=self.colores["bg_frame"])
        self.notebook.add(self.frame_stats, text="📊 Estadísticas")
        
        # Pestaña de gráficos
        self.frame_graficos = tk.Frame(self.notebook, bg=self.colores["bg_frame"])
        self.notebook.add(self.frame_graficos, text="📈 Gráficos")
        
        # Pestaña de comparación (resultados)
        self.frame_comparacion_resultados = tk.Frame(self.notebook, bg=self.colores["bg_frame"])
        self.notebook.add(self.frame_comparacion_resultados, text="🔄 Comparación")
        
        # Configurar cada pestaña
        self.setup_stats_tab()
        self.setup_graficos_tab()
        self.setup_comparacion_tab()
        
        # Inicialmente deshabilitar pestaña de comparación
        self.notebook.tab(2, state="disabled")
        
    def setup_stats_tab(self):
        """Configurar pestaña de estadísticas avanzadas"""
        # Frame para métricas principales con grid
        frame_metricas = tk.Frame(self.frame_stats, bg=self.colores["bg_frame"])
        frame_metricas.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Configurar grid responsivo
        for i in range(2):
            frame_metricas.columnconfigure(i, weight=1)
        
        self.labels_stats = {}
        metricas = [
            ("📖 Palabras", "0"),
            ("✏️ Caracteres", "0"),
            ("🔄 Palabras únicas", "0"),
            ("📝 Oraciones", "0"),
            ("🔤 Sílabas totales", "0"),
            ("📊 Densidad léxica", "0%"),
            ("🌍 Idioma detectado", "---"),
            ("😊 Sentimiento", "---")
        ]
        
        for i, (nombre, valor) in enumerate(metricas):
            # Frame para cada métrica
            frame = tk.Frame(
                frame_metricas,
                bg=self.colores["bg_frame"],
                relief=tk.RIDGE,
                borderwidth=1,
                highlightbackground=self.colores["border"],
                highlightthickness=1
            )
            frame.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")
            
            # Título de la métrica
            tk.Label(
                frame,
                text=nombre,
                font=("Segoe UI", 10),
                bg=self.colores["bg_frame"],
                fg=self.colores["texto_secundario"]
            ).pack(pady=(12, 5))
            
            # Valor de la métrica
            label_valor = tk.Label(
                frame,
                text=valor,
                font=("Segoe UI", 18, "bold"),
                bg=self.colores["bg_frame"],
                fg=self.colores["acento"]
            )
            label_valor.pack(pady=(0, 12))
            self.labels_stats[nombre] = label_valor
        
        # Frame para palabras más comunes
        frame_comunes = tk.Frame(self.frame_stats, bg=self.colores["bg_frame"], relief=tk.RIDGE, borderwidth=1)
        frame_comunes.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        tk.Label(
            frame_comunes,
            text="⭐ PALABRAS MÁS COMUNES (Top 10)",
            font=("Segoe UI", 11, "bold"),
            bg=self.colores["bg_frame"],
            fg=self.colores["texto_principal"]
        ).pack(pady=(10, 5))
        
        # Frame para el Listbox con scroll
        listbox_frame = tk.Frame(frame_comunes, bg=self.colores["bg_frame"])
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.lista_comunes = tk.Listbox(
            listbox_frame,
            height=8,
            font=("Consolas", 10),
            bg=self.colores["bg_texto"],
            fg=self.colores["texto_principal"],
            relief=tk.FLAT,
            borderwidth=0,
            yscrollcommand=scrollbar.set
        )
        self.lista_comunes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lista_comunes.yview)
        
    def setup_graficos_tab(self):
        """Configurar pestaña de gráficos"""
        self.frame_grafico = tk.Frame(self.frame_graficos, bg=self.colores["bg_frame"])
        self.frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def setup_comparacion_tab(self):
        """Configurar pestaña de comparación de textos"""
        self.text_comparacion = scrolledtext.ScrolledText(
            self.frame_comparacion_resultados,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=self.colores["bg_texto"],
            fg=self.colores["texto_principal"],
            relief=tk.FLAT,
            borderwidth=0
        )
        self.text_comparacion.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def cambiar_modo(self):
        """Cambiar entre modo simple y comparación"""
        if self.modo_var.get() == "simple":
            self.frame_comparacion.pack_forget()
            self.frame_simple.pack(fill=tk.BOTH, expand=True)
            self.notebook.tab(2, state="disabled")
        else:
            self.frame_simple.pack_forget()
            self.frame_comparacion.pack(fill=tk.BOTH, expand=True)
            self.notebook.tab(2, state="normal")
            
    def limpiar_placeholder(self, event):
        if self.texto_area.get("1.0", "end-1c") == "Escribe o pega tu texto aquí...":
            self.texto_area.delete("1.0", tk.END)
            
    def contar_silabas(self, palabra):
        """Contar sílabas de una palabra (método simple)"""
        palabra = palabra.lower()
        contador = 0
        vocales = "aeiouáéíóúü"
        if len(palabra) == 0:
            return 0
        if palabra[0] in vocales:
            contador += 1
        for i in range(1, len(palabra)):
            if palabra[i] in vocales and palabra[i-1] not in vocales:
                contador += 1
        if palabra.endswith("e"):
            contador = max(1, contador - 1)
        return max(1, contador)
    
    def densidad_lexica(self, palabras_unicas, total_palabras):
        """Calcular densidad léxica (riqueza de vocabulario)"""
        if total_palabras == 0:
            return 0
        return (palabras_unicas / total_palabras) * 100
    
    def analizar_texto(self):
        """Análisis principal del texto"""
        if self.modo_var.get() == "simple":
            self.analizar_texto_simple()
        else:
            self.comparar_textos()
            
    def analizar_texto_simple(self):
        """Análisis completo del texto simple"""
        texto = self.texto_area.get("1.0", tk.END).strip()
        
        if not texto or texto == "Escribe o pega tu texto aquí...":
            messagebox.showinfo("Información", "Por favor, ingresa algún texto para analizar.")
            return
            
        # Limpiar texto
        texto_limpio = re.sub(r'[^\w\s]', '', texto)
        palabras = texto_limpio.lower().split()
        
        # Estadísticas básicas
        total_palabras = len(palabras)
        caracteres = len(re.sub(r'\s', '', texto))
        palabras_unicas = len(set(palabras))
        
        # Oraciones
        oraciones = re.split(r'[.!?]+', texto)
        total_oraciones = len([o for o in oraciones if o.strip()])
        
        # Sílabas
        total_silabas = sum(self.contar_silabas(p) for p in palabras)
        
        # Densidad léxica
        densidad = self.densidad_lexica(palabras_unicas, total_palabras)
        
        # Idioma
        try:
            idioma = detect(texto)
            nombres_idiomas = {
                'es': 'Español', 'en': 'Inglés', 'fr': 'Francés',
                'de': 'Alemán', 'it': 'Italiano', 'pt': 'Portugués'
            }
            idioma_detectado = nombres_idiomas.get(idioma, idioma)
        except:
            idioma_detectado = "No detectable"
            
        # Sentimiento
        try:
            blob = TextBlob(texto)
            polaridad = blob.sentiment.polarity
            if polaridad > 0.1:
                sentimiento = "😊 Positivo"
            elif polaridad < -0.1:
                sentimiento = "😞 Negativo"
            else:
                sentimiento = "😐 Neutral"
        except:
            sentimiento = "No disponible"
            
        # Palabras más comunes
        contador = Counter(palabras)
        palabras_comunes = contador.most_common(10)
        
        # Actualizar UI
        self.labels_stats["📖 Palabras"].config(text=str(total_palabras))
        self.labels_stats["✏️ Caracteres"].config(text=str(caracteres))
        self.labels_stats["🔄 Palabras únicas"].config(text=str(palabras_unicas))
        self.labels_stats["📝 Oraciones"].config(text=str(total_oraciones))
        self.labels_stats["🔤 Sílabas totales"].config(text=str(total_silabas))
        self.labels_stats["📊 Densidad léxica"].config(text=f"{densidad:.1f}%")
        self.labels_stats["🌍 Idioma detectado"].config(text=idioma_detectado)
        self.labels_stats["😊 Sentimiento"].config(text=sentimiento)
        
        # Actualizar lista de palabras comunes
        self.lista_comunes.delete(0, tk.END)
        for palabra, count in palabras_comunes:
            self.lista_comunes.insert(tk.END, f"{palabra} → {count} veces")
            
        # Generar gráfico
        self.generar_grafico(palabras_comunes[:8])
        
        messagebox.showinfo("Éxito", f"¡Análisis completado!\n\nTotal de palabras: {total_palabras}\nPalabras únicas: {palabras_unicas}\nIdioma detectado: {idioma_detectado}")
        
    def generar_grafico(self, palabras_comunes):
        """Generar gráfico de barras con matplotlib estilo profesional"""
        # Limpiar frame anterior
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
            
        if not palabras_comunes:
            return
            
        palabras = [p[0] for p in palabras_comunes]
        frecuencias = [p[1] for p in palabras_comunes]
        
        # Configurar estilo profesional
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(8, 4), facecolor=self.colores["bg_frame"])
        ax.set_facecolor(self.colores["bg_frame"])
        
        # Crear barras con gradiente de azules
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(palabras)))
        bars = ax.bar(palabras, frecuencias, color=colors, edgecolor=self.colores["acento"], linewidth=1.5)
        
        # Personalizar
        ax.set_xlabel('Palabras', fontsize=10, color=self.colores["texto_secundario"])
        ax.set_ylabel('Frecuencia', fontsize=10, color=self.colores["texto_secundario"])
        ax.set_title('Top 8 Palabras Más Frecuentes', fontsize=12, color=self.colores["texto_principal"], pad=15)
        ax.tick_params(colors=self.colores["texto_secundario"], rotation=45)
        
        # Configurar spines
        for spine in ax.spines.values():
            spine.set_color(self.colores["border"])
            spine.set_linewidth(0.5)
            
        # Añadir valores en las barras
        for bar, freq in zip(bars, frecuencias):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   str(freq), ha='center', va='bottom', 
                   color=self.colores["texto_principal"], fontsize=9, fontweight='bold')
            
        # Ajustar layout
        plt.tight_layout()
        
        # Mostrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def comparar_textos(self):
        """Comparar dos textos"""
        texto1 = self.texto_area1.get("1.0", tk.END).strip()
        texto2 = self.texto_area2.get("1.0", tk.END).strip()
        
        if not texto1 or not texto2:
            messagebox.showinfo("Información", "Por favor, ingresa ambos textos para comparar.")
            return
            
        # Limpiar y procesar
        limpio1 = re.sub(r'[^\w\s]', '', texto1).lower().split()
        limpio2 = re.sub(r'[^\w\s]', '', texto2).lower().split()
        
        set1 = set(limpio1)
        set2 = set(limpio2)
        
        palabras_comunes = set1 & set2
        palabras_solo_texto1 = set1 - set2
        palabras_solo_texto2 = set2 - set1
        
        # Similitud (coeficiente de Jaccard)
        jaccard = len(palabras_comunes) / len(set1 | set2) if set1 | set2 else 0
        
        # Mostrar resultados
        self.text_comparacion.delete("1.0", tk.END)
        
        # Crear texto formateado bonito
        resultado = f"""
╔════════════════════════════════════════════════════════════════════════╗
║                         COMPARACIÓN DE TEXTOS                           ║
╚════════════════════════════════════════════════════════════════════════╝

📊 ESTADÍSTICAS INDIVIDUALES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Texto 1: {len(limpio1):,} palabras, {len(set1):,} palabras únicas
  Texto 2: {len(limpio2):,} palabras, {len(set2):,} palabras únicas

🔄 SIMILITUD ENTRE TEXTOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Coeficiente de Jaccard: {jaccard:.2%}
  Palabras en común: {len(palabras_comunes):,}

📝 PALABRAS EXCLUSIVAS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Solo en Texto 1 ({len(palabras_solo_texto1)} palabras):
    {', '.join(list(palabras_solo_texto1)[:20])}
    {'...' if len(palabras_solo_texto1) > 20 else ''}

  Solo en Texto 2 ({len(palabras_solo_texto2)} palabras):
    {', '.join(list(palabras_solo_texto2)[:20])}
    {'...' if len(palabras_solo_texto2) > 20 else ''}

✨ PALABRAS EN COMÚN (Top 20):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {', '.join(list(palabras_comunes)[:20])}
  {'...' if len(palabras_comunes) > 20 else ''}

📈 ANÁLISIS DE SIMILITUD:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {'🟢 Alta similitud' if jaccard > 0.5 else '🟡 Similitud media' if jaccard > 0.3 else '🔴 Baja similitud'}
  Los textos {'comparten mucho vocabulario' if jaccard > 0.5 else 'tienen algunas similitudes' if jaccard > 0.3 else 'son muy diferentes en su vocabulario'}
"""
        
        self.text_comparacion.insert("1.0", resultado)
        
        # Cambiar a la pestaña de comparación
        self.notebook.select(2)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Comparación", f"Comparación completada\nSimilitud entre textos: {jaccard:.1%}")
        
    def limpiar_todo(self):
        """Limpiar todas las áreas de texto"""
        self.texto_area.delete("1.0", tk.END)
        self.texto_area.insert("1.0", "Escribe o pega tu texto aquí...")
        
        if hasattr(self, 'texto_area1'):
            self.texto_area1.delete("1.0", tk.END)
            self.texto_area2.delete("1.0", tk.END)
            
        # Resetear estadísticas
        for label in self.labels_stats.values():
            label.config(text="0")
        self.lista_comunes.delete(0, tk.END)
        
        # Limpiar gráfico
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
            
        # Limpiar comparación
        if hasattr(self, 'text_comparacion'):
            self.text_comparacion.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorPalabrasAvanzado(root)
    root.mainloop()
