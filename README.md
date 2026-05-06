# 📊 Analizador de Textos Avanzado

Aplicación de escritorio con interfaz gráfica para análisis lingüístico y comparación de textos. Desarrollada en Python con Tkinter.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Características

- **Análisis completo de textos**: contador de palabras, caracteres, oraciones y sílabas
- **Estadísticas avanzadas**: densidad léxica, palabras únicas
- **Detección de idioma**: soporte para múltiples idiomas (español, inglés, francés, alemán, italiano, portugués)
- **Análisis de sentimiento**: clasifica el texto como positivo, negativo o neutral
- **Palabras más frecuentes**: lista Top 10 con visualización
- **Gráficos interactivos**: barras con las palabras más usadas
- **Comparación de textos**: similitud entre dos textos mediante coeficiente de Jaccard
- **Interfaz profesional**: pestañas organizadas, diseño limpio estilo Google Docs/Word

## 🖥️ Capturas de Pantalla

| Estadísticas | Gráficos | Comparación |
|-------------|----------|-------------|
| [Métricas completas] | [Barras interactivas] | [Similitud entre textos] |

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos para instalar

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/analizador-textos.git
cd analizador-textos
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación

**Windows**:
```bash
ejecutar.bat
```
o
```bash
python ContadorDePalabras.py
```

**Linux/Mac**:
```bash
python3 ContadorDePalabras.py
```

## 📚 Uso

### Modo Texto Único
1. Escribe o pega tu texto en el área principal
2. Haz clic en "ANALIZAR TEXTO"
3. Visualiza los resultados en las pestañas:
   - **Estadísticas**: métricas detalladas
   - **Gráficos**: visualización de palabras frecuentes

### Modo Comparar Textos
1. Selecciona "Comparar Textos" en el selector superior
2. Ingresa los dos textos en las áreas correspondientes
3. Haz clic en "ANALIZAR TEXTO"
4. Revisa la similitud y diferencias en la pestaña "Comparación"

## 📦 Dependencias

- `tkinter`: interfaz gráfica (incluida en Python estándar)
- `matplotlib`: gráficos estadísticos
- `langdetect`: detección de idiomas
- `textblob`: análisis de sentimiento
- `numpy`: procesamiento numérico

## 📊 Métricas Calculadas

- **Palabras**: total de palabras en el texto
- **Caracteres**: caracteres sin espacios
- **Palabras únicas**: vocabulario distinto
- **Oraciones**: mediante puntuación (.!?)
- **Sílabas**: algoritmo de conteo silábico
- **Densidad léxica**: (palabras únicas / total palabras) × 100
- **Idioma**: detección automática
- **Sentimiento**: polaridad del texto
- **Similitud**: coeficiente de Jaccard entre textos

## 🎨 Paleta de Colores

Estilo clásico limpio inspirado en editores profesionales:
- Gris claro para fondos
- Blanco para áreas de texto
- Gris oscuro para acentos y botones
- Negro suave para texto principal

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Distribuido bajo licencia MIT. Ver `LICENSE` para más información.

## 👤 Autor

**Christian Lera**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- Biblioteca `langdetect` para detección de idiomas
- `TextBlob` para análisis de sentimiento
- `Matplotlib` para visualización de datos

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:
1. Abre un issue en GitHub
2. Contacta al autor

---

⭐ ¡No olvides darle una estrella al proyecto si te fue útil!
