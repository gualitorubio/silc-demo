import streamlit as st
import google.generativeai as genai
from pinecone import Pinecone

# ==========================================
# 1. CONFIGURACIÓN DE IDENTIDAD Y PÁGINA
# ==========================================
st.set_page_config(
    page_title="SILC Demo - Rubio Intelligence Systems", 
    page_icon="⚖️", 
    layout="centered"
)

# Estilo para logos
st.markdown("<style> .stImage {display: block; margin-left: auto; margin-right: auto;} </style>", unsafe_allow_html=True)

# ==========================================
# 2. BARRA LATERAL (IDENTIDAD)
# ==========================================
with st.sidebar:
    try:
        st.image("SILC Logo.png", use_container_width=True)
        st.image("Rubio Intelligence Systems Logo.png", use_container_width=True)
    except:
        pass
    
    st.divider()
    st.markdown("### 📖 Instrucciones de Uso")
    st.info("Esta es una versión de cortesía. Solo permite **una consulta técnica** para demostrar el poder del SILC.")
    
    st.divider()
    st.markdown("### Director")
    st.write("Doctorando Carlos Rubio")
    st.caption("© 2026 Rubio Intelligence Systems")

# ==========================================
# 3. LÓGICA DE BLOQUEO (UNA SOLA PREGUNTA)
# ==========================================
if "demo_finalizada" not in st.session_state:
    st.session_state.demo_finalizada = False

st.title("⚖️ SILC")
st.markdown("#### *Certeza jurídica con profundidad histórica*")
st.divider()

# Muro de pago si ya se hizo la pregunta
if st.session_state.demo_finalizada:
    st.error("### 🛑 CONSULTA DE CORTESÍA AGOTADA")
    st.markdown("""
    Estimado colega, ha completado su prueba gratuita. Para acceder de forma ilimitada 
    a los **124,000 registros**, análisis comparativos y descarga de fichas técnicas:
    """)
    st.link_button("🚀 ADQUIRIR SUSCRIPCIÓN PROFESIONAL", "https://silcmexico.com")
    st.stop()

# ==========================================
# 4. CONFIGURACIÓN DE MOTOR (IA & VECTOR DB)
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3-flash-preview')
    pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
    index = pc.Index("galaxia-de-datos")
except Exception as e:
    st.error("Error de conexión técnica. Verifique sus Secrets.")

# ==========================================
# 5. PROCESAMIENTO DE LA PREGUNTA ÚNICA
# ==========================================
if prompt := st.chat_input("Escriba su pregunta de prueba aquí..."):
    # Mostramos la pregunta del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Consultando registros del SILC..."):
                # 1. Búsqueda Vectorial
                res_embed = pc.inference.embed(
                    model="multilingual-e5-large",
                    inputs=[prompt],
                    parameters={"input_type": "query"}
                )
                
                query_res = index.query(
                    vector=res_embed[0].values, 
                    top_k=5, 
                    include_metadata=True,
                    namespace="silc-juridico"
                )
                
                contexto_legal = "\n\n".join([m['metadata']['text'] for m in query_res['matches']])

                # 2. Generación de Respuesta con Rigor
                instruccion = (
                    f"Eres el SILC. Tu lema es 'Certeza jurídica con profundidad histórica'. "
                    f"Responde con altísimo rigor académico y legal basándote en este contexto:\n\n"
                    f"{contexto_legal}\n\nPregunta: {prompt}"
                )

                response = model.generate_content(instruccion)
                st.markdown(response.text)
                
                # 3. ACTIVAR EL BLOQUEO PERMANENTE
                st.session_state.demo_finalizada = True
                st.success("Análisis completado exitosamente.")
                st.toast("Ha agotado su consulta de cortesía.")
                
        except Exception as e:
            st.error(f"Error en el procesamiento: {str(e)}")
