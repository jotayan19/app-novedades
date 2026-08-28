import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import io
import requests
import base64

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="SISTEMA DE NOVEDADES",
    page_icon="👮‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Moderno tipo Dashboard
st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    
    /* Sidebar moderno */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 2px solid #10b981;
    }
    
    /* Header con logo */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 30px;
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
        border-radius: 20px;
        margin: 20px auto;
        max-width: 900px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
        border: 2px solid #10b981;
    }
    
    .header-logo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #0f172a;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 3px solid #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
    }
    
    .header-text h1 {
        color: #10b981;
        font-size: 2em;
        margin: 0;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
    }
    
    .header-text p {
        color: #94a3b8;
        margin: 5px 0 0 0;
        font-size: 0.9em;
        text-align: center;
    }
    
    /* Login Card moderna - CENTRADA */
    .login-container {
        max-width: 500px;
        margin: 80px auto;
        padding: 0 20px;
    }
    
    .login-card {
        padding: 50px 40px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border-radius: 25px;
        box-shadow: 0 15px 50px rgba(16, 185, 129, 0.3);
        border: 3px solid #10b981;
        text-align: center;
    }
    
    .login-icon {
        font-size: 4em;
        margin-bottom: 20px;
    }
    
    .login-title {
        font-size: 2.2em;
        font-weight: bold;
        color: #10b981;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    
    .login-subtitle {
        color: #94a3b8;
        margin-bottom: 40px;
        font-style: italic;
        font-size: 0.95em;
    }
    
    /* Tarjetas de estadísticas */
    .stat-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 10px 0;
        border: 2px solid #10b981;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .stat-value {
        font-size: 2.5em;
        font-weight: bold;
        color: #10b981;
        margin: 10px 0;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Botones modernos */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        padding: 12px 30px !important;
        font-size: 1.1em !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Inputs modernos */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div, 
    .stTextArea > div > div > textarea {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 2px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1em !important;
    }
    
    .stTextInput > div > div > input:focus, 
    .stSelectbox > div > div > div:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.5) !important;
    }
    
    /* Dataframes */
    .dataframe {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: bold;
        padding: 12px;
    }
    
    .dataframe td {
        background-color: #0f172a !important;
        padding: 10px;
    }
    
    /* Tabs modernos */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #1e293b;
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #0f172a;
        border-radius: 10px;
        color: #94a3b8;
        padding: 12px 25px;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: 2px solid #4CAF50;
    }
    
    /* Métricas */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #10b981;
    }
    
    [data-testid="stMetricValue"] {
        color: #10b981 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    /* Footer */
    .main-footer {
        text-align: center;
        padding: 25px;
        margin-top: 50px;
        color: #64748b;
        border-top: 2px solid #10b981;
    }
    
    /* Sidebar */
    .sidebar-header {
        color: #10b981;
        font-size: 1.2em;
        font-weight: bold;
        margin: 20px 0 15px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-align: center;
    }
    
    /* Hora en sidebar */
    .clock-box {
        text-align: center;
        padding: 15px;
        background: #0f172a;
        border-radius: 12px;
        border: 2px solid #10b981;
        margin: 10px 0;
    }
    
    .clock-label {
        color: #94a3b8;
        font-size: 0.85em;
        margin-bottom: 5px;
    }
    
    .clock-value {
        color: #10b981;
        font-size: 1.6em;
        font-weight: bold;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONSTANTES ====================
USUARIO_CORRECTO = "DRAGJOTAYANLEONEL"
CONTRASENA_CORRECTA = "Drag2026"

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
REPO_OWNER = "jotayan19"
REPO_NAME = "app-novedades"
BRANCH = "main"
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents"

NOMBRES_ARCHIVOS = {
    'empleados': 'empleados.csv', 'horarios': 'horarios.csv',
    'novedades': 'novedades.csv', 'racionamiento': 'racionamiento.csv',
    'plan_llamada': 'plan_llamada.csv'
}

AULAS_TERCER_ANO = ["23 TT", "18 TM", "23 TM", "24 TM", "26 TM", "28 TM"]
AULAS_CAO = ["7 TT", "8 TT"]
AULAS = AULAS_TERCER_ANO + AULAS_CAO

OPCIONES_HORARIO = ["", "06:20", "07:30", "08:10", "08:30", "09:20", "09:30", "10:30", "13:50", "15:10", "16:40", "apresto en domicilio"]

MOTIVOS = {
    "Ausente fuera de la escuela": ["SSD", "ART", "DESCANSO DE GUARDIA", "A CUENTA DE LAO", "AUTORIZADO", "LES"],
    "Presente pero fuera del escuadron": ["GUARDIA DIURNA", "GUARDIA NOCTURNA", "FORMACION", "PRACTICA DE DESFILE"]
}

# ==================== FUNCIONES DE GITHUB ====================
def get_github_file_sha(filename):
    if not GITHUB_TOKEN: return None
    url = f"{BASE_URL}/{filename}?ref={BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json().get("sha")
    except: pass
    return None

def save_to_github(filename, content_str):
    if not GITHUB_TOKEN: return False
    url = f"{BASE_URL}/{filename}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    content_b64 = base64.b64encode(content_str.encode('utf-8')).decode('utf-8')
    sha = get_github_file_sha(filename)
    payload = {
        "message": f"Auto-save: {filename}",
        "content": content_b64,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha
    try:
        resp = requests.put(url, json=payload, headers=headers)
        return resp.status_code in [200, 201]
    except Exception as e:
        st.error(f"Error guardando en GitHub: {e}")
        return False

def load_from_github(filename):
    if not GITHUB_TOKEN: return []
    url = f"{BASE_URL}/{filename}?ref={BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            content_b64 = data.get("content", "")
            decoded = base64.b64decode(content_b64).decode('utf-8')
            reader = csv.reader(decoded.splitlines())
            return [row for row in reader if row]
    except: pass
    return []

# ==================== FUNCIONES AUXILIARES ====================
def cargar_csv_inicial(nombre_referencia):
    try:
        with open(nombre_referencia, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return [row for row in reader if row]
    except:
        return []

def convertir_a_csv(datos):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(datos)
    return output.getvalue()

def normalizar_motivo(motivo):
    if not motivo: return motivo
    return str(motivo).strip().upper()

def determinar_curso(grado):
    grado_upper = str(grado).upper()
    if "DRAG" in grado_upper or "DRAGONEANTE" in grado_upper or "III" in grado_upper:
        return "Tercer Año"
    return "Auxiliar Operativo"

def obtener_grado_abreviado(nombre):
    empleados = st.session_state.get('empleados', [])
    for emp in empleados:
        if len(emp) >= 2 and emp[1].upper().strip() == nombre.upper().strip():
            curso = determinar_curso(emp[0])
            return "ASP III" if curso == "Tercer Año" else "ASP I"
    return "ASP I"

def obtener_nombre_completo(nombre_buscado):
    empleados = st.session_state.get('empleados', [])
    for emp in empleados:
        if len(emp) >= 2 and emp[1].upper().strip() == nombre_buscado.upper().strip():
            return emp[1].upper()
    return nombre_buscado.upper()

def obtener_horario_aula(aula):
    horarios = st.session_state.get('horarios', [])
    aula_upper = aula.strip().upper()
    aula_base = aula_upper.split('(')[0].strip()
    for hor in horarios:
        if len(hor) >= 2:
            hor_aula = hor[0].strip().upper()
            hor_aula_base = hor_aula.split('(')[0].strip()
            if hor_aula_base == aula_base:
                return hor[1]
    return ""

def numero_a_texto(numero):
    numeros = {
        0: "CERO (00)", 1: "UNO (01)", 2: "DOS (02)", 3: "TRES (03)", 4: "CUATRO (04)",
        5: "CINCO (05)", 6: "SEIS (06)", 7: "SIETE (07)", 8: "OCHO (08)",
        9: "NUEVE (09)", 10: "DIEZ (10)", 11: "ONCE (11)", 12: "DOCE (12)",
        13: "TRECE (13)", 14: "CATORCE (14)", 15: "QUINCE (15)", 16: "DIECISEIS (16)",
        17: "DIECISIETE (17)", 18: "DIECIOCHO (18)", 19: "DIECINUEVE (19)", 20: "VEINTE (20)",
        21: "VEINTIUNO (21)", 22: "VEINTIDOS (22)", 23: "VEINTITRES (23)", 24: "VEINTICUATRO (24)",
        25: "VEINTICINCO (25)", 41: "CUARENTA Y UNO (41)"
    }
    return numeros.get(numero, f"{numero:02d}")

def calcular_estadisticas():
    empleados = st.session_state.get('empleados', [])
    novedades = st.session_state.get('novedades', [])
    hoy = datetime.now().strftime("%d/%m/%Y")
    
    novedades_norm = []
    for n in novedades:
        if len(n) >= 5:
            n_copy = list(n)
            n_copy[2] = normalizar_motivo(n_copy[2])
            novedades_norm.append(n_copy)
        else:
            novedades_norm.append(n)
    
    novedades_hoy = [n for n in novedades_norm if len(n) >= 5 and n[4] == hoy]
    
    if not empleados: return None
    
    total_general = len(empleados)
    total_3 = sum(1 for e in empleados if determinar_curso(e[0]) == "Tercer Año")
    total_cao = sum(1 for e in empleados if determinar_curso(e[0]) == "Auxiliar Operativo")
    
    ausentes_novedades = len(novedades_hoy)
    ausentes_apresto = sum(1 for e in empleados if len(e) >= 5 and obtener_horario_aula(e[4]) == "apresto en domicilio")
    ausentes_total = ausentes_novedades + ausentes_apresto
    presentes_total = total_general - ausentes_total
    
    ausentes_3 = sum(1 for n in novedades_hoy if determinar_curso(n[0]) == "Tercer Año")
    ausentes_3 += sum(1 for e in empleados if determinar_curso(e[0]) == "Tercer Año" and len(e) >= 5 and obtener_horario_aula(e[4]) == "apresto en domicilio")
    
    ausentes_cao = sum(1 for n in novedades_hoy if determinar_curso(n[0]) == "Auxiliar Operativo")
    ausentes_cao += sum(1 for e in empleados if determinar_curso(e[0]) == "Auxiliar Operativo" and len(e) >= 5 and obtener_horario_aula(e[4]) == "apresto en domicilio")
    
    presentes_3 = total_3 - ausentes_3
    presentes_cao = total_cao - ausentes_cao
    
    aulas_dict = {}
    for emp in empleados:
        if len(emp) >= 5:
            nombre = emp[1]
            aula = emp[4].strip().upper()
            curso = determinar_curso(emp[0])
            horario = obtener_horario_aula(aula)
            
            if aula not in aulas_dict:
                aulas_dict[aula] = {"total": 0, "ausentes": 0, "horario": horario, "curso": curso}
            
            aulas_dict[aula]["total"] += 1
            tiene_novedad = any(n[0].upper().strip() == nombre.upper().strip() for n in novedades_hoy)
            if tiene_novedad or horario == "apresto en domicilio":
                aulas_dict[aula]["ausentes"] += 1
    
    presentes_0620 = sum(1 for e in empleados if len(e) >= 5 and obtener_horario_aula(e[4]) == "06:20" and not any(n[0].upper().strip() == e[1].upper().strip() for n in novedades_hoy))
    
    aulas_diferenciado = {}
    total_diferenciado = 0
    for aula, info in aulas_dict.items():
        horario = info["horario"]
        if horario and horario != "06:20" and horario != "apresto en domicilio":
            presentes_aula = info["total"] - info["ausentes"]
            aulas_diferenciado[aula] = {"total": presentes_aula, "horario": horario, "curso": info["curso"]}
            total_diferenciado += presentes_aula
    
    aulas_apresto = {aula: info["total"] for aula, info in aulas_dict.items() if info["horario"] == "apresto en domicilio"}
    total_apresto = sum(aulas_apresto.values())
    
    return {
        "total_general": total_general, "total_3": total_3, "total_cao": total_cao,
        "presentes_total": presentes_total, "presentes_3": presentes_3, "presentes_cao": presentes_cao,
        "ausentes_total": ausentes_total, "ausentes_3": ausentes_3, "ausentes_cao": ausentes_cao,
        "presentes_0620": presentes_0620, "aulas_dict": aulas_dict, "novedades_hoy": novedades_hoy,
        "total_diferenciado": total_diferenciado, "aulas_diferenciado": aulas_diferenciado,
        "total_apresto": total_apresto, "aulas_apresto": aulas_apresto
    }

# ==================== LOGIN CENTRADO ====================
def pantalla_login():
    # Header con logo centrado
    st.markdown("""
    <div class="main-header">
        <div class="header-logo">
            <div style="font-size: 3em;">⚔</div>
        </div>
        <div class="header-text">
            <h1>SISTEMA DE NOVEDADES</h1>
            <p>ESCUADRÓN H "CABO MARCELO GODOY" - AÑO 2026</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login centrado
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-icon"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">ACCESO RESTRINGIDO</div>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">NOVEDADES ESCUADRÓN H "CABO MARCELO GODOY"</p>', unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        usuario = st.text_input("👤 Usuario", placeholder="Ingrese su usuario")
        contrasena = st.text_input("🔒 Contraseña", type="password", placeholder="Ingrese su contraseña")
        submitted = st.form_submit_button("🚀 INGRESAR AL SISTEMA")
        
        if submitted:
            if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:
                st.session_state['logueado'] = True
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #64748b; margin-top: 30px; font-size: 0.85em;">Sistema de Gendarmería Nacional Argentina © 2026</div>', unsafe_allow_html=True)

# ==================== INICIALIZACIÓN ====================
if 'logueado' not in st.session_state: st.session_state['logueado'] = False
if not st.session_state['logueado']:
    pantalla_login()
    st.stop()

if 'empleados' not in st.session_state: 
    data = load_from_github(NOMBRES_ARCHIVOS['empleados'])
    st.session_state['empleados'] = data if data else cargar_csv_inicial(NOMBRES_ARCHIVOS['empleados'])
if 'horarios' not in st.session_state: 
    data = load_from_github(NOMBRES_ARCHIVOS['horarios'])
    st.session_state['horarios'] = data if data else cargar_csv_inicial(NOMBRES_ARCHIVOS['horarios'])
if 'novedades' not in st.session_state: 
    data = load_from_github(NOMBRES_ARCHIVOS['novedades'])
    st.session_state['novedades'] = data if data else cargar_csv_inicial(NOMBRES_ARCHIVOS['novedades'])
if 'racionamiento' not in st.session_state: 
    data = load_from_github(NOMBRES_ARCHIVOS['racionamiento'])
    st.session_state['racionamiento'] = data if data else cargar_csv_inicial(NOMBRES_ARCHIVOS['racionamiento'])
if 'plan_llamada' not in st.session_state: st.session_state['plan_llamada'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['plan_llamada'])
if 'nov_counter' not in st.session_state: st.session_state['nov_counter'] = 0
if 'rac_counter' not in st.session_state: st.session_state['rac_counter'] = 0

# ==================== HEADER ====================
st.markdown("""
<div class="main-header">
    <div class="header-logo">
        <div style="font-size: 3em;">👮‍♂️</div>
    </div>
    <div class="header-text">
        <h1>SISTEMA DE NOVEDADES</h1>
        <p>ESCUADRÓN H "CABO MARCELO GODOY" - AÑO 2026</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div class="sidebar-header">📊 PANEL DE CONTROL</div>', unsafe_allow_html=True)
    
    # Fecha y Hora
    ahora = datetime.now()
    st.markdown('<div class="clock-box">', unsafe_allow_html=True)
    st.markdown('<div class="clock-label">📅 Fecha</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="clock-value">{ahora.strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="clock-box" style="margin-top: 10px;">', unsafe_allow_html=True)
    st.markdown('<div class="clock-label">🕐 Hora</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="clock-value">{ahora.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    stats = calcular_estadisticas()
    if stats:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">👥 FUERZA EFECTIVA</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{stats["total_general"]}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.metric("✅ Presentes", stats["presentes_total"])
        st.metric("📋 Ausentes", stats["ausentes_total"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">📚 POR CURSO</div>', unsafe_allow_html=True)
        st.metric(" Tercer Año", f"{stats['presentes_3']}/{stats['total_3']}")
        st.metric("🛡️ Aux. Operativo", f"{stats['presentes_cao']}/{stats['total_cao']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="sidebar-header">💾 GUARDADO</div>', unsafe_allow_html=True)
    if GITHUB_TOKEN:
        st.success("✅ Auto-guardado activado")
    else:
        st.warning("⚠️ Sin token GitHub")
        if st.download_button("📥 Descargar respaldo", data=convertir_a_csv(st.session_state['empleados']), file_name="empleados.csv", mime="text/csv", use_container_width=True): pass
    
    st.markdown("---")
    if st.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
        st.session_state['logueado'] = False
        st.rerun()

# ==================== PESTAÑAS ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    " Personal", "🏫 Aulas/Horarios", "📞 Plan Llamada", "📋 Novedades", "🍽️ Racionamiento", "📊 FE por Aula", "📝 Reportes"
])

# ==================== TAB 1: PERSONAL ====================
with tab1:
    st.header("👥 Gestión de Personal")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.subheader(" Importar Excel")
        archivo_excel = st.file_uploader("Selecciona archivo Excel", type=['xlsx', 'xls'], key="excel_personal")
        if archivo_excel is not None:
            if st.button("💾 Importar Personal", type="primary", use_container_width=True):
                try:
                    df = pd.read_excel(archivo_excel)
                    df.columns = [str(c).strip().upper() for c in df.columns]
                    empleados = []
                    for _, row in df.iterrows():
                        grado = str(row.get('GRADO', '')).strip()
                        nombre = str(row.get('APELLIDO Y NOMBRE', '')).strip()
                        dni = str(row.get('DNI', '')).strip()
                        ce = str(row.get('CE', '')).strip()
                        aula = str(row.get('AULA', '')).strip().upper()
                        if grado and nombre and str(grado).upper() != 'GRADO':
                            empleados.append([grado, nombre, dni, ce, aula])
                    if empleados:
                        st.session_state['empleados'] = empleados
                        if GITHUB_TOKEN:
                            save_to_github(NOMBRES_ARCHIVOS['empleados'], convertir_a_csv(empleados))
                        st.success(f"✅ Se importaron {len(empleados)} empleados")
                        st.rerun()
                except Exception as e: st.error(f"Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.subheader("📋 Personal Registrado")
        empleados = st.session_state.get('empleados', [])
        if empleados:
            df_empleados = pd.DataFrame(empleados, columns=['Grado', 'Apellido y Nombre', 'DNI', 'CE', 'Aula'])
            st.dataframe(df_empleados, use_container_width=True, height=400)
        else: st.info("No hay personal registrado.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: HORARIOS ====================
with tab2:
    st.header(" Configuración de Horarios")
    st.info(f"AULAS: {', '.join(AULAS)}")
    
    horarios_actuales = st.session_state.get('horarios', [])
    horarios_dict = {h[0].upper(): h[1] for h in horarios_actuales if len(h) >= 2}
    
    with st.form("form_horarios"):
        nuevos_horarios = []
        cols = st.columns(2)
        for i, aula in enumerate(AULAS):
            with cols[i % 2]:
                horario_actual = horarios_dict.get(aula.upper(), "")
                index_val = 0
                if horario_actual in OPCIONES_HORARIO: 
                    index_val = OPCIONES_HORARIO.index(horario_actual)
                horario = st.selectbox(f"AULA {aula}", OPCIONES_HORARIO, index=index_val, key=f"horario_{aula}")
                if horario: nuevos_horarios.append([aula.upper(), horario])
        
        if st.form_submit_button("💾 Guardar Horarios", type="primary", use_container_width=True):
            st.session_state['horarios'] = nuevos_horarios
            if GITHUB_TOKEN:
                save_to_github(NOMBRES_ARCHIVOS['horarios'], convertir_a_csv(nuevos_horarios))
            st.success("✅ Horarios guardados")
            st.rerun()

# ==================== TAB 3: PLAN LLAMADA ====================
with tab3:
    st.header("📞 Plan de Llamada")
    empleados = st.session_state.get('empleados', [])
    if empleados:
        nombres = [f"{e[0]} - {e[1]}" for e in empleados]
        empleado_sel = st.selectbox("Seleccionar Aspirante:", [""] + nombres)
        if empleado_sel:
            nombre = empleado_sel.split(" - ", 1)[1]
            st.write(f"**Nombre:** {nombre}")

# ==================== TAB 4: NOVEDADES ====================
with tab4:
    st.header("📋 Registro de Novedades")
    empleados = st.session_state.get('empleados', [])
    hoy = datetime.now().strftime("%d/%m/%Y")
    
    if empleados:
        nombres = [f"{e[0]} - {e[1]}" for e in empleados]
        col1, col2 = st.columns(2)
        with col1:
            empleado_sel = st.selectbox("🔍 Buscar Empleado:", [""] + nombres, key=f"nov_emp_{st.session_state['nov_counter']}")
            categoria = st.selectbox("📂 Categoría:", [""] + list(MOTIVOS.keys()), key="nov_cat")
        with col2:
            motivos_disponibles = MOTIVOS.get(categoria, [])
            motivo = st.selectbox("📌 Motivo:", [""] + motivos_disponibles, key="nov_mot")
            observaciones = st.text_area(" Observaciones:", height=100, key="nov_obs")
        
        if st.button(" Guardar Novedad", type="primary", use_container_width=True):
            if empleado_sel and categoria and motivo:
                nombre = empleado_sel.split(" - ", 1)[1]
                nueva_novedad = [nombre, categoria, normalizar_motivo(motivo), observaciones, hoy]
                st.session_state['novedades'].append(nueva_novedad)
                st.session_state['nov_counter'] += 1
                if GITHUB_TOKEN:
                    save_to_github(NOMBRES_ARCHIVOS['novedades'], convertir_a_csv(st.session_state['novedades']))
                st.success("✅ Novedad guardada")
                st.rerun()

# ==================== TAB 5: RACIONAMIENTO ====================
with tab5:
    st.header("🍽️ Registro de Racionamiento")
    empleados = st.session_state.get('empleados', [])
    hoy = datetime.now().strftime("%d/%m/%Y")
    
    if empleados:
        nombres = [f"{e[0]} - {e[1]}" for e in empleados]
        col1, col2 = st.columns(2)
        with col1:
            empleado_sel = st.selectbox("🔍 Buscar Empleado:", [""] + nombres, key=f"rac_emp_{st.session_state['rac_counter']}")
        with col2:
            observaciones = st.text_input("📝 Observaciones:", key="rac_obs")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("💾 Guardar Almuerzo", type="primary", use_container_width=True):
                if empleado_sel:
                    nombre = empleado_sel.split(" - ", 1)[1]
                    st.session_state['racionamiento'].append([nombre, "Almuerzo", observaciones, hoy])
                    st.session_state['rac_counter'] += 1
                    if GITHUB_TOKEN:
                        save_to_github(NOMBRES_ARCHIVOS['racionamiento'], convertir_a_csv(st.session_state['racionamiento']))
                    st.success("✅ Almuerzo registrado")
                    st.rerun()

# ==================== TAB 6: FE POR AULA ====================
with tab6:
    st.header("📊 Fuerza Efectiva por Aula")
    stats = calcular_estadisticas()
    if stats and stats['aulas_dict']:
        datos = [{"Aula": a, "FE": i["total"], "Horario": i["horario"] or "Sin asignar", "P": i["total"]-i["ausentes"], "A": i["ausentes"]} for a, i in sorted(stats["aulas_dict"].items())]
        st.dataframe(pd.DataFrame(datos), use_container_width=True)

# ==================== TAB 7: REPORTES ====================
with tab7:
    st.header("📝 Reportes y Minutas")
    if st.button("🔄 Generar Minuta Institucional", type="primary", use_container_width=True):
        stats = calcular_estadisticas()
        if not stats: st.error("No hay datos")
        else:
            fecha_minuta = datetime.now().strftime("%d/%m/%Y")
            todas_novedades = stats["novedades_hoy"]
            racionamiento = st.session_state.get('racionamiento', [])
            rac_hoy = [r for r in racionamiento if len(r) >= 4 and r[3] == fecha_minuta]
            
            cant_ssd = len([n for n in todas_novedades if n[2] == "SSD"])
            cant_aut = len([n for n in todas_novedades if n[2] == "AUTORIZADO"])
            cant_lao_cuenta = len([n for n in todas_novedades if n[2] == "A CUENTA DE LAO"])
            cant_lao26 = len([n for n in todas_novedades if n[2] == "LAO"])
            cant_les = len([n for n in todas_novedades if n[2] == "LES"])
            cant_descanso = len([n for n in todas_novedades if n[2] == "DESCANSO DE GUARDIA"])
            cant_guardia_diur = len([n for n in todas_novedades if n[2] == "GUARDIA DIURNA"])
            
            def obtener_lista_enumerada(motivo):
                nombres = [n for n in todas_novedades if n[2] == motivo]
                if not nombres: return ""
                return "\n".join([f"{i}. {obtener_grado_abreviado(n[0])} {obtener_nombre_completo(n[0])}" for i, n in enumerate(nombres, 1)])
            
            minuta = f"NOVEDADES ESC \"H\" FECHA: {fecha_minuta}\nFE: {stats['total_general']}\nP: {stats['presentes_total']}\nA: {stats['ausentes_total']}\n\n"
            minuta += f"FORMADOS PRIMERA OBLIGACIÓN: {numero_a_texto(stats['presentes_0620'])}\n\n"
            minuta += f"INGRESO HORARIO DIFERENCIADO: {numero_a_texto(stats['total_diferenciado'])}\n"
            if stats['aulas_diferenciado']:
                for i, (aula, info) in enumerate(sorted(stats['aulas_diferenciado'].items()), 1):
                    grado = "ASP III" if info['curso'] == 'Tercer Año' else "ASP I"
                    minuta += f"{i}. AULA {aula} - {info['total']} {grado} - INGRESO {info['horario']}\n"
            minuta += f"\nAPRESTOS EN SUS DOMICILIOS: {numero_a_texto(stats['total_apresto'])}\n"
            if stats['aulas_apresto']:
                for aula, cant in sorted(stats['aulas_apresto'].items()):
                    minuta += f"  - AULA {aula}: {cant} ASPIRANTES\n"
            minuta += f"\nSSD: {numero_a_texto(cant_ssd)}.-\n"
            lista = obtener_lista_enumerada("SSD")
            if lista: minuta += f"{lista}\n"
            minuta += f"\nAUTORIZADOS: {numero_a_texto(cant_aut)}.-\n"
            lista = obtener_lista_enumerada("AUTORIZADO")
            if lista: minuta += f"{lista}\n"
            minuta += f"\nA CUENTA DE LAO26: {numero_a_texto(cant_lao_cuenta)}.-\n"
            lista = obtener_lista_enumerada("A CUENTA DE LAO")
            if lista: minuta += f"{lista}\n"
            minuta += f"\nLAO26: {numero_a_texto(cant_lao26)}.-\n"
            lista = obtener_lista_enumerada("LAO")
            if lista: minuta += f"{lista}\n"
            minuta += f"\nLES: {numero_a_texto(cant_les)}.-\n"
            lista = obtener_lista_enumerada("LES")
            if lista: minuta += f"{lista}\n"
            minuta += f"\nDESCANSO SERVICIO ARMAS NOCTURNO: {numero_a_texto(cant_descanso)}.-\n"
            lista = obtener_lista_enumerada("DESCANSO DE GUARDIA")
            if lista: minuta += f"{lista}\n"
            minuta += f"\nSERVICIO ARMAS DIURNO: {numero_a_texto(cant_guardia_diur)}\n"
            lista = obtener_lista_enumerada("GUARDIA DIURNA")
            if lista: minuta += f"{lista}\n"
            minuta += f"\nRACIONAMIENTO: {numero_a_texto(len(rac_hoy))}\n"
            if rac_hoy:
                for i, r in enumerate(rac_hoy, 1):
                    minuta += f"{i}. {obtener_grado_abreviado(r[0])} {obtener_nombre_completo(r[0])}\n"
            minuta = minuta.upper()
            
            st.text_area("📄 Minuta Generada:", minuta, height=600)
            st.download_button("📥 Descargar Minuta (TXT)", minuta, f"minuta_{datetime.now().strftime('%d%m%y')}.txt", "text/plain")

st.markdown('<div class="main-footer"><small>SISTEMA DE NOVEDADES ESCUADRÓN H "CABO MARCELO GODOY" - AÑO 2026<br>Disciplina, Honor y Servicio</small></div>', unsafe_allow_html=True)
