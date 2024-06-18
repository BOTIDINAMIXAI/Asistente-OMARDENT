# pages/notificaciones.py
import streamlit as st
from utils.data_manager import generar_notificaciones_pendientes

def show():
    generar_notificaciones_pendientes()
