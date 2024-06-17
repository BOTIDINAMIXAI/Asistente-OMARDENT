import streamlit as st
from utils.data_manager import buscar_datos_guardados

def show():
    st.title("🔍 Buscar datos_guardados")
    buscar_datos_guardados()
