import streamlit as st
import requests # Para conectar con el CRM y la base de datos

# --- 1. FUNCIÓN DE BLOQUEO PERMANENTE ---
# (Aquí conectaríamos con tu base de datos de WhatsApps usados)
def usuario_ya_consulto(whatsapp):
    # Esta función revisará si el número existe en tu lista de MailingBoss o Google Sheets
    # Por ahora, simularemos la lógica de sesión, pero para producción usaremos tu CRM
    if "lista_negra" not in st.session_state:
        st.session_state.lista_negra = []
    return whatsapp in st.session_state.lista_negra

# --- 2. MURO DE ACCESO ---
if 'autorizado' not in st.session_state:
    st.session_state.autorizado = False

if not st.session_state.autorizado:
    st.title("⚖️ SILC - Modo de Prueba")
    perfil = st.radio("Identifíquese:", ["Docente (Acceso Total)", "Abogado (Prueba Única)"])
    
    if perfil == "Docente (Acceso Total)":
        clave = st.text_input("Clave Institucional:", type="password")
        if st.button("Entrar"):
            if clave == "SILC_UNIVERSIDAD_2026":
                st.session_state.autorizado = True
                st.session_state.rol = "VIP"
                st.rerun()
    else:
        nombre = st.text_input("Nombre:")
        whatsapp = st.text_input("WhatsApp (con prefijo +52):")
        if st.button("Iniciar mi única consulta gratis"):
            if usuario_ya_consulto(whatsapp):
                st.error("Usted ya ha agotado su prueba gratuita.")
                st.info("Suscríbase en silcmexico.com para acceso ilimitado.")
                st.stop()
            else:
                st.session_state.autorizado = True
                st.session_state.rol = "LEAD"
                st.session_state.wa = whatsapp
                st.rerun()
    st.stop()

# --- 3. RESTRICCIÓN DE UNA SOLA PREGUNTA ---
if st.session_state.rol == "LEAD":
    if 'preguntas_contadas' not in st.session_state:
        st.session_state.preguntas_contadas = 0
    
    if st.session_state.preguntas_contadas >= 1:
        st.warning("Prueba de cortesía finalizada.")
        st.markdown("### 🛑 Para continuar, adquiere un Plan Profesional.")
        st.stop()

# --- AQUÍ EMPIEZA TU CÓDIGO ORIGINAL DEL RAG ---
# (Carga de Gemini 2.0 Flash, Pinecone, etc.)
