import streamlit as st
import requests

# ----- CONFIG DASHBOARD -----

st.set_page_config(
    page_title="Consulta Expedientes Sinaloa, by: LIC. JOSEPH ÁNGEL MEZA LEÓN",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- HEADER / BANNER ---
st.markdown(
    "<h1 style='text-align:center;'>📁 Consulta de Expedientes - Poder Judicial Sinaloa</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# --- SIDEBAR FILTERS (optional) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Coat_of_arms_of_Sinaloa.svg/1200px-Coat_of_arms_of_Sinaloa.svg.png", width=100)
    st.markdown("**Filtros de consulta:**")
    materia = st.selectbox(
        "Selecciona la materia:",
        ["Civil", "Familiar", "Mercantil", "Administrativo"]
    )

# --- INPUTS ---
col1, col2 = st.columns([3, 1])
with col1:
    expediente = st.text_input("📄 Número de expediente (ej. 123/2025):")

with col2:
    buscar_btn = st.button("🔍 Buscar")

st.markdown("---")

if buscar_btn:
    if not expediente:
        st.error("Ingresa un número de expediente válido.")
    else:
        # --- MOCK / API Call Example ---
        # REEMPLAZAR AQUI por API real / backend
        try:
            api_url = f"https://tu-backend-api/expediente?num={expediente}&materia={materia}"
            resp = requests.get(api_url, timeout=10)
            data = resp.json()
        except Exception as e:
            st.error("Error al conectar con el servicio.")
            data = {}

        if not data.get("encontrado"):
            st.warning("No se encontró expediente o no tienes permiso de acceso.")
        else:
            # --- MAIN RESULTS ----
            st.markdown(f"### 📊 Estado del expediente: **{expediente}**")
            st.write(f"- **Materia:** {materia}")
            st.write(f"- **Juzgado:** {data.get('juzgado')}")
            st.write(f"- **Estatus actual:** {data.get('estatus')}")
            
            st.markdown("## 📁 Acciones disponibles")
            colA, colB, colC = st.columns(3)
            
            with colA:
                if st.button("📄 Ver Acuerdos"):
                    st.session_state.view = "acuerdos"
            with colB:
                if st.button("📎 Ver Documentos"):
                    st.session_state.view = "docs"
            with colC:
                if st.button("📅 Audiencias"):
                    st.session_state.view = "audiencias"

            st.markdown("---")

            # --- CONDITIONAL CONTENT ---
            view = st.session_state.get("view", None)
            if view == "acuerdos":
                st.markdown("### 📑 Lista de acuerdos:")
                for a in data.get("acuerdos", []):
                    st.write(f"- {a['fecha']} — {a['descripcion']}")

            if view == "docs":
                st.markdown("### 📎 Documentos disponibles:")
                for d in data.get("documentos", []):
                    st.write(f"[📥 {d['nombre']}]({d['url']})")

            if view == "audiencias":
                st.markdown("### 📅 Audiencias programadas:")
                for aud in data.get("audiencias", []):
                    st.write(f"- {aud['fecha']} — {aud['detalle']}")
