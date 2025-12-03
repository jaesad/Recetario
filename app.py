import streamlit as st
import json
import os
from pathlib import Path

# Configurar la página
st.set_page_config(
    page_title="Recetario de Cocina",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
        /* Estilos globales */
        .main {
            padding: 1rem;
        }
        
        /* Estilos para las tarjetas de recetas */
        .recipe-card {
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            padding: 1rem;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            background-color: white;
            height: 100%;
        }
        
        .recipe-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            border-color: #2E86AB;
        }
        
        .recipe-card-title {
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 10px;
            min-height: 50px;
        }
        
        /* Estilos para vista de detalles */
        .detail-title {
            font-size: 2.5em;
            font-weight: bold;
            color: #2E86AB;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .section-header {
            font-size: 1.8em;
            font-weight: bold;
            color: #A23B72;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 3px solid #A23B72;
            padding-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'galeria'
if 'receta_seleccionada' not in st.session_state:
    st.session_state.receta_seleccionada = None

# Cargar las recetas
@st.cache_data
def cargar_recetas():
    """Carga el archivo de recetas JSON"""
    ruta_recetas = Path(__file__).parent / "recetas.json"
    with open(ruta_recetas, "r", encoding="utf-8") as f:
        return json.load(f)

# Obtener ruta de la imagen
def obtener_ruta_imagen(ruta_relativa):
    """Obtiene la ruta completa de la imagen"""
    ruta_relativa = ruta_relativa.lstrip("/")
    ruta_imagen = Path(__file__).parent / ruta_relativa
    
    if ruta_imagen.exists():
        return str(ruta_imagen)
    return None

# Formatear ingredientes recursivamente
def formatear_ingredientes(ingredientes, nivel=0):
    """Formatea ingredientes incluyendo los anidados"""
    resultado = []
    
    for nombre, detalles in ingredientes.items():
        if isinstance(detalles, dict):
            # Verificar si tiene estructura de ingrediente (Cantidad, Unidad)
            if 'Cantidad' in detalles or 'Unidad' in detalles:
                cantidad = detalles.get('Cantidad', '')
                unidad = detalles.get('Unidad', '')
                
                if unidad:
                    texto = f"**{nombre}**: {cantidad} {unidad}"
                elif cantidad:
                    texto = f"**{nombre}**: {cantidad}"
                else:
                    texto = f"**{nombre}**"
                
                resultado.append(('ingrediente', nivel, texto))
            else:
                # Es un grupo de ingredientes anidados
                resultado.append(('titulo', nivel, f"**{nombre}:**"))
                # Recursión para ingredientes anidados
                sub_ingredientes = formatear_ingredientes(detalles, nivel + 1)
                resultado.extend(sub_ingredientes)
        else:
            resultado.append(('ingrediente', nivel, f"**{nombre}**: {detalles}"))
    
    return resultado

# Página de galería
def mostrar_galeria(recetas, termino_busqueda=""):
    """Muestra la galería de recetas en formato de tarjetas"""
    st.title("🍳 Recetario de Cocina")
    st.markdown("### Selecciona una receta para ver los detalles")
    
    # Campo de búsqueda
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        busqueda = st.text_input(
            "🔍 Buscar recetas",
            value=termino_busqueda,
            placeholder="Escribe el nombre de una receta...",
            label_visibility="collapsed"
        )
    
    # Filtrar recetas
    if busqueda.strip():
        recetas_filtradas = {
            nombre: datos for nombre, datos in recetas.items()
            if busqueda.lower() in nombre.lower()
        }
    else:
        recetas_filtradas = recetas
    
    # Mostrar contador
    st.markdown(f"**{len(recetas_filtradas)} receta(s) encontrada(s)**")
    st.markdown("---")
    
    # Mostrar recetas en grid
    if recetas_filtradas:
        # Crear columnas para el grid (3 por fila)
        recetas_lista = list(recetas_filtradas.items())
        num_cols = 3
        
        for i in range(0, len(recetas_lista), num_cols):
            cols = st.columns(num_cols)
            
            for j in range(num_cols):
                idx = i + j
                if idx < len(recetas_lista):
                    nombre, datos = recetas_lista[idx]
                    
                    with cols[j]:
                        # Contenedor de la tarjeta
                        with st.container():
                            # Imagen
                            ruta_imagen = obtener_ruta_imagen(datos.get("imagen", ""))
                            if ruta_imagen:
                                st.image(ruta_imagen, width='stretch')
                            else:
                                st.info("Sin imagen")
                            
                            # Título de la receta
                            st.markdown(f'<div class="recipe-card-title">{nombre}</div>', unsafe_allow_html=True)
                            
                            # Botón para ver detalles
                            if st.button(f"Ver receta", key=f"btn_{nombre}", width='stretch'):
                                st.session_state.receta_seleccionada = nombre
                                st.session_state.pagina = 'detalle'
                                st.rerun()
                        
                        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("🔍 No se encontraron recetas. Intenta con otra búsqueda.")

# Página de detalles de receta
def mostrar_detalle(nombre_receta, datos_receta):
    """Muestra los detalles completos de una receta"""
    
    # Usar componente para ejecutar JavaScript que haga scroll al top
    import streamlit.components.v1 as components
    components.html(
        """
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
        """,
        height=0,
    )
    
    # Botón para volver
    if st.button("← Volver a la galería", type="secondary"):
        st.session_state.pagina = 'galeria'
        st.rerun()
    
    st.markdown("---")
    
    # Título
    st.markdown(f'<div class="detail-title">🍽️ {nombre_receta}</div>', unsafe_allow_html=True)
    
    # Columnas para layout
    col_img, col_content = st.columns([1, 1])
    
    with col_img:
        # Imagen
        ruta_imagen = obtener_ruta_imagen(datos_receta.get("imagen", ""))
        if ruta_imagen:
            st.image(ruta_imagen, width='stretch')
        else:
            st.warning("⚠️ Imagen no encontrada")
    
    with col_content:
        # Ingredientes
        st.markdown('<div class="section-header">📝 Ingredientes</div>', unsafe_allow_html=True)
        
        if "Ingredientes" in datos_receta:
            ingredientes_formateados = formatear_ingredientes(datos_receta["Ingredientes"])
            
            for tipo, nivel, texto in ingredientes_formateados:
                if tipo == 'titulo':
                    st.markdown(texto)
                else:
                    # Agregar indentación para ingredientes anidados
                    indentacion = "  " * nivel
                    if nivel > 0:
                        st.markdown(f"{indentacion}• {texto}")
                    else:
                        st.markdown(f"• {texto}")
    
    # Instrucciones (ancho completo)
    st.markdown('<div class="section-header">👨‍🍳 Instrucciones</div>', unsafe_allow_html=True)
    
    if "Instrucciones" in datos_receta:
        for i, instruccion in enumerate(datos_receta["Instrucciones"], 1):
            st.markdown(f"**{i}.** {instruccion}")
            st.markdown("")

# Función principal
def main():
    recetas = cargar_recetas()
    
    # Navegación basada en session state
    if st.session_state.pagina == 'galeria':
        mostrar_galeria(recetas)
    elif st.session_state.pagina == 'detalle' and st.session_state.receta_seleccionada:
        nombre = st.session_state.receta_seleccionada
        if nombre in recetas:
            mostrar_detalle(nombre, recetas[nombre])
        else:
            st.error("Receta no encontrada")
            st.session_state.pagina = 'galeria'
            st.rerun()

if __name__ == "__main__":
    main()
