# 🍳 Recetario de Cocina - Aplicación Streamlit

Aplicación interactiva de recetas de cocina desarrollada con Streamlit. Permite buscar y explorar recetas con ingredientes, instrucciones e imágenes.

## 📋 Características

- ✅ Buscador de recetas en tiempo real
- 📸 Visualización de imágenes de cada receta
- 📝 Lista completa de ingredientes con cantidades
- 👨‍🍳 Instrucciones paso a paso
- 🎨 Interfaz moderna y responsiva
- 📱 Optimizada para móviles

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto** (si está en un repositorio)
   ```bash
   cd Recetario
   ```

2. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   streamlit run app.py
   ```

4. **Abrir en el navegador**
   La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📁 Estructura del proyecto

```
Recetario/
├── app.py              # Aplicación principal de Streamlit
├── recetas.json        # Base de datos de recetas
├── requirements.txt    # Dependencias del proyecto
├── README.md           # Este archivo
└── imagenes/           # Carpeta con imágenes de recetas
    ├── pimientos-asados.jpg
    ├── pollo-a-las-hierbas.jpg
    └── ... (más imágenes)
```

## 💻 Cómo usar

1. **Buscar una receta:**
   - Escribe en el campo de búsqueda de la barra lateral
   - Las recetas se filtran en tiempo real mientras escribes

2. **Seleccionar una receta:**
   - Elige la receta deseada del menú desplegable
   - Se mostrará la imagen, ingredientes e instrucciones

3. **Ver detalles:**
   - Desplázate para ver todos los ingredientes y pasos
   - Cada paso está numerado y formateado claramente

## 🔍 Ejemplos de búsqueda

- "Pollo" → Encontrará todas las recetas con pollo
- "Merluza" → Mostrará recetas de merluza
- "Ensalada" → Filtrará recetas de ensaladas
- "Patatas" → Recetas que contienen patatas

## ⚙️ Requisitos del sistema

- **Procesador:** Cualquiera
- **RAM:** 512 MB mínimo (1 GB recomendado)
- **Espacio en disco:** 100 MB
- **Conexión de red:** No requiere conexión continua (funciona offline)

## 📝 Agregar nuevas recetas

Para agregar una nueva receta al archivo `recetas.json`:

```json
"Nombre de la Receta": {
    "imagen": "/imagenes/nombre-imagen.jpg",
    "Ingredientes": {
        "Ingrediente 1": {"Cantidad": 2, "Unidad": "piezas"},
        "Ingrediente 2": {"Cantidad": 100, "Unidad": "gramos"}
    },
    "Instrucciones": [
        "Paso 1",
        "Paso 2",
        "Paso 3"
    ]
}
```

## 🎨 Personalización

Puedes modificar los estilos CSS en la sección `<style>` del archivo `app.py` para cambiar colores y formatos.

## 🐛 Solución de problemas

**Problema:** La imagen no se muestra
- Verifica que el archivo de imagen existe en la carpeta `imagenes/`
- Comprueba que la ruta en el JSON es correcta

**Problema:** "ModuleNotFoundError: No module named 'streamlit'"
- Ejecuta: `pip install -r requirements.txt`

**Problema:** La aplicación es lenta
- Cierra otras aplicaciones
- Verifica que las imágenes no sean demasiado pesadas (< 1 MB cada una)

## 📄 Licencia

Este proyecto es de uso personal/educativo.

## 👨‍💻 Autor

Creado con ❤️ usando Streamlit

---

¡Disfruta cocinando! 🍽️
