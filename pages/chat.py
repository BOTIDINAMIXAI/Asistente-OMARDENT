# pages/chat.py
import streamlit as st
import io
from gtts import gTTS
from utils.data_manager import (
    extraer_texto_pdf, 
    preprocesar_texto, 
    obtener_respuesta, 
    handle_voice_input
)

def show():
    st.header("💬 Hablar con Galatea OMARDENT - Página de Chat")

    # Inicializa los valores predeterminados si no existen
    if 'modelo' not in st.session_state:
        st.session_state.modelo = "gpt-3.5-turbo"
    if 'temperatura' not in st.session_state:
        st.session_state.temperatura = 0.5

    # --- Barra lateral ---
    with st.sidebar:
        st.image(os.path.join("assets", "Logo Omardent.png"), use_column_width=True)
        st.title("🤖 Galatea OMARDENT")
        st.markdown("---")

        # Selección de modelo de lenguaje
        st.subheader("🧠 Configuración del Modelo")
        st.session_state.modelo = st.selectbox(
            "Selecciona el modelo:",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k"],
            index=0,
            help="Elige el modelo de lenguaje de OpenAI que prefieras."
        )

        # Opciones adicionales
        st.markdown("---")
        st.session_state.temperatura = st.slider("🌡️ Temperatura", min_value=0.0, max_value=1.0, value=st.session_state.temperatura, step=0.1)

    # --- Área principal de la aplicación ---
    # Carga de archivo PDF
    archivo_pdf = st.file_uploader("📂 Cargar PDF", type='pdf', key='chat_pdf')

    # --- Chatbot ---
    if 'mensajes_chat' not in st.session_state:
        st.session_state.mensajes_chat = []

    for mensaje in st.session_state.mensajes_chat:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    pregunta_usuario = st.chat_input("Pregunta:")
    if pregunta_usuario:
        st.session_state.mensajes_chat.append({"role": "user", "content": pregunta_usuario})
        with st.chat_message("user"):
            st.markdown(pregunta_usuario)

        if archivo_pdf:
            texto_pdf = extraer_texto_pdf(archivo_pdf)
            texto_preprocesado = preprocesar_texto(texto_pdf)
        else:
            texto_preprocesado = ""  

        respuesta = obtener_respuesta(pregunta_usuario, texto_preprocesado, st.session_state.modelo, st.session_state.temperatura)
        st.session_state.mensajes_chat.append({"role": "assistant", "content": respuesta})
        with st.chat_message("assistant"):
            st.markdown(respuesta)

    # --- Captura de voz ---
    st.markdown("### Captura de voz")
    audio_capturado = st.file_uploader("Subir archivo de audio", type=["wav", "mp3"], key='audio_chat')
    if audio_capturado:
        texto_extraido = handle_voice_input(audio_capturado)
        st.write("Texto extraído del audio:")
        st.write(texto_extraido)

    st.markdown("---")
