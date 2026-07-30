import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuración de página
st.set_page_config(page_title="Directorio OSC | CEDHNL", layout="wide")

# 2. Función de carga de datos
def cargar_datos():
    archivo = "directorio_osc.csv"
    if not os.path.exists(archivo):
        st.error(f"⚠️ No se encontró el archivo '{archivo}'")
        return pd.DataFrame()
    
    for enc in ['utf-8', 'latin-1', 'cp1252']:
        for sep in [',', ';']:
            try:
                df = pd.read_csv(archivo, encoding=enc, sep=sep)
                if len(df.columns) > 1:
                    df.columns = df.columns.str.strip().str.lower()
                    return df
            except:
                continue
    return pd.DataFrame()

df = cargar_datos()

# 3. Estilos CSS (Corregido: faltaba st.markdown al inicio)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }

    .header-premium {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 40px;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    /* --- ESTILO PARA KPIs --- */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        flex: 1;
        text-align: center;
        border: 1px solid #f1f5f9;
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #10b981;
        line-height: 1;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* --- ESTILO PARA TARJETAS COMPACTAS --- */
    .card-osc {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        height: 380px;
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease;
        border: 1px solid #f1f5f9;
    }
    .card-osc:hover { transform: translateY(-5px); }

    .tag-premium {
        background-color: #ecfdf5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 100px;
        font-weight: 700;
        font-size: 10px;
        text-transform: uppercase;
        border: 1px solid #a7f3d0;
        margin-bottom: 8px;
        width: fit-content;
    }

    .card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
        height: 50px;
        line-height: 1.2;
        overflow: hidden;
    }

    .card-desc {
        font-size: 0.85rem;
        color: #64748b;
        flex-grow: 1;
        overflow: hidden;
        margin-bottom: 12px;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
    }

    .card-info {
        font-size: 0.8rem;
        border-top: 1px solid #f1f5f9;
        padding-top: 12px;
        color: #475569;
        line-height: 1.4;
    }

    .btn-web {
        display: block;
        background: #10b981;
        color: white !important;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        text-decoration: none;
        margin-top: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .section-title {
        font-weight: 700;
        color: #0f172a;
        margin: 20px 0;
        border-left: 5px solid #10b981;
        padding-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Header
st.markdown("""
    <div class="header-premium">
        <h1 style="margin:0; font-size: 3rem;">CEDHNL</h1>
        <p style="margin:10px 0 0 0; opacity:0.9;">Directorio de Organizaciones de la Sociedad Civil</p>
    </div>
    """, unsafe_allow_html=True)

if not df.empty:
    # --- 5. DASHBOARD ---
    st.markdown('<h2 class="section-title">Análisis de la Red de Apoyo</h2>', unsafe_allow_html=True)
    
    total_osc = len(df)
    total_ejes = df['tag'].nunique() if 'tag' in df.columns else "N/A"
    total_con_web = df[df['web'].notna() & (df['web'] != '#')].shape[0]

    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-value">{total_osc}</div>
                <div class="kpi-label">Organizaciones<br>Registradas</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{total_ejes}</div>
                <div class="kpi-label">Ejes de<br>Atención</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{total_con_web}</div>
                <div class="kpi-label">Con Enlace<br>Digital</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 6. FILTROS ---
    st.markdown('<h2 class="section-title">Directorio Interactivo</h2>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        busqueda = st.text_input("🔍 Buscar por nombre o palabra clave...", placeholder="Ej: Salud, Mujer, Monterrey")
    with c2:
        if 'nombre' in df.columns:
            df['letra'] = df['nombre'].astype(str).str[0].str.upper()
            letra_sel = st.pills("Inicial:", ["Todas"] + sorted(df['letra'].unique().astype(str)), default="Todas")
        else:
            letra_sel = "Todas"

    # Aplicar Filtros
    df_f = df.copy()
    if busqueda:
        df_f = df_f[df_f.apply(lambda r: busqueda.lower() in str(r).lower(), axis=1)]
    if letra_sel != "Todas":
        df_f = df_f[df_f['letra'] == letra_sel]

    # --- 7. LISTADO DE TARJETAS (COMPACTAS) ---
    st.write(f"Mostrando **{len(df_f)}** resultados")
    
    for i in range(0, len(df_f), 3):
        cols = st.columns(3)
        batch = df_f.iloc[i:i+3].to_dict('records')
        
        for idx, row in enumerate(batch):
            with cols[idx]:
                web = str(row.get('web', '#'))
                if web != "#" and not web.startswith('http'): 
                    web = "https://" + web
                
                st.markdown(f"""
                    <div class="card-osc">
                        <div class="tag-premium">{row.get('tag', 'General')}</div>
                        <div class="card-title">{row.get('nombre', 'S/N')}</div>
                        <div class="card-desc">{row.get('desc', 'Sin descripción.')[:150]}...</div>
                        <div class="card-info">
                            📍 <b>Dirección:</b> {row.get('ubicacion', 'N/A')}<br>
                            📞 <b>Tel:</b> {row.get('tel', 'N/A')}
                        </div>
                        <a href="{web}" target="_blank" class="btn-web">Ver sitio web</a>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.error("No se pudo cargar el listado. Verifica el archivo CSV.")