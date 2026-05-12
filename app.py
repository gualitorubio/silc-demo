import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SILC Demo - Rubio Intelligence Systems", layout="wide")

# Carga de Logos (Deben estar en la raíz de tu GitHub)
st.sidebar.image("SILC Logo.png", use_container_width=True)
st.sidebar.image("Rubio Intelligence Systems Logo.png", use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Instrucciones")
st.sidebar.info("1. Ingrese su consulta.\n2. Espere el análisis técnico.\n3. Su prueba de cortesía es de una sola consulta.")

st.sidebar.markdown("---")
st.sidebar.markdown("**Director**")
st.sidebar.write("Doctorando Carlos Rubio")
st.sidebar.caption("© 2026 Rubio Intelligence Systems")

# --- CONTROL DE ACCESO ---
if 'acceso' not in st.session_state:
    st.session_state.acceso = False

if not st.session_state.acceso:
    st.title("⚖️ SILC: Sistema de Inteligencia Legal y Contexto")
    opcion = st.radio("Identifíquese:", ["Invitado VIP (Docente)", "Prueba Gratuita (Abogado)"])
    
    if opcion == "Invitado VIP (Docente)":
        clave = st.text_input("Clave Institucional:", type="password")
        if st.button("Entrar"):
            if clave == "SILC_UNAM_2026": # Puedes cambiar esta clave
                st.session_state.acceso = True
                st.session_state.rol = "VIP"
                st.rerun()
    else:
        wa = st.text_input("WhatsApp (10 dígitos):")
        if st.button("Iniciar Consulta"):
            if len(wa) >= 10:
                st.session_state.acceso = True
                st.session_state.rol = "LEAD"
                st.session_state.wa = wa
                st.rerun()
    st.stop()

# --- BLOQUEO DE CONSULTA ÚNICA ---
if st.session_state.rol == "LEAD":
    if 'usado' not in st.session_state:
        st.session_state.usado = False
    
    if st.session_state.usado:
        st.error("### 🛑 CONSULTA AGOTADA")
        st.info("Doctor, ha agotado su prueba. Para continuar, adquiera un plan.")
        st.link_button("Ir a Planes de Suscripción", "https://silcmexico.com")
        st.stop()

# --- ESPACIO PARA TU LÓGICA DE IA (GEMINI + PINECONE) ---
st.title("🤖 Consulta Técnica SILC")
user_query = st.chat_input("Realice su consulta aquí...")

if user_query:
    # Aquí es donde el sistema responde usando tus API Keys
    with st.chat_message("assistant"):
        st.write(f"Procesando consulta técnica para el número {st.session_state.get('wa', 'VIP')}...")
        # (La respuesta de tu modelo iría aquí)
        st.success("Respuesta generada con éxito.")
    
    if st.session_state.rol == "LEAD":
        st.session_state.usado = True
        st.toast("Prueba finalizada.")
