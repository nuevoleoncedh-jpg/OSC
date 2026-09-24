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

# 3. Estilos CSS (Actualizados con más color)
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

    /* --- ESTILO PARA TARJETAS CON MÁS COLOR --- */
    .card-osc {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        padding: 22px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.08);
        margin-bottom: 20px;
        height: 480px;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        border: 1px solid #e2e8f0;
        border-left: 6px solid #10b981; /* Borde izquierdo verde vibrante */
    }
    .card-osc:hover { 
        transform: translateY(-6px); 
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.15);
        border-color: #cbd5e1;
        border-left-color: #059669;
    }

    .tag-premium {
        background-color: #d1fae5;
        color: #047857;
        padding: 5px 12px;
        border-radius: 100px;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        border: 1px solid #a7f3d0;
        margin-bottom: 10px;
        width: fit-content;
    }

    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 10px;
        height: 48px;
        line-height: 1.2;
        overflow: hidden;
    }

    /* Estilo para Objeto con bloque de color */
    .card-desc {
        font-size: 0.98rem;
        color: #1e293b;
        line-height: 1.45;
        margin-bottom: 10px;
        background-color: #f0fdf4;
        padding: 8px 12px;
        border-radius: 10px;
        border-left: 3px solid #34d399;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* Estilo para Servicios con bloque de color */
    .card-services {
        font-size: 0.98rem;
        color: #1e293b;
        line-height: 1.45;
        margin-bottom: 12px;
        background-color: #f0f9ff;
        padding: 8px 12px;
        border-radius: 100px;
        border-radius: 10px;
        border-left: 3px solid #38bdf8;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .card-info {
        font-size: 0.85rem;
        border-top: 1px dashed #cbd5e1;
        padding-top: 10px;
        color: #475569;
        line-height: 1.5;
        margin-top: auto;
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
    total_con_web = df[df['web'].notna() & (df['web'] != '#')].shape[0] if 'web' in df.columns else 0

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
            df['letra'] = df['nombre'].dropna().astype(str).str[0].str.upper()
            letras_unicas = sorted([str(l) for l in df['letra'].dropna().unique() if str(l).strip() and str(l).lower() != 'nan'])
            letra_sel = st.pills("Inicial:", ["Todas"] + letras_unicas, default="Todas")
        else:
            letra_sel = "Todas"

    # Aplicar Filtros
    df_f = df.copy()
    if busqueda:
        df_f = df_f[df_f.apply(lambda r: busqueda.lower() in str(r).lower(), axis=1)]
    if 'letra' in df_f.columns and letra_sel != "Todas":
        df_f = df_f[df_f['letra'] == letra_sel]

    # --- 7. LISTADO DE TARJETAS ---
    st.write(f"Mostrando **{len(df_f)}** resultados")
    
    for i in range(0, len(df_f), 3):
        cols = st.columns(3)
        batch = df_f.iloc[i:i+3].to_dict('records')
        
        for idx, row in enumerate(batch):
            with cols[idx]:
                objeto_txt = str(row.get('objeto', row.get('desc', 'Sin descripción.')))
                servicios_txt = str(row.get('servicios', 'No especificados'))
                ubicacion = row.get('ubicación', row.get('ubicacion', 'N/A'))
                telefono = row.get('tel', 'N/A')
                
                st.markdown(f"""
                    <div class="card-osc">
                        <div class="tag-premium">{row.get('tag', 'General')}</div>
                        <div class="card-title">{row.get('nombre', 'S/N')}</div>
                        <div class="card-desc">
                            🎯 <b style="color: #0f766e;">Objeto:</b> {objeto_txt[:180]}
                        </div>
                        <div class="card-services">
                            🤝 <b style="color: #0369a1;">Servicios:</b> {servicios_txt[:180]}
                        </div>
                        <div class="card-info">
                            📍 <b>Dirección:</b> {ubicacion}<br>
                            📞 <b>Tel:</b> {telefono}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.error("No se pudo cargar el listado. Verifica el archivo CSV.")
