# pages/radiografias.py
import streamlit as st
from utils.data_manager import guardar_en_archivo
import pandas as pd

def show():
    st.title("📋 Registro de Radiografías")

    if 'radiografias' not in st.session_state:
        st.session_state.radiografias = []

    # Formulario para registrar radiografías
    with st.form("radiografia_form"):
        nombre_paciente = st.text_input("Nombre del Paciente")
        fecha_envio = st.date_input("Fecha en que se envía la Radiografía")
        motivo_consulta = st.text_area("Motivo de Consulta")
        tipo_diagnostico = st.text_input("Tipo de Diagnóstico")
        tutor_envia = st.selectbox("Tutor que envía la Radiografía", ["Dr. José Daniel C", "Dr. José Omar C"])
        motivo_envio = st.text_area("Motivo para Enviar la Radiografía")
        respuesta_recomendaciones = st.selectbox("Recomendaciones e Indicaciones", [
            "Recomendaciones después de una exodoncia dental",
            "Recomendaciones después de un blanqueamiento dental",
            "Recomendaciones para el uso de una prótesis dental"
        ])

        submitted = st.form_submit_button("Registrar Radiografía")

        if submitted:
            radiografia = {
                "nombre_paciente": nombre_paciente,
                "fecha_envio": str(fecha_envio),
                "motivo_consulta": motivo_consulta,
                "tipo_diagnostico": tipo_diagnostico,
                "tutor_envia": tutor_envia,
                "motivo_envio": motivo_envio,
                "respuesta_recomendaciones": respuesta_recomendaciones
            }
            st.session_state.radiografias.append(radiografia)
            guardar_en_archivo('radiografias.json', st.session_state.radiografias)
            st.success("Radiografía registrada con éxito.")
    
    if st.session_state.radiografias:
        st.write("### Radiografías Registradas")
        df_radiografias = pd.DataFrame(st.session_state.radiografias)
        st.write(df_radiografias)
        
        # Agregar opción para descargar como PDF
        if not df_radiografias.empty:
            pdf_file = guardar_como_pdf(df_radiografias, "Registro de Radiografías", "radiografias.pdf")
            st.download_button(
                label="📥 Descargar PDF",
                data=open(pdf_file, 'rb').read(),
                file_name="radiografias.pdf",
                mime="application/pdf"
            )

def guardar_como_pdf(dataframe, titulo, filename):
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
