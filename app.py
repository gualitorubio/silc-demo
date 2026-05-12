import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA E IDENTIDAD ---
st.set_page_config(page_title="SILC Demo - Rubio Intelligence Systems", layout="wide")

# Carga de Logos en la barra lateral
st.sidebar.image("SILC Logo.png", use_container_width=True)
st.sidebar.image("Rubio Intelligence Systems Logo.png", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Instrucciones de Uso")
st.sidebar.info("""
1. Escriba su pregunta de prueba en el chat.
2. Obtendrá un análisis técnico basado en nuestra base de datos legislativa.
3. Esta es una prueba de cortesía de una sola consulta.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Director**")
st.sidebar.write("Doctorando Carlos Rubio")
st.sidebar.caption("© 2026 Rubio Intelligence Systems")

# --- LÓGICA DE CONTROL DE CONSULTA ÚNICA ---
if 'consulta_realizada' not in st.session_state:
    st.session_state.consulta_realizada = False

# Encabezado principal
st.title("⚖️ SILC: Sistema de Inteligencia Legal y Contexto")
st.subheader("Certeza jurídica con profundidad histórica")
st.write("Bienvenido al centro de pruebas. Explore el potencial de nuestra galaxia de datos.")

# Muro de pago/bloqueo si ya usó su oportunidad
if st.session_state.consulta_realizada:
    st.error("### 🛑 CONSULTA DE CORTESÍA AGOTADA")
    st.markdown("Estimado usuario, ha completado su prueba gratuita de SILC.")
    st.info("Para realizar consultas ilimitadas y acceder a los 124,000 registros completos, por favor adquiera una suscripción.")
    st.link_button("Ver Planes de Suscripción en silcmexico.com", "https://silcmexico.com")
    st.stop()

# --- INTERFAZ DE ENTRADA ---
st.markdown("---")
user_input = st.chat_input("Escriba su pregunta de prueba aquí...")

if user_input:
    # Marcamos que ya usó su oportunidad inmediatamente para evitar abusos
    st.session_state.consulta_realizada = True
    
    with st.chat_message("assistant"):
        with st.spinner("Realizando análisis técnico profundo..."):
            # Aquí iría la integración con Gemini y Pinecone
            st.write(f"Doctor Rubio, el sistema está procesando la siguiente consulta: **{user_input}**")
            st.markdown("---")
            st.success("Análisis completado. Esta respuesta fue generada como parte de su prueba de cortesía.")

    st.toast("Ha agotado su consulta de prueba.")
