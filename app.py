import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Directorio OSC - CEDHNL",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------------------------------
# 2. ESTILOS CSS PERSONALIZADOS
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* ENCABEZADO CON LOGO Y TÍTULO */
    .cedh-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding-bottom: 15px;
        border-bottom: 3px solid #003366;
        margin-bottom: 25px;
    }
    .cedh-logo {
        height: 75px;
        width: auto;
    }
    .cedh-title-container {
        display: flex;
        flex-direction: column;
    }
    .cedh-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #003366;
        margin: 0;
        line-height: 1.2;
    }
    .cedh-subtitle {
        font-size: 1.0rem;
        color: #555555;
        margin: 0;
    }

    /* ESTILO FIJO DE LAS FICHAS / CARDS */
    .osc-card {
        background-color: #ffffff;
        border: 1px solid #d1d5db;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        
        /* ALTO FIJO UNIFORME PARA TODAS LAS FICHAS */
        height: 340px;
        
        /* SCROLL EN CONTENIDO QUE SUPERE LA ALTURA */
        overflow-y: auto;
        
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    .osc-card:hover {
        border-color: #003366;
        box-shadow: 0 6px 12px -2px rgba(0, 51, 102, 0.15);
    }

    .osc-nombre {
        font-size: 1.05rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
        border-bottom: 1px solid #f3f4f6;
        padding-bottom: 6px;
    }

    .osc-section-title {
        font-size: 0.78rem;
        font-weight: 700;
        color: #003366;
        text-transform: uppercase;
        margin-top: 6px;
        margin-bottom: 2px;
    }

    .osc-text {
        font-size: 0.85rem;
        color: #374151;
        line-height: 1.35;
        margin-bottom: 6px;
    }

    .osc-tag {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ENCABEZADO CON LOGO DE CEDHNL
# ---------------------------------------------------------
# Nota: Puedes usar la URL directa o la ruta a tu archivo local (ej. "assets/logo_cedhnl.png")
LOGO_URL = "https://www.cedhnl.org.mx/assets/img/logo.png"

st.markdown(f"""
    <div class="cedh-header">
        <img src="{LOGO_URL}" class="cedh-logo" alt="Logo CEDHNL">
        <div class="cedh-title-container">
            <h1 class="cedh-title">Comisión Estatal de Derechos Humanos de Nuevo León</h1>
            <p class="cedh-subtitle">Directorio de Organizaciones de la Sociedad Civil (OSC)</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 4. CARGA Y PROCESAMIENTO DE DATOS
# ---------------------------------------------------------
@st.cache_data
def cargar_datos():
    # Cargar archivo CSV / Excel del directorio de OSC
    # Reemplaza 'directorio_osc.xlsx' o 'directorio_osc.csv' por tu ruta real
    try:
        df = pd.read_excel("directorio_osc.xlsx")
    except Exception:
        # Ejemplo de respaldo por si no encuentra el archivo local
        df = pd.DataFrame([
            {
                "NOMBRE": "Academia Libre de Derechos Humanos, A.C.",
                "OBJETO": "Divulgar el saber y el libre debate de las ideas sobre los Derechos Humanos como un pilar indiscutible en la lucha por la dignidad y la igualdad.",
                "SERVICIOS": "Divulgación y enseñanza de los derechos humanos a través de medios electrónicos.",
                "UBICACIÓN": "Calle Gral. Carlos Salazar Pte. 745, Centro, 64000 Monterrey, N.L.",
                "TEL": "812927 0610",
                "WEB": "aldh.edu.mx@gmail.com | https://aldh.mx",
                "TAG": "Jóvenes / Educación"
            },
            {
                "NOMBRE": "Acciona e Incluye, S.A.S de C.V.",
                "OBJETO": "Realizar actividades de investigación y desarrollo en ciencias sociales y humanidades, apoyar con consultorías y brindar servicios de traducción e interpretación.",
                "SERVICIOS": "Interpretación simultánea de Lengua de Señas Mexicana (LSM), talleres de sensibilización y plataformas educativas.",
                "UBICACIÓN": "Miguel Ángel 451, Col. Misión Real, Apodaca, N.L.",
                "TEL": "8110661698",
                "WEB": "inclusionmonterrey@gmail.com",
                "TAG": "Discapacidad / LSM"
            },
            {
                "NOMBRE": "ACODEMIS, A.C.",
                "OBJETO": "Luchar contra las prácticas de discriminación laboral, educativas, políticas de seguridad, asistencia jurídica y de salud de las minorías sexuales.",
                "SERVICIOS": "Pruebas rápidas para detección de VIH, SÍFILIS y HEPATITIS C en sus centros comunitarios.",
                "UBICACIÓN": "Washington 947 Ote. / Villagrán 637 Nte., Monterrey, N.L.",
                "TEL": "8183450927",
                "WEB": "acodemis@gmail.com | http://www.acodemis.org",
                "TAG": "Salud / VIH"
            }
        ])
    return df

df = cargar_datos()

# Búsqueda / Filtro opcional
busqueda = st.text_input("🔍 Buscar por Nombre, Servicio o Clasificación:", "")

if busqueda:
    df_filtrado = df[
        df['NOMBRE'].str.contains(busqueda, case=False, na=False) |
        df['SERVICIOS'].str.contains(busqueda, case=False, na=False) |
        df['TAG'].str.contains(busqueda, case=False, na=False)
    ]
else:
    df_filtrado = df


# ---------------------------------------------------------
# 5. RENDERIZADO DE FICHAS UNIFORMES (3 COLUMNAS)
# ---------------------------------------------------------
cols_per_row = 3
cols = st.columns(cols_per_row)

for idx, (_, row) in enumerate(df_filtrado.iterrows()):
    col = cols[idx % cols_per_row]
    
    # Preparación de valores seguros
    nombre = row.get("NOMBRE", "Sin nombre")
    objeto = row.get("OBJETO", "No especificado")
    servicios = row.get("SERVICIOS", "No especificado")
    ubicacion = row.get("UBICACIÓN", "No disponible")
    telefono = row.get("TEL", "Sin teléfono")
    web_correo = row.get("WEB", "Sin contacto")
    tag = row.get("TAG", "General")

    with col:
        # Estructura estandarizada idéntica para todas las fichas
        st.markdown(f"""
            <div class="osc-card">
                <div>
                    <div class="osc-nombre">{nombre}</div>
                    
                    <div class="osc-section-title">Objeto Social</div>
                    <div class="osc-text">{objeto}</div>
                    
                    <div class="osc-section-title">Servicios</div>
                    <div class="osc-text">{servicios}</div>
                    
                    <div class="osc-section-title">Ubicación y Contacto</div>
                    <div class="osc-text">📍 {ubicacion}</div>
                    <div class="osc-text">📞 {telefono} | ✉️ {web_correo}</div>
                </div>
                
                <div>
                    <span class="osc-tag">🏷️ {tag}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
