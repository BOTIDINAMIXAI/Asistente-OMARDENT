# utils/data_manager.py
import tempfile
import io
import openai
from dotenv import load_dotenv
from gtts import gTTS
import PyPDF2
import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pandas as pd
from fpdf import FPDF
import streamlit as st


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Cargar la clave API desde el archivo .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Verifica que la clave de API está configurada
if not openai_api_key:
    st.error("No API key provided. Please set your API key in the .env file.")


# Funciones generales
def extraer_texto_pdf(archivo):
    texto = ""
    if archivo:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(archivo.read())
            temp_file_path = temp_file.name
        with open(temp_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in range(len(reader.pages)):
                texto += reader.pages[page].extract_text()
        os.unlink(temp_file_path)
    return texto

def preprocesar_texto(texto):
    tokens = word_tokenize(texto, language='spanish')
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stopwords_es = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word not in stopwords_es]
    stemmer = SnowballStemmer('spanish')
    tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(tokens)

# Función para obtener respuesta de OpenAI usando el modelo GPT y convertir a audio
def obtener_respuesta(pregunta, texto_preprocesado, modelo, temperatura=0.5):
    try:
        response = openai.ChatCompletion.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Actúa como Galatea, la asistente de la clínica Odontológica OMARDENT y resuelve las inquietudes"},
                {"role": "user", "content": f"{pregunta}\n\nContexto: {texto_preprocesado}"}
            ],
            temperature=temperatura
        )
        respuesta = response.choices[0].message['content'].strip()

        # Convertir la respuesta a audio
        tts = gTTS(text=respuesta, lang='es')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        # Mostrar la respuesta en texto y audio
        st.audio(audio_bytes, format="audio/mp3")
        return respuesta

    except openai.OpenAIError as e:
        st.error(f"Error al comunicarse con OpenAI: {e}")
        return "Lo siento, no puedo procesar tu solicitud en este momento."

def guardar_en_archivo(nombre_archivo, datos):
    carpeta = "datos_guardados"
    os.makedirs(carpeta, exist_ok=True)
    ruta_archivo = os.path.join(carpeta, nombre_archivo)
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)
    return ruta_archivo

def cargar_desde_archivo(nombre_archivo):
    carpeta = "datos_guardados"
    ruta_archivo = os.path.join(carpeta, nombre_archivo)
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    else:
        return []

def generar_pdf(dataframe, titulo, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=titulo, ln=True, align='C')

    for i, row in dataframe.iterrows():
        row_text = ", ".join(f"{col}: {val}" for col, val in row.items())
        pdf.cell(200, 10, txt=row_text, ln=True)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name

# Función para manejar el flujo de trabajos del laboratorio
def flujo_laboratorio():
    st.title("🦷 Gestión de Trabajos de Laboratorio")

    if 'laboratorio' not in st.session_state:
        st.session_state.laboratorio = []

    # Formulario para ingresar datos del trabajo
    with st.form("laboratorio_form"):
        tipo_trabajo = st.selectbox("Tipo de trabajo:", [
            "Protesis total", "Protesis removible metal-acrilico", "Parcialita acrilico",
            "Placa de blanqueamiento", "Placa de bruxismo", "Corona de acrilico", 
            "Corona en zirconio", "Protesis flexible", "Acker flexible"
        ])
        doctor = st.selectbox("Doctor que requiere el trabajo:", ["Dr. Jose Daniel C", "Dr. Jose Omar C"])
        fecha_entrega = st.date_input("Fecha de entrega:")
        fecha_envio = st.date_input("Fecha de envío:")
        laboratorio = st.selectbox("Laboratorio dental:", ["Ernesto Correa lab", "Formando Sonrisas"])
        numero_orden = st.text_input("Número de orden:")
        cantidad = st.number_input("Cantidad:", min_value=1, step=1)

        submitted = st.form_submit_button("Registrar Trabajo")

        if submitted:
            trabajo = {
                "tipo_trabajo": tipo_trabajo,
                "doctor": doctor,
                "fecha_entrega": str(fecha_entrega),
                "fecha_envio": str(fecha_envio),
                "laboratorio": laboratorio,
                "numero_orden": numero_orden,
                "cantidad": cantidad,
                "estado": "pendiente"
            }
            st.session_state.laboratorio.append(trabajo)
            guardar_en_archivo('trabajos_laboratorio.json', st.session_state.laboratorio)
            st.success("Trabajo registrado con éxito.")
    
    if st.session_state.laboratorio:
        st.write("### Trabajos Registrados")
        df_trabajos = pd.DataFrame(st.session_state.laboratorio)
        st.write(df_trabajos)

        pdf_file = generar_pdf(df_trabajos, "Registro de Trabajos de Laboratorio", "trabajos_laboratorio.pdf")
        st.download_button(
            label="📥 Descargar PDF",
            data=open(pdf_file, 'rb').read(),
            file_name="trabajos_laboratorio.pdf",
            mime="application/pdf"
        )

# Función para manejar el flujo de insumos
def flujo_insumos():
    st.title("📦 Gestión de Insumos")

    if 'insumos' not in st.session_state:
        st.session_state.insumos = []

    # Formulario para ingresar insumos
    with st.form("insumos_form"):
        insumo_nombre = st.text_input("Nombre del Insumo:")
        insumo_cantidad = st.number_input("Cantidad Faltante:", min_value=0, step=1)
        submitted = st.form_submit_button("Agregar Insumo")

        if submitted and insumo_nombre:
            insumo = {"nombre": insumo_nombre, "cantidad": insumo_cantidad}
            st.session_state.insumos.append(insumo)
            guardar_en_archivo('insumos.json', st.session_state.insumos)
            st.success(f"Insumo '{insumo_nombre}' agregado con éxito.")

    if st.session_state.insumos:
        st.write("### Insumos Registrados")
        insumos_df = pd.DataFrame(st.session_state.insumos)
        st.write(insumos_df)

        pdf_file = generar_pdf(insumos_df, "Registro de Insumos Faltantes", "insumos.pdf")
        st.download_button(
            label="📥 Descargar PDF",
            data=open(pdf_file, 'rb').read(),
            file_name="insumos_faltantes.pdf",
            mime="application/pdf"
        )

def buscar_datos_guardados():
    st.title("🔍 Buscar Datos Guardados")

    # Mostrar archivos disponibles
    carpeta = "datos_guardados"
    if not os.path.exists(carpeta):
        st.info("No se encontraron archivos de datos guardados.")
        return

    archivos = [f for f in os.listdir(carpeta) if f.endswith('.json')]

    if archivos:
        archivo_seleccionado = st.selectbox("Selecciona un archivo para ver:", archivos)
        
        if archivo_seleccionado:
            datos = cargar_desde_archivo(archivo_seleccionado)
            if datos:
                st.write(f"### Datos del archivo {archivo_seleccionado}")
                st.json(datos)
            else:
                st.warning(f"No se encontraron datos en el archivo {archivo_seleccionado}")
    else:
        st.info("No se encontraron archivos de datos guardados.")

def generar_notificaciones_pendientes():
    if 'laboratorio' not in st.session_state or not st.session_state.laboratorio:
        st.info("No hay trabajos pendientes.")
        return
    
    pendientes = [trabajo for trabajo in st.session_state.laboratorio if trabajo["estado"] == "pendiente"]
    if pendientes:
        st.write("### Notificaciones de Trabajos Pendientes")
        for trabajo in pendientes:
            st.info(f"Pendiente: {trabajo['tipo_trabajo']} - {trabajo['numero_orden']} para {trabajo['doctor']}. Enviado a {trabajo['laboratorio']} el {trabajo['fecha_envio']}.")

def mostrar_datos_como_texto(datos):
    """Convierte datos JSON a un formato de texto legible."""
    texto = ""
    if isinstance(datos, dict):
        for key, value in datos.items():
            texto += f"{key}: {value}\n"
    elif isinstance(datos, list):
        for item in datos:
            if isinstance(item, dict):
                for key, value in item.items():
                    texto += f"{key}: {value}\n"
                texto += "\n"
            else:
                texto += f"{item}\n"
    return texto

# Incluye otras funciones utilitarias según sea necesario
