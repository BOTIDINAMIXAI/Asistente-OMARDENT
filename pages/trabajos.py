import streamlit as st
from utils.data_manager import flujo_laboratorio

def show():
    st.title("🦷 Gestión de Trabajos de Laboratorio")
    flujo_laboratorio()
