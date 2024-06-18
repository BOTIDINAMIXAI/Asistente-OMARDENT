import streamlit as st
import os
import openai
from utils.data_manager import (
    extraer_texto_pdf, 
    preprocesar_texto, 
    obtener_respuesta
)
import speech_recognition as sr

# Configuración de la clave API
openai.api_key = ""  # Reemplaza esto con tu clave API real

def inicializar_estado():
    """Inicializa el estado de la sesión si no está ya inicializado."""
    if 'modelo' not in st.session_state:
        st.session_state['modelo'] = "gpt-3.5-turbo-16k"
    if 'temperatura' not in st.session_state:
        st.session_state['temperatura'] = 0.5
    if 'mensajes_chat' not in st.session_state:
        st.session_state['mensajes_chat'] = []

def barra_lateral():
    ruta_logo = os.path.join("assets", "Logo Omardent.png")
    if os.path.exists(ruta_logo):
        st.sidebar.image(ruta_logo, use_column_width=True)
    else:
        st.sidebar.warning(f"Error: No se pudo encontrar la imagen en la ruta: {ruta_logo}")

    st.sidebar.title("🤖 Galatea OMARDENT")
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Configuración del Modelo")
    st.session_state['modelo'] = st.sidebar.selectbox(
        "Selecciona el modelo:",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k"],
        index=0,
        key='modelo_selectbox',  # Clave única
        help="Elige el modelo de lenguaje de OpenAI que prefieras."
    )
    st.sidebar.markdown("---")
    st.session_state['temperatura'] = st.sidebar.slider(
        "🌡️ Temperatura",
        min_value=0.0, max_value=1.0,
        value=st.session_state['temperatura'],
        step=0.1,
        key='temperatura_slider'  # Clave única
    )

def mostrar_mensajes_chat():
    for mensaje in st.session_state['mensajes_chat']:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def manejar_pregunta_usuario(pregunta_usuario, archivo_pdf):
    st.session_state['mensajes_chat'].append({"role": "user", "content": pregunta_usuario})
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)

    texto_preprocesado = ""
    if archivo_pdf:
        texto_pdf = extraer_texto_pdf(archivo_pdf)
        texto_preprocesado = preprocesar_texto(texto_pdf)

    respuesta = obtener_respuesta(pregunta_usuario, texto_preprocesado, st.session_state['modelo'], st.session_state['temperatura'])
    st.session_state['mensajes_chat'].append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)

def manejar_captura_de_voz(audio_capturado):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_capturado) as source:
        audio = recognizer.record(source)
        try:
            texto_extraido = recognizer.recognize_google(audio, language='es-ES')
            st.markdown("### Texto extraído del audio:")
            st.write(texto_extraido)
        except sr.UnknownValueError:
            st.markdown("### No se pudo entender el audio.")
        except sr.RequestError as e:
            st.markdown(f"### Error en el servicio de reconocimiento: {e}")

def main():
    inicializar_estado()
    barra_lateral()

    st.title("VIRTUAL OMARDENT AI-BOTIDINAMIX")
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
                <source src="https://dnznrvs05pmza.cloudfront.net/9f234f58-3cb2-489d-98cc-4e40c83b1acd.mp4?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiODFlMzZiOGQwMWNiN2I0YiIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTcxODg0MTYwMH0.NGKRvVNwKR6Aa_gP-m8zFYAnFPBz1L9Zzz1xjWxnaj8" type="video/mp4">
            </video>
        </div>
        """,
        unsafe_allow_html=True,
    )

    archivo_pdf = st.file_uploader("📂 Cargar PDF", type='pdf', key='chat_pdf')

# Sidebar para navegación
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a", ["Página Principal", "Gestión de Trabajos", "Gestión de Insumos", "Registro de Radiografías", "Buscar Datos", "Notificaciones", "Recomendaciones"])

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
elif page == "Recomendaciones":
    from pages import recomendaciones
    recomendaciones.show()

if __name__ == "__main__":
    main()
