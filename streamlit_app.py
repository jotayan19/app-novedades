import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import io

# ==================== CONFIGURACIÓN DE PÁGINA Y ESTILOS ====================
st.set_page_config(
    page_title="NOVEDADES ESCUADRÓN H",
    page_icon="👮‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL del Logo de Gendarmería (Escudo Oficial)
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Escudo_de_la_Gendarmer%C3%ADa_Nacional_Argentina.svg/1200px-Escudo_de_la_Gendarmer%C3%ADa_Nacional_Argentina.svg.png"

# Inyección de CSS para diseño moderno Verde/Gris Oscuro
st.markdown("""
<style>
    /* Fondo general y textos */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Títulos y encabezados */
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #f0f0f0 !important;
    }
    
    /* Sidebar (Menú lateral) */
    section[data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
        color: #4CAF50 !important;
    }
    
    /* Botones Primarios (Verde Gendarmería) */
    .stButton > button {
        background-color: #2E5936 !important;
        color: white !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #4CAF50 !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.4);
    }
    
    /* Inputs y Selectboxes (Campos de texto) */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        background-color: #2c2c2c !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus, 
    .stSelectbox > div > div > div:focus {
        border-color: #4CAF50 !important;
        box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
    }
    
    /* Dataframes (Tablas) */
    .dataframe {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
    }
    .dataframe th {
        background-color: #2E5936 !important;
        color: white !important;
    }
    
    /* Alertas e Info boxes */
    .stAlert {
        background-color: #2c2c2c !important;
        border-left: 4px solid #4CAF50 !important;
        color: #e0e0e0 !important;
    }
    
    /* Login Container Personalizado */
    .login-card {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(145deg, #1e1e1e, #252525);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 1px solid #333;
        text-align: center;
    }
    .login-logo {
        width: 120px;
        height: auto;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.1));
    }
    .login-title {
        font-size: 1.8em;
        font-weight: bold;
        color: #4CAF50 !important;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .login-subtitle {
        font-size: 0.9em;
        color: #aaa !important;
        margin-bottom: 30px;
        font-style: italic;
    }
    
    /* Tabs (Pestañas) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #2c2c2c;
        border-radius: 8px 8px 0 0;
        color: #aaa;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2E5936 !important;
        color: white !important;
        border-bottom: 2px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONSTANTES Y DATOS ====================
USUARIO_CORRECTO = "DRAGJOTAYANLEONEL"
CONTRASENA_CORRECTA = "Drag2026"

NOMBRES_ARCHIVOS = {
    'empleados': 'empleados.csv',
    'horarios': 'horarios.csv',
    'novedades': 'novedades.csv',
    'racionamiento': 'racionamiento.csv',
    'plan_llamada': 'plan_llamada.csv'
}

AULAS_TERCER_ANO = ["23 TT", "18 TM", "23 TM", "24 TM", "26 TM", "28 TM"]
AULAS_CAO = ["7 TT", "8 TT"]
AULAS = AULAS_TERCER_ANO + AULAS_CAO

MOTIVOS = {
    "Ausente fuera de la escuela": ["SSD", "ART", "Descanso de guardia", "A cuenta de LAO", "Autorizado"],
    "Presente pero fuera del escuadron": ["Guardia diurna", "Guardia nocturna", "Formacion", "Practica de desfile"]
}

# ==================== FUNCIONES AUXILIARES ====================
def cargar_csv_inicial(nombre_referencia):
    try:
        with open(nombre_referencia, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return [row for row in reader if row]
    except FileNotFoundError:
        return []
    except Exception:
        return []

def convertir_a_csv(datos):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(datos)
    return output.getvalue()

def normalizar_motivo(motivo):
    if not motivo:
        return motivo
    motivo = str(motivo).strip().upper()
    if motivo == "ARTE":
        return "ART"
    if motivo.startswith("ART") and len(motivo) <= 5:
        return "ART"
    return motivo

def determinar_curso(grado):
    grado_upper = str(grado).upper()
    if "DRAG" in grado_upper or "DRAGONEANTE" in grado_upper or "III" in grado_upper:
        return "Tercer Año"
    return "Auxiliar Operativo"

def obtener_grado_por_nombre(nombre):
    empleados = st.session_state.get('empleados', [])
    for emp in empleados:
        if len(emp) >= 2 and emp[1].upper().strip() == nombre.upper().strip():
            return emp[0]
    return ""

def determinar_curso_por_nombre(nombre):
    grado = obtener_grado_por_nombre(nombre)
    if grado:
        return determinar_curso(grado)
    return "Tercer Año" if "DRAG" in nombre.upper() else "Auxiliar Operativo"

def obtener_horario_aula(aula):
    horarios = st.session_state.get('horarios', [])
    for hor in horarios:
        if len(hor) >= 2 and hor[0].strip().upper() == aula.strip().upper():
            return hor[1]
    return "06:20"

def numero_a_texto(numero):
    numeros = {
        1: "UNO (01)", 2: "DOS (02)", 3: "TRES (03)", 4: "CUATRO (04)",
        5: "CINCO (05)", 6: "SEIS (06)", 7: "SIETE (07)", 8: "OCHO (08)",
        9: "NUEVE (09)", 10: "DIEZ (10)", 11: "ONCE (11)", 12: "DOCE (12)",
        13: "TRECE (13)", 14: "CATORCE (14)", 15: "QUINCE (15)", 16: "DIECISEIS (16)",
        17: "DIECISIETE (17)", 18: "DIECIOCHO (18)", 19: "DIECINUEVE (19)", 20: "VEINTE (20)",
        21: "VEINTIUNO (21)", 22: "VEINTIDOS (22)", 23: "VEINTITRES (23)", 24: "VEINTICUATRO (24)",
        25: "VEINTICINCO (25)"
    }
    return numeros.get(numero, str(numero).zfill(2))

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
    
    if not empleados:
        return None
    
    total_3 = sum(1 for e in empleados if determinar_curso(e[0]) == "Tercer Año")
    total_cao = sum(1 for e in empleados if determinar_curso(e[0]) == "Auxiliar Operativo")
    total_general = len(empleados)
    
    ausentes_3 = sum(1 for n in novedades_hoy if determinar_curso_por_nombre(n[0]) == "Tercer Año")
    ausentes_cao = sum(1 for n in novedades_hoy if determinar_curso_por_nombre(n[0]) == "Auxiliar Operativo")
    ausentes_total = len(novedades_hoy)
    
    presentes_3 = total_3 - ausentes_3
    presentes_cao = total_cao - ausentes_cao
    presentes_total = total_general - ausentes_total
    
    formados_0620_3 = 0
    formados_0620_cao = 0
    ausentes_0620_3 = 0
    ausentes_0620_cao = 0
    
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
            if tiene_novedad:
                aulas_dict[aula]["ausentes"] += 1
                
            if horario == "06:20":
                if curso == "Tercer Año":
                    formados_0620_3 += 1
                    if tiene_novedad: ausentes_0620_3 += 1
                else:
                    formados_0620_cao += 1
                    if tiene_novedad: ausentes_0620_cao += 1
    
    total_0620 = sum(info["total"] for info in aulas_dict.values() if info["horario"] == "06:20")
    ausentes_0620 = sum(info["ausentes"] for info in aulas_dict.values() if info["horario"] == "06:20")
    presentes_0620 = total_0620 - ausentes_0620
    
    return {
        "total_general": total_general, "total_3": total_3, "total_cao": total_cao,
        "presentes_total": presentes_total, "presentes_3": presentes_3, "presentes_cao": presentes_cao,
        "ausentes_total": ausentes_total, "ausentes_3": ausentes_3, "ausentes_cao": ausentes_cao,
        "presentes_0620": presentes_0620,
        "formados_0620_3": formados_0620_3 - ausentes_0620_3,
        "formados_0620_cao": formados_0620_cao - ausentes_0620_cao,
        "aulas_dict": aulas_dict, "novedades_hoy": novedades_hoy
    }

# ==================== PANTALLA DE LOGIN MODERNA ====================
def pantalla_login():
    # Usamos columnas para centrar perfectamente la tarjeta
    col_center = st.columns([1, 2, 1]) 
    
    with col_center[1]:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Logo de Gendarmería
        st.image(LOGO_URL, width=100)
        
        st.markdown('<h1 class="login-title">Acceso Restringido</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">NOVEDADES ESCUADRÓN H "CABO MARCELO GODOY"</p>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            usuario = st.text_input("Usuario", placeholder="Ingrese su usuario", label_visibility="collapsed")
            contrasena = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña", label_visibility="collapsed")
            
            # Botón de ancho completo
            submitted = st.form_submit_button("INGRESAR AL SISTEMA", use_container_width=True)
            
            if submitted:
                if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:
                    st.session_state['logueado'] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas. Intente nuevamente.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer pequeño
        st.markdown('<div style="text-align: center; color: #666; margin-top: 20px; font-size: 0.8em;">Sistema de Gendarmería Nacional Argentina © 2026</div>', unsafe_allow_html=True)

# ==================== INICIALIZACIÓN DE SESIÓN ====================
if 'logueado' not in st.session_state:
    st.session_state['logueado'] = False

if not st.session_state['logueado']:
    pantalla_login()
    st.stop()

# Cargar datos iniciales si no existen en sesión
if 'empleados' not in st.session_state:
    st.session_state['empleados'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['empleados'])
if 'horarios' not in st.session_state:
    st.session_state['horarios'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['horarios'])
if 'novedades' not in st.session_state:
    st.session_state['novedades'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['novedades'])
if 'racionamiento' not in st.session_state:
    st.session_state['racionamiento'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['racionamiento'])
if 'plan_llamada' not in st.session_state:
    st.session_state['plan_llamada'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['plan_llamada'])

# ==================== ENCABEZADO PRINCIPAL ====================
st.markdown("---")
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image(LOGO_URL, width=80)
with col_titulo:
    st.markdown('<h1 style="color: #4CAF50; font-size: 2.5em; margin-top: 10px;">NOVEDADES ESCUADRÓN H "CABO MARCELO GODOY"</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #aaa; font-size: 1.2em; margin-top: -10px;">DRAGONEANTE JOTAYAN MEDINA LEONEL - AÑO 2026</p>', unsafe_allow_html=True)
st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<h2 style="color: #4CAF50; text-align: center;">PANEL DE CONTROL</h2>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Fecha y Hora destacadas
    c1, c2 = st.columns(2)
    with c1: st.metric("📅 Fecha", datetime.now().strftime('%d/%m/%Y'))
    with c2: st.metric("🕐 Hora", datetime.now().strftime('%H:%M:%S'))
    
    st.markdown("---")
    
    stats = calcular_estadisticas()
    if stats:
        st.markdown("#### 📊 Estadísticas del Día")
        st.metric(" Fuerza Efectiva", stats["total_general"])
        st.metric("✅ Presentes", stats["presentes_total"])
        st.metric("️ Ausentes", stats["ausentes_total"])
        st.divider()
        st.metric("🎓 Tercer Año", f"{stats['presentes_3']}/{stats['total_3']}")
        st.metric("🛡️ Aux. Operativo", f"{stats['presentes_cao']}/{stats['total_cao']}")
    
    st.markdown("---")
    st.markdown("#### 💾 Gestión de Datos")
    st.caption("⚠️ En la nube los datos son temporales. Descarga tus avances.")
    
    if st.download_button(" Descargar empleados.csv", data=convertir_a_csv(st.session_state['empleados']), file_name="empleados.csv", mime="text/csv", use_container_width=True):
        pass
    if st.download_button(" Descargar novedades.csv", data=convertir_a_csv(st.session_state['novedades']), file_name="novedades.csv", mime="text/csv", use_container_width=True):
        pass
        
    st.divider()
    if st.button("🔄 Reiniciar Datos", type="secondary", use_container_width=True):
        st.session_state['empleados'] = []
        st.session_state['novedades'] = []
        st.session_state['racionamiento'] = []
        st.success("Datos reiniciados.")
        st.rerun()
        
    st.divider()
    if st.button(" Cerrar Sesión", type="primary", use_container_width=True):
        st.session_state['logueado'] = False
        st.rerun()

# ==================== PESTAÑAS ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👥 Personal", "🏫 Aulas/Horarios", "📞 Plan Llamada", "📋 Novedades", "🍽️ Racionamiento", "📊 Reportes"
])

# ==================== TAB 1: PERSONAL ====================
with tab1:
    st.header("Gestión de Personal")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader(" Importar Excel")
        st.info("Usa el archivo `listaescuadronh.xlsx`")
        archivo_excel = st.file_uploader("Selecciona tu archivo Excel", type=['xlsx', 'xls'], key="excel_personal")
        
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
                        
                        if grado and nombre and str(grado).lower() != 'nan' and str(nombre).lower() != 'nan' and str(grado).upper() != 'GRADO':
                            empleados.append([grado, nombre, dni, ce, aula])
                    
                    if empleados:
                        st.session_state['empleados'] = empleados
                        st.success(f"✅ Se importaron {len(empleados)} empleados correctamente")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error al leer el Excel: {str(e)}")
    
    with col2:
        st.subheader("📋 Personal Registrado")
        empleados = st.session_state.get('empleados', [])
        if empleados:
            df_empleados = pd.DataFrame(empleados, columns=['Grado', 'Apellido y Nombre', 'DNI', 'CE', 'Aula'])
            st.dataframe(df_empleados, use_container_width=True, height=400)
            st.write(f"**Total:** {len(empleados)} | **3° Año:** {sum(1 for e in empleados if determinar_curso(e[0])=='Tercer Año')} | **CAO:** {sum(1 for e in empleados if determinar_curso(e[0])=='Auxiliar Operativo')}")
        else:
            st.info("No hay personal registrado. Importa un Excel para comenzar.")

# ==================== TAB 2: AULAS Y HORARIOS ====================
with tab2:
    st.header("Configuración de Horarios de Aulas")
    st.info("🎓 Tercer Año: 23TT, 18TM, 23TM, 24TM, 26TM, 28TM | 🛡️ CAO: 7TT, 8TT")
    
    horarios_actuales = st.session_state.get('horarios', [])
    horarios_dict = {h[0]: h[1] for h in horarios_actuales if len(h) >= 2}
    
    with st.form("form_horarios"):
        nuevos_horarios = []
        cols = st.columns(2)
        for i, aula in enumerate(AULAS):
            with cols[i % 2]:
                horario_actual = horarios_dict.get(aula, "06:20")
                horario = st.selectbox(f"Aula {aula}", ["06:20", "07:30", "08:10", "09:20"],
                                       index=["06:20", "07:30", "08:10", "09:20"].index(horario_actual) if horario_actual in ["06:20", "07:30", "08:10", "09:20"] else 0,
                                       key=f"horario_{aula}")
                nuevos_horarios.append([aula, horario])
        
        if st.form_submit_button("💾 Guardar Horarios", type="primary", use_container_width=True):
            st.session_state['horarios'] = nuevos_horarios
            st.success("✅ Horarios guardados en memoria")
            st.rerun()

    st.divider()
    st.subheader("Reporte de Aulas")
    stats = calcular_estadisticas()
    if stats:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ✅ Primera Obligación (06:20)")
            st.metric("Total", sum(info["total"] for info in stats["aulas_dict"].values() if info["horario"]=="06:20"))
            st.metric("Presentes", sum(info["total"]-info["ausentes"] for info in stats["aulas_dict"].values() if info["horario"]=="06:20"))
        with col2:
            st.markdown("#### ⏰ Horario Diferenciado")
            st.metric("Total", sum(info["total"] for info in stats["aulas_dict"].values() if info["horario"]!="06:20"))
            st.metric("Presentes", sum(info["total"]-info["ausentes"] for info in stats["aulas_dict"].values() if info["horario"]!="06:20"))
        
        datos_aulas = [{"Aula": a, "Curso": i["curso"], "Horario": i["horario"], "FE": i["total"], "P": i["total"]-i["ausentes"], "A": i["ausentes"]} for a, i in sorted(stats["aulas_dict"].items())]
        st.dataframe(pd.DataFrame(datos_aulas), use_container_width=True)

# ==================== TAB 3: PLAN DE LLAMADA ====================
with tab3:
    st.header("Plan de Llamada")
    st.info("Información detallada de cada aspirante")
    
    empleados = st.session_state.get('empleados', [])
    
    if empleados:
        st.subheader("Buscar Aspirante")
        nombres = [f"{e[0]} - {e[1]}" for e in empleados]
        empleado_sel = st.selectbox("Seleccionar Aspirante:", [""] + nombres)
        
        if empleado_sel:
            nombre = empleado_sel.split(" - ", 1)[1]
            grado = empleado_sel.split(" - ", 1)[0]
            
            plan_datos = st.session_state.get('plan_llamada', [])
            info_detallada = None
            for row in plan_datos:
                if len(row) >= 2 and row[1].upper().strip() == nombre.upper().strip():
                    info_detallada = row
                    break
            
            st.divider()
            st.subheader(f"Información de: {nombre}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Grado:** {grado}")
                st.markdown(f"**DNI:** {next((e[2] for e in empleados if e[1].upper().strip() == nombre.upper().strip()), 'N/A')}")
                st.markdown(f"**CE:** {next((e[3] for e in empleados if e[1].upper().strip() == nombre.upper().strip()), 'N/A')}")
                st.markdown(f"**Aula:** {next((e[4] for e in empleados if e[1].upper().strip() == nombre.upper().strip()), 'N/A')}")
            
            with col2:
                if info_detallada and len(info_detallada) >= 6:
                    st.markdown(f"**Domicilio:** {info_detallada[2] if len(info_detallada) > 2 else 'N/A'}")
                    st.markdown(f"**Teléfono:** {info_detallada[3] if len(info_detallada) > 3 else 'N/A'}")
                    st.markdown(f"**Contacto Emergencia:** {info_detallada[4] if len(info_detallada) > 4 else 'N/A'}")
                    st.markdown(f"**Tel. Emergencia:** {info_detallada[5] if len(info_detallada) > 5 else 'N/A'}")
                else:
                    st.warning("⚠️ No hay información detallada cargada para este aspirante.")
            
            st.divider()
            if info_detallada:
                info_texto = f"FICHA PERSONAL\n\nGrado: {grado}\nNombre: {nombre}\n"
                info_texto += f"DNI: {next((e[2] for e in empleados if e[1].upper().strip() == nombre.upper().strip()), 'N/A')}\n"
                info_texto += f"CE: {next((e[3] for e in empleados if e[1].upper().strip() == nombre.upper().strip()), 'N/A')}\n"
                info_texto += f"Aula: {next((e[4] for e in empleados if e[1].upper().strip() == nombre.upper().strip()), 'N/A')}\n"
                if len(info_detallada) >= 6:
                    info_texto += f"\nDomicilio: {info_detallada[2]}\nTeléfono: {info_detallada[3]}\n"
                    info_texto += f"Contacto Emergencia: {info_detallada[4]}\nTel. Emergencia: {info_detallada[5]}\n"
                
                st.download_button("📥 Descargar Ficha Personal (TXT)", info_texto, f"ficha_{nombre.replace(' ', '_')}.txt", "text/plain")
    else:
        st.warning("⚠️ Primero debes importar el personal en la pestaña 'Personal'")

# ==================== TAB 4: NOVEDADES ====================
with tab4:
    st.header("Registro de Novedades")
    empleados = st.session_state.get('empleados', [])
    hoy = datetime.now().strftime("%d/%m/%Y")
    
    stats = calcular_estadisticas()
    if stats:
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Ausentes Total", stats["ausentes_total"])
        with col2: st.metric("Ausentes Tercer Año", stats["ausentes_3"])
        with col3: st.metric("Ausentes Aux. Operativo", stats["ausentes_cao"])
    
    if empleados:
        nombres = [f"{e[0]} - {e[1]}" for e in empleados]
        
        st.subheader("Registrar Nueva Novedad")
        col1, col2 = st.columns(2)
        with col1:
            empleado_sel = st.selectbox("Buscar Empleado:", [""] + nombres, key="nov_emp")
            categoria = st.selectbox("Categoría:", [""] + list(MOTIVOS.keys()), key="nov_cat")
        with col2:
            motivos_disponibles = MOTIVOS.get(categoria, [])
            motivo = st.selectbox("Motivo:", [""] + motivos_disponibles, key="nov_mot")
            observaciones = st.text_area("Observaciones / Diagnóstico:", height=100, key="nov_obs")
        
        if st.button("Guardar Novedad", type="primary", use_container_width=True):
            if empleado_sel and categoria and motivo:
                nombre = empleado_sel.split(" - ", 1)[1]
                motivo_norm = normalizar_motivo(motivo)
                nueva_novedad = [nombre, categoria, motivo_norm, observaciones, hoy]
                
                novedades_actuales = st.session_state.get('novedades', [])
                novedades_actuales.append(nueva_novedad)
                st.session_state['novedades'] = novedades_actuales
                
                st.success(f"Noviedad guardada: {nombre} - {motivo_norm}")
                st.rerun()
            else:
                st.warning("Completa todos los campos")
        
        st.divider()
        st.subheader(f"Novedades del Día ({hoy})")
        novedades = st.session_state.get('novedades', [])
        novedades_hoy = [n for n in novedades if len(n) >= 5 and n[4] == hoy]
        
        if novedades_hoy:
            for idx, nov in enumerate(novedades_hoy):
                motivo_mostrar = normalizar_motivo(nov[2])
                curso = determinar_curso_por_nombre(nov[0])
                icono_curso = "🎓" if curso == "Tercer Año" else "️"
                
                col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 2, 1, 1])
                with col1: st.write(f"**{nov[0]}**")
                with col2: st.write(f"{icono_curso} {curso[:3]}")
                with col3: st.write(motivo_mostrar)
                with col4: st.write(nov[3] if nov[3] else "-")
                with col5: st.write(nov[4])
                with col6:
                    if st.button("️", key=f"del_nov_{idx}"):
                        novedades_actuales = [row for row in st.session_state.get('novedades', []) if row != nov]
                        st.session_state['novedades'] = novedades_actuales
                        st.success(f"Novedad eliminada")
                        st.rerun()
        else:
            st.info("No hay novedades registradas para hoy.")
    else:
        st.warning("Primero importa el personal")

# ==================== TAB 5: RACIONAMIENTO ====================
with tab5:
    st.header("Registro de Racionamiento")
    empleados = st.session_state.get('empleados', [])
    hoy = datetime.now().strftime("%d/%m/%Y")
    
    if empleados:
        nombres = [f"{e[0]} - {e[1]}" for e in empleados]
        st.subheader("Registrar Racionamiento")
        col1, col2 = st.columns(2)
        with col1:
            empleado_sel = st.selectbox("Buscar Empleado:", [""] + nombres, key="rac_emp")
            comida = st.selectbox("Tipo de Comida:", ["", "Desayuno", "Almuerzo", "Merienda", "Cena"], key="rac_com")
        with col2:
            observaciones = st.text_input("Observaciones:", key="rac_obs")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Guardar Racionamiento", type="primary", use_container_width=True):
                if empleado_sel and comida:
                    nombre = empleado_sel.split(" - ", 1)[1]
                    nuevo_rac = [nombre, comida, observaciones, hoy]
                    
                    rac_actuales = st.session_state.get('racionamiento', [])
                    rac_actuales.append(nuevo_rac)
                    st.session_state['racionamiento'] = rac_actuales
                    
                    st.success("Racionamiento guardado")
                    st.rerun()
                else:
                    st.warning("Completa todos los campos")
        
        st.divider()
        st.subheader(f"Racionamiento del Día ({hoy})")
        racionamiento = st.session_state.get('racionamiento', [])
        rac_hoy = [r for r in racionamiento if len(r) >= 4 and r[3] == hoy]
        
        if rac_hoy:
            conteo = {"Desayuno": 0, "Almuerzo": 0, "Merienda": 0, "Cena": 0}
            for r in rac_hoy:
                if r[1] in conteo:
                    conteo[r[1]] += 1
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Desayunos", conteo["Desayuno"])
            with col2: st.metric("Almuerzos", conteo["Almuerzo"])
            with col3: st.metric("Meriendas", conteo["Merienda"])
            with col4: st.metric("Cenas", conteo["Cena"])
            
            st.divider()
            for idx, rac in enumerate(rac_hoy):
                col1, col2, col3, col4, col5 = st.columns([3, 2, 3, 1, 1])
                with col1: st.write(f"**{rac[0]}**")
                with col2: st.write(f"{rac[1]}")
                with col3: st.write(rac[2] if rac[2] else "-")
                with col4: st.write(rac[3])
                with col5:
                    if st.button("🗑️", key=f"del_rac_{idx}"):
                        rac_actuales = [row for row in st.session_state.get('racionamiento', []) if row != rac]
                        st.session_state['racionamiento'] = rac_actuales
                        st.success(f"Racionamiento eliminado")
                        st.rerun()
            
            st.divider()
            if st.button("Generar Minuta de Racionamiento", type="primary", use_container_width=True):
                minuta_rac = f"RACIONAMIENTO DEL DÍA {hoy}\n\n"
                minuta_rac += f"Desayunos: {conteo['Desayuno']}\n"
                minuta_rac += f"Almuerzos: {conteo['Almuerzo']}\n"
                minuta_rac += f"Meriendas: {conteo['Merienda']}\n"
                minuta_rac += f"Cenas: {conteo['Cena']}\n"
                minuta_rac += f"Total raciones: {len(rac_hoy)}\n\n"
                
                for tipo in ["Desayuno", "Almuerzo", "Merienda", "Cena"]:
                    items = [r for r in rac_hoy if r[1] == tipo]
                    if items:
                        minuta_rac += f"{tipo.upper()}:\n"
                        for r in items:
                            minuta_rac += f"  - {r[0]}\n"
                        minuta_rac += "\n"
                
                st.text_area("Minuta de Racionamiento:", minuta_rac, height=300)
                st.download_button("Descargar Minuta Racionamiento (TXT)", minuta_rac, f"racionamiento_{hoy.replace('/', '')}.txt", "text/plain")
        else:
            st.info("No hay racionamiento registrado.")
    else:
        st.warning("Primero importa el personal")

# ==================== TAB 6: REPORTES ====================
with tab6:
    st.header("Reportes y Minutas")
    tab_rep1, tab_rep2 = st.tabs(["Minuta Modelo 1", "Minuta Modelo 2"])
    
    with tab_rep1:
        st.subheader("Minuta Informativa por Cursos")
        if st.button("Generar Minuta Modelo 1", type="primary", use_container_width=True):
            stats = calcular_estadisticas()
            if not stats:
                st.error("No hay datos")
            else:
                fecha_minuta = datetime.now().strftime("%d%b%y").upper()
                tercer_ano = [n for n in stats["novedades_hoy"] if determinar_curso_por_nombre(n[0]) == "Tercer Año"]
                auxiliar_op = [n for n in stats["novedades_hoy"] if determinar_curso_por_nombre(n[0]) == "Auxiliar Operativo"]
                
                minuta = f"MINUTA INFORMATIVA DEL ESCUADRÓN H \"CABO MARCELO GODOY\" DEL DÍA {fecha_minuta}\n\n"
                minuta += f"FE: {stats['total_general']}\n"
                minuta += f"PRESENTES EN INSTITUTO: {stats['presentes_total']}\n"
                minuta += f"PRESENTES EN ESCUADRON: {stats['presentes_total']}\n"
                minuta += f"AUSENTES / FUERA DEL INSTITUTO: {stats['ausentes_total']}\n"
                minuta += f"FORMADOS A PRIMERA OBLIGACIÓN: {stats['presentes_0620']}\n\n"
                
                minuta += "CURSO DE TERCER AÑO\n\n"
                minuta += f"FE: {stats['total_3']}\n"
                minuta += f"PRESENTES EN INSTITUTO: {stats['presentes_3']}\n"
                minuta += f"PRESENTES EN ESCUADRON: {stats['presentes_3']}\n"
                minuta += f"AUSENTES / FUERA DEL INSTITUTO: {stats['ausentes_3']}\n"
                minuta += f"FORMADOS PRIMERA OBLIGACIÓN: {stats['formados_0620_3']}\n\n"
                minuta += "OBS:\n\n"
                
                for motivo_tipo in ["Guardia diurna", "Guardia nocturna", "ART", "SSD", "A cuenta de LAO", "Autorizado"]:
                    items = [n for n in tercer_ano if n[2] == motivo_tipo]
                    if items:
                        if motivo_tipo == "Guardia diurna":
                            minuta += f"SERVICIO DE ARMAS DIURNA: {numero_a_texto(len(items))} ASPIRANTES.\n"
                        elif motivo_tipo == "Guardia nocturna":
                            minuta += f"DESCANSO DE SERVICIO DE ARMAS NOCTURNO: {numero_a_texto(len(items))} ASPIRANTES.\n"
                        elif motivo_tipo == "ART":
                            minuta += "ART:\n"
                        elif motivo_tipo == "SSD":
                            minuta += "SIN SERVICIO EN DOMICILIO:\n"
                        elif motivo_tipo == "A cuenta de LAO":
                            minuta += "LAO: (A CUENTA DE LAO)\n"
                        elif motivo_tipo == "Autorizado":
                            minuta += "AUTORIZADO:\n"
                        
                        for i, item in enumerate(items, 1):
                            if motivo_tipo == "ART":
                                minuta += f"{i}. {item[0].upper()} (D: {item[4]}, H: {item[3] if item[3] else 'N/O'})\n"
                            else:
                                minuta += f"{i}. {item[0].upper()}\n"
                        minuta += "\n"
                
                minuta += "\nCURSO AUXILIAR OPERATIVO\n\n"
                minuta += f"FE: {stats['total_cao']}\n"
                minuta += f"PRESENTES EN INSTITUTO: {stats['presentes_cao']}\n"
                minuta += f"PRESENTES EN ESCUADRON: {stats['presentes_cao']}\n"
                minuta += f"AUSENTES / FUERA DEL INSTITUTO: {stats['ausentes_cao']}\n"
                minuta += f"FORMADOS PRIMERA OBLIGACIÓN: {stats['formados_0620_cao']}\n\n"
                minuta += "OBS:\n\n"
                
                for motivo_tipo in ["Guardia diurna", "Guardia nocturna", "ART", "SSD", "A cuenta de LAO", "Autorizado"]:
                    items = [n for n in auxiliar_op if n[2] == motivo_tipo]
                    if items:
                        if motivo_tipo == "Guardia diurna":
                            minuta += f"SERVICIO DE ARMAS DIURNO: {numero_a_texto(len(items))} ASPIRANTES.\n"
                        elif motivo_tipo == "Guardia nocturna":
                            minuta += f"DESCANSO DE SERVICIO DE ARMAS NOCTURNO: {numero_a_texto(len(items))} ASPIRANTES.\n"
                        elif motivo_tipo == "ART":
                            minuta += "ART:\n"
                        elif motivo_tipo == "SSD":
                            minuta += "SIN SERVICIO EN DOMICILIO:\n"
                        elif motivo_tipo == "A cuenta de LAO":
                            minuta += "LAO: (A CUENTA DE LAO)\n"
                        elif motivo_tipo == "Autorizado":
                            minuta += "AUTORIZADO:\n"
                        
                        for i, item in enumerate(items, 1):
                            if motivo_tipo == "ART":
                                minuta += f"{i}. {item[0].upper()} (D: {item[4]}, H: {item[3] if item[3] else 'N/O'})\n"
                            else:
                                minuta += f"{i}. {item[0].upper()}\n"
                        minuta += "\n"
                
                st.text_area("Minuta Generada (copia el texto):", minuta, height=500)
                st.download_button("Descargar Minuta (TXT)", minuta, f"minuta_modelo1_{datetime.now().strftime('%d%m%y')}.txt", "text/plain")
    
    with tab_rep2:
        st.subheader("Parte de Formación (General)")
        if st.button("Generar Minuta Modelo 2", type="primary", use_container_width=True):
            stats = calcular_estadisticas()
            if not stats:
                st.error("No hay datos")
            else:
                fecha_minuta = datetime.now().strftime("%d%b%y").upper()
                minuta = f"PARTE DE FORMACIÓN DEL ESCUADRÓN \"H\", DEL DIA {fecha_minuta}\n\n"
                minuta += f"FE: {stats['total_general']}\n"
                minuta += f"P: {stats['presentes_total']}\n"
                minuta += f"A: {stats['ausentes_total']}\n"
                minuta += f"FORMADOS: {stats['presentes_0620']}\n\n"
                minuta += "NOVEDADES:\n\n"
                
                motivos_unicos = list(set([n[2] for n in stats["novedades_hoy"]]))
                for motivo in motivos_unicos:
                    items = [n for n in stats["novedades_hoy"] if n[2] == motivo]
                    if motivo == "Guardia diurna":
                        minuta += f"- SERVICIO DE ARMAS DIURNO: {numero_a_texto(len(items))} ASP DE III Y CAO.\n\n"
                    elif motivo == "Guardia nocturna":
                        minuta += f"- DESCANSO DE SERVICIO DE ARMA NOCTURNO: {numero_a_texto(len(items))} ASP.\n\n"
                    elif motivo == "ART":
                        minuta += f"ART: {numero_a_texto(len(items))} ASP.\n\n"
                    else:
                        minuta += f"- {motivo.upper()}: {numero_a_texto(len(items))} ASP.\n\n"
                    
                    for i, item in enumerate(items, 1):
                        if motivo == "ART":
                            minuta += f"{i}. {item[0].upper()} DESDE {item[4]}.\n"
                        else:
                            minuta += f"{i}. {item[0].upper()}.\n"
                    minuta += "\n"
                
                st.text_area("Minuta Generada (copia el texto):", minuta, height=500)
                st.download_button("Descargar Minuta (TXT)", minuta, f"minuta_modelo2_{datetime.now().strftime('%d%m%y')}.txt", "text/plain")

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: #666;'><small>NOVEDADES ESCUADRÓN H \"CABO MARCELO GODOY\" - AÑO 2026</small></div>", unsafe_allow_html=True)
