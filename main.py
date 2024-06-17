import  os
import openai
from dotenv import load_dotenv
import streamlit as st
from utils.data_manager import (
    extraer_texto_pdf, 
    preprocesar_texto, 
    obtener_respuesta, 
    flujo_laboratorio, 
    flujo_insumos, 
    buscar_datos_guardados, 
    generar_notificaciones_pendientes
)

# Cargar la clave API desde el archivo .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Verifica que la clave de API está configurada
if not openai_api_key:
    st.error("No API key provided. Please set your API key in the .env file.")

# Configuración de la página principal
st.set_page_config(page_title="Asistente Virtual OMARDENT", page_icon="🤖")

# Título principal
st.title("Asistente Virtual OMARDENT")

# Sidebar para navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Página Principal", "Gestión de Trabajos", "Gestión de Insumos", "Registro de Radiografías", "Buscar Datos", "Notificaciones"])

# Mostrar el logo en el sidebar
logo_path = os.path.join("assets", "Logo Omardent.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
else:
    st.sidebar.warning("No se encontró el logo en la ruta especificada.")

# Importar páginas

if page == "Página Principal":
    from pages import home
    home.show()
elif page == "Gestión de Trabajos":
    from pages import trabajos
    trabajos.show()
elif page == "Gestión de Insumos":
    from pages import insumos
    insumos.show()
elif page == "Registro de Radiografías":
    from pages import radiografias
    radiografias.show()
elif page == "Buscar Datos":
    from pages import buscar_datos
    buscar_datos.show()
elif page == "Notificaciones":
    from pages import notificaciones
    notificaciones.show()
elif page == "Página Chat":
    from pages import chat
    chat.show()

# --- Video de fondo ---
with st.container():
    st.markdown(
        f"""
        <style>
        #video-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            background-color: lightblue;
            overflow: hidden;
        }}
        #background-video {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
        </style>
        <div id="video-container">
            <video id="background-video" autoplay loop muted playsinline>
                 <source src="https://cdn.leonardo.ai/users/645c3d5c-ca1b-4ce8-aefa-a091494e0d09/generations/89dda365-bf17-4867-87d4-bd918d4a2818/89dda365-bf17-4867-87d4-bd918d4a2818.mp4" type="video/mp4">
            </video>
        </div>
        """,
        unsafe_allow_html=True,
    )
