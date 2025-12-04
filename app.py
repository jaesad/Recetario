import streamlit as st
import json
import os
from PIL import Image, ImageOps

# Configuración de la página (Título y layout)
st.set_page_config(
    page_title="Mi Recetario",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PERSONALIZADOS (MOBILE FIRST) ---
st.markdown("""
    <style>
    /* Ajustes generales para móvil */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    
    /* Estilo de las tarjetas de recetas */
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        margin-bottom: 15px;
        align-items: center;
    }

    /* Títulos de las tarjetas */
    h3 {
        margin-top: 0 !important;
        padding-top: 0 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }

    /* Botones personalizados */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #ff4b4b;
        color: #ff4b4b;
        background-color: transparent;
        transition: all 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #ff4b4b;
        color: white;
        border-color: #ff4b4b;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE AYUDA ---

@st.cache_data
def cargar_recetas():
    """Carga el archivo JSON de recetas."""
    archivo = 'recetas.json'
    if not os.path.exists(archivo):
        st.error(f"No se encuentra el archivo {archivo}")
        return {}
    
    with open(archivo, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            st.error("Error al leer el archivo JSON.")
            return {}

def procesar_imagen(ruta_relativa, tamaño=(300, 300), modo='cover'):
    """
    Carga, redimensiona y recorta una imagen para que sea uniforme.
    Maneja errores si la imagen no existe.
    """
    # El JSON tiene rutas tipo "/imagenes/foto.jpg", quitamos la barra inicial
    ruta_limpia = ruta_relativa.lstrip('/')
    
    if os.path.exists(ruta_limpia):
        try:
            img = Image.open(ruta_limpia)
            # ImageOps.fit recorta la imagen al centro para llenar el tamaño sin deformar (aspect ratio cover)
            if modo == 'cover':
                img = ImageOps.fit(img, tamaño, method=Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            return None
    return None

# --- GESTIÓN DE ESTADO (NAVEGACIÓN) ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'inicio'
if 'receta_seleccionada' not in st.session_state:
    st.session_state.receta_seleccionada = None

def ir_a_detalle(nombre_receta):
    st.session_state.receta_seleccionada = nombre_receta
    st.session_state.pagina = 'detalle'

def ir_a_inicio():
    st.session_state.pagina = 'inicio'

# --- VISTA PRINCIPAL (LISTADO) ---
def mostrar_inicio(recetas):
    st.title("📖 Mi Recetario")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar receta...", placeholder="Ej: Paella, Pollo...")
    
    st.write("") # Espaciador

    # Filtrar recetas
    items_recetas = list(recetas.items())
    if busqueda:
        items_recetas = [
            (k, v) for k, v in items_recetas 
            if busqueda.lower() in k.lower()
        ]

    if not items_recetas:
        st.info("No se encontraron recetas con ese nombre.")
        return

    # Renderizar lista de recetas
    for nombre, datos in items_recetas:
        # Usamos columnas para simular la tarjeta: Texto a la izq, Imagen a la der
        # En móvil, Streamlit apila las columnas, pero se verá bien igualmente.
        col_texto, col_img = st.columns([2, 1], gap="small")
        
        with col_texto:
            st.subheader(nombre)
            
            # Generar una descripción breve basada en los primeros ingredientes
            ingredientes_lista = list(datos.get('Ingredientes', {}).keys())
            descripcion = ", ".join(ingredientes_lista[:4])
            if len(ingredientes_lista) > 4:
                descripcion += "..."
            
            st.caption(f"{descripcion}")
            
            # Botón "Ver más"
            # Usamos un callback para cambiar el estado sin recargar toda la lógica desde cero
            st.button(
                "Ver receta", 
                key=f"btn_{nombre}", 
                on_click=ir_a_detalle, 
                args=(nombre,)
            )

        with col_img:
            # Procesamos la imagen para que sea un cuadrado perfecto (thumbnail)
            imagen = procesar_imagen(datos.get('imagen', ''), tamaño=(200, 200))
            if imagen:
                st.image(imagen, width='stretch')
            else:
                # Placeholder si no hay imagen
                st.markdown(
                    """<div style="height:100px; background-color:#f0f0f0; 
                    display:flex; align-items:center; justify-content:center; 
                    border-radius:8px; color:#aaa;">Sin Foto</div>""", 
                    unsafe_allow_html=True
                )

# --- VISTA DETALLE ---
def mostrar_detalle(recetas):
    nombre = st.session_state.receta_seleccionada
    datos = recetas.get(nombre)
    
    if not datos:
        st.error("Receta no encontrada.")
        if st.button("Volver"): ir_a_inicio()
        return

    # Botón flotante o superior para volver
    st.button("⬅️ Volver al listado", on_click=ir_a_inicio)
    
    st.title(nombre)
    
    # Imagen principal (Grande)
    imagen = procesar_imagen(datos.get('imagen', ''), tamaño=(800, 500), modo='cover')
    if imagen:
        st.image(imagen, width='stretch')
    
    st.divider()
    
    # Layout de Ingredientes y Pasos
    # En móvil se verán uno debajo del otro. En escritorio usamos tabs para ahorrar espacio
    tab1, tab2 = st.tabs(["🛒 Ingredientes", "👨‍🍳 Elaboración"])
    
    with tab1:
        st.write("#### Lo que necesitas:")
        ingredientes = datos.get('Ingredientes', {})
        for ing, detalle in ingredientes.items():
            cant = detalle.get('Cantidad', '')
            unidad = detalle.get('Unidad', '')
            texto_ing = f"**{ing}**: {cant} {unidad}"
            st.checkbox(texto_ing, key=f"chk_{nombre}_{ing}")

    with tab2:
        st.write("#### Paso a paso:")
        instrucciones = datos.get('Instrucciones', [])
        for i, paso in enumerate(instrucciones, 1):
            st.markdown(f"""
            <div style="background-color:#f9f9f9; color:black; padding:10px; border-radius:8px; margin-bottom:10px; border-left: 4px solid #ff4b4b;">
                <strong>{i}.</strong> {paso}
            </div>
            """, unsafe_allow_html=True)

# --- BLOQUE PRINCIPAL ---
def main():
    recetas = cargar_recetas()
    
    if st.session_state.pagina == 'inicio':
        mostrar_inicio(recetas)
    elif st.session_state.pagina == 'detalle':
        mostrar_detalle(recetas)

if __name__ == "__main__":
    main()