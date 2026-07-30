import pandas as pd
import streamlit as st

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Directorio de OSC | CEDHNL",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Carga y limpieza de datos con caché
@st.cache_data
def load_data():
    file_path = "directorio_osc2026.xlsx"
    df = pd.read_excel(file_path)

    # Eliminar columnas irrelevantes si existen
    df = df.drop(columns=["Unnamed: 8"], errors="ignore")

    # Limpieza de campos nulos y espacios
    df["LETRA"] = df["LETRA"].astype(str).str.strip().str.upper()
    df["NOMBRE"] = df["NOMBRE"].astype(str).str.strip()
    df["OBJETO"] = df["OBJETO"].fillna("").astype(str).str.strip()
    df["SERVICIOS"] = df["SERVICIOS"].fillna("").astype(str).str.strip()
    df["UBICACIÓN"] = df["UBICACIÓN"].fillna("").astype(str).str.strip()
    df["TEL"] = df["TEL"].fillna("").astype(str).str.strip()
    df["WEB"] = df["WEB"].fillna("").astype(str).str.strip()

    # Normalización de etiquetas (TAGs)
    df["TAG"] = (
        df["TAG"]
        .fillna("General")
        .astype(str)
        .str.strip()
        .replace({"Pevención de Adicciones": "Prevención de Adicciones"})
    )

    return df


df = load_data()

# Header de la aplicación
st.title("📂 Directorio de Organizaciones de la Sociedad Civil")
st.caption(
    f"Explora y consulta las {len(df)} organizaciones registradas en la base de datos."
)
st.divider()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("🔍 Filtros de Búsqueda")

# 1. Buscador global
search_query = st.sidebar.text_input(
    "Buscar por nombre, servicio o palabra clave:",
    placeholder="Escribe aquí (ej. niños, adicciones, Monterrey)...",
)

# 2. Filtro por Categoría / TAG
categories = ["Todas"] + sorted([t for t in df["TAG"].unique() if t])
selected_tag = st.sidebar.selectbox("Filtrar por Categoría (TAG):", categories)

# 3. Filtro por Abecedario (Letra inicial)
letters = ["Todas"] + sorted([l for l in df["LETRA"].unique() if l])
selected_letter = st.sidebar.selectbox("Filtrar por Letra (A-Z):", letters)

# Reset de filtros
if st.sidebar.button("🧹 Limpiar filtros", use_container_width=True):
    st.rerun()

# --- APLICACIÓN DE FILTROS ---
filtered_df = df.copy()

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["NOMBRE"].str.lower().str.contains(q)
        | filtered_df["OBJETO"].str.lower().str.contains(q)
        | filtered_df["SERVICIOS"].str.lower().str.contains(q)
        | filtered_df["UBICACIÓN"].str.lower().str.contains(q)
    ]

if selected_tag != "Todas":
    filtered_df = filtered_df[filtered_df["TAG"] == selected_tag]

if selected_letter != "Todas":
    filtered_df = filtered_df[filtered_df["LETRA"] == selected_letter]

# --- VISTA PRINCIPAL ---
st.subheader(f"Mostrando {len(filtered_df)} de {len(df)} organizaciones")

# Selector de vista
view_type = st.radio(
    "Modo de visualización:",
    ["🎴 Tarjetas Explorables", "📊 Tabla Completa (Excel)"],
    horizontal=True,
)

st.write("")

if view_type == "🎴 Tarjetas Explorables":
    if filtered_df.empty:
        st.warning(
            "No se encontraron organizaciones que coincidan con los filtros seleccionados."
        )
    else:
        # Renderizar en cuadrícula de 2 columnas
        cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            col = cols[idx % 2]
            with col:
                with st.container(border=True):
                    # Badge de Categoría y Letra
                    st.markdown(
                        f"**:blue[{row['TAG']}]** &nbsp; | &nbsp; **Letra:** `{row['LETRA']}`"
                    )
                    st.markdown(f"### {row['NOMBRE']}")

                    if row["OBJETO"]:
                        st.markdown(f"**Objeto:** {row['OBJETO']}")

                    if row["SERVICIOS"]:
                        st.info(f"**Servicios:** {row['SERVICIOS']}")

                    st.markdown("---")

                    # Detalles de contacto
                    if row["UBICACIÓN"]:
                        st.markdown(f"📍 **Ubicación:** {row['UBICACIÓN']}")

                    if row["TEL"]:
                        st.markdown(f"📞 **Teléfono:** `{row['TEL']}`")

                    if row["WEB"]:
                        st.markdown(f"🌐 **Web / Contacto:** {row['WEB']}")

else:
    # Vista en tabla interactiva estilo Excel
    st.dataframe(
        filtered_df[
            [
                "LETRA",
                "NOMBRE",
                "TAG",
                "SERVICIOS",
                "UBICACIÓN",
                "TEL",
                "WEB",
                "OBJETO",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        height=600,
    )

# Pie de página
st.divider()
st.caption("Directorio de Organizaciones de la Sociedad Civil | CEDHNL")