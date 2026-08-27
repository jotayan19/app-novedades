import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import io

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="SISTEMA DE NOVEDADES",
    page_icon="👮‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #121212; color: #e0e0e0; }
    h1, h2, h3, h4, h5, h6, label, p, span, div { color: #f0f0f0 !important; }
    section[data-testid="stSidebar"] { background-color: #1e1e1e; border-right: 1px solid #333; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 { color: #4CAF50 !important; }
    .stButton > button {
        background-color: #2E5936 !important; color: white !important;
        border: 1px solid #4CAF50 !important; border-radius: 8px !important;
        font-weight: bold !important;
    }
    .stButton > button:hover { background-color: #4CAF50 !important; }
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stTextArea > div > div > textarea {
        background-color: #2c2c2c !important; color: white !important;
        border: 1px solid #444 !important; border-radius: 8px !important;
    }
    .dataframe { background-color: #1e1e1e !important; color: #e0e0e0 !important; }
    .dataframe th { background-color: #2E5936 !important; color: white !important; }
    .login-card {
        max-width: 500px; margin: 80px auto; padding: 40px;
        background: linear-gradient(145deg, #1e1e1e, #252525);
        border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 1px solid #333; text-align: center;
    }
    .login-title { font-size: 2.5em; font-weight: bold; color: #4CAF50 !important; margin-bottom: 30px; text-transform: uppercase; }
    .main-title {
        text-align: center; font-size: 3.5em; font-weight: bold;
        color: #4CAF50 !important; margin-top: 20px; margin-bottom: 10px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CONSTANTES ====================
USUARIO_CORRECTO = "DRAGJOTAYANLEONEL"
CONTRASENA_CORRECTA = "Drag2026"

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
    for hor in horarios:
        if len(hor) >= 2:
            if hor[0].strip().upper() == aula_upper:
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
    
    ausentes_apresto = 0
    for e in empleados:
        if len(e) >= 5:
            aula = e[4].strip().upper()
            horario = obtener_horario_aula(aula)
            if horario == "apresto en domicilio":
                ausentes_apresto += 1
    
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
    
    presentes_0620 = 0
    for e in empleados:
        if len(e) >= 5:
            aula = e[4].strip().upper()
            horario = obtener_horario_aula(aula)
            if horario == "06:20":
                if not any(n[0].upper().strip() == e[1].upper().strip() for n in novedades_hoy):
                    presentes_0620 += 1
    
    aulas_diferenciado = {}
    total_diferenciado = 0
    
    for aula, info in aulas_dict.items():
        horario = info["horario"]
        if horario and horario != "06:20" and horario != "apresto en domicilio":
            presentes_aula = info["total"] - info["ausentes"]
            aulas_diferenciado[aula] = {
                "total": presentes_aula,
                "horario": horario,
                "curso": info["curso"]
            }
            total_diferenciado += presentes_aula
    
    aulas_apresto = {}
    total_apresto = 0
    for aula, info in aulas_dict.items():
        if info["horario"] == "apresto en domicilio":
            aulas_apresto[aula] = info["total"]
            total_apresto += info["total"]
    
    return {
        "total_general": total_general, "total_3": total_3, "total_cao": total_cao,
        "presentes_total": presentes_total, "presentes_3": presentes_3, "presentes_cao": presentes_cao,
        "ausentes_total": ausentes_total, "ausentes_3": ausentes_3, "ausentes_cao": ausentes_cao,
        "presentes_0620": presentes_0620,
        "aulas_dict": aulas_dict, "novedades_hoy": novedades_hoy,
        "total_diferenciado": total_diferenciado,
        "aulas_diferenciado": aulas_diferenciado,
        "total_apresto": total_apresto,
        "aulas_apresto": aulas_apresto
    }

# ==================== LOGIN ====================
def pantalla_login():
    col_center = st.columns([1, 2, 1]) 
    with col_center[1]:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">SISTEMA DE NOVEDADES</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">NOVEDADES ESCUADRON H "CABO MARCELO GODOY"</p>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            usuario = st.text_input("Usuario", placeholder="Ingrese su usuario", label_visibility="collapsed")
            contrasena = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña", label_visibility="collapsed")
            submitted = st.form_submit_button("INGRESAR AL SISTEMA", use_container_width=True)
            
            if submitted:
                if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:
                    st.session_state['logueado'] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== INICIALIZACIÓN ====================
if 'logueado' not in st.session_state: st.session_state['logueado'] = False
if not st.session_state['logueado']:
    pantalla_login()
    st.stop()

if 'empleados' not in st.session_state: st.session_state['empleados'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['empleados'])
if 'horarios' not in st.session_state: st.session_state['horarios'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['horarios'])
if 'novedades' not in st.session_state: st.session_state['novedades'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['novedades'])
if 'racionamiento' not in st.session_state: st.session_state['racionamiento'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['racionamiento'])
if 'plan_llamada' not in st.session_state: st.session_state['plan_llamada'] = cargar_csv_inicial(NOMBRES_ARCHIVOS['plan_llamada'])
if 'nov_counter' not in st.session_state: st.session_state['nov_counter'] = 0
if 'rac_counter' not in st.session_state: st.session_state['rac_counter'] = 0

# ==================== ENCABEZADO ====================
st.markdown('<h1 class="main-title">SISTEMA DE NOVEDADES</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #aaa; font-size: 1.2em; margin-top: -10px;">DRAGONEANTE PRINCIPAL JOTAYAN MEDINA LEONEL - AÑO 2026</p>', unsafe_allow_html=True)
st.markdown("---")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<h2 style="color: #4CAF50; text-align: center;">PANEL DE CONTROL</h2>', unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.metric("📅 Fecha", datetime.now().strftime('%d/%m/%Y'))
    with c2: st.metric("🕐 Hora", datetime.now().strftime('%H:%M:%S'))
    st.markdown("---")
    
    stats = calcular_estadisticas()
    if stats:
        st.metric("👥 Fuerza Efectiva", stats["total_general"])
        st.metric("✅ Presentes", stats["presentes_total"])
        st.metric("📋 Ausentes", stats["ausentes_total"])
    
    st.markdown("---")
    st.markdown("#### 💾 Guardar Datos")
    st.info("⚠️ Descargá los CSV para no perder los datos")
    
    if st.download_button("📥 Descargar empleados.csv", data=convertir_a_csv(st.session_state['empleados']), file_name="empleados.csv", mime="text/csv", use_container_width=True):
        st.success("✅ Descargado")
    if st.download_button("📥 Descargar novedades.csv", data=convertir_a_csv(st.session_state['novedades']), file_name="novedades.csv", mime="text/csv", use_container_width=True):
        st.success("✅ Descargado")
    if st.download_button("📥 Descargar racionamiento.csv", data=convertir_a_csv(st.session_state['racionamiento']), file_name="racionamiento.csv", mime="text/csv", use_container_width=True):
        st.success("✅ Descargado")
    
    st.markdown("---")
    if st.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
        st.session_state['logueado'] = False
        st.rerun()

# ==================== PESTAÑAS ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "👥 Personal", " Aulas/Horarios", "📞 Plan Llamada", "📋 Novedades", "🍽️ Racionamiento", " FE por Aula", "📝 Reportes"
])

# ==================== TAB 1: PERSONAL ====================
with tab1:
    st.header("Gestión de Personal")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📤 Importar Excel")
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
                        if grado and nombre and str(grado).upper() != 'GRADO':
                            empleados.append([grado, nombre, dni, ce, aula])
                    if empleados:
                        st.session_state['empleados'] = empleados
                        st.success(f"✅ Se importaron {len(empleados)} empleados")
                        
                        # DESCARGA AUTOMÁTICA DEL CSV
                        csv_data = convertir_a_csv(empleados)
                        st.download_button(
                            "️ Descargar CSV de respaldo",
                            data=csv_data,
                            file_name=f"empleados_{datetime.now().strftime('%d%m%Y')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        st.rerun()
                except Exception as e: st.error(f"Error: {str(e)}")
    with col2:
        st.subheader(" Personal Registrado")
        empleados = st.session_state.get('empleados', [])
        if empleados:
            df_empleados = pd.DataFrame(empleados, columns=['Grado', 'Apellido y Nombre', 'DNI', 'CE', 'Aula'])
            st.dataframe(df_empleados, use_container_width=True, height=400)
        else: st.info("No hay personal registrado.")

# ==================== TAB 2: HORARIOS ====================
with tab2:
    st.header("Configuración de Horarios")
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
                if horario: 
                    nuevos_horarios.append([aula.upper(), horario])
        
        if st.form_submit_button("💾 Guardar Horarios", type="primary", use_container_width=True):
            st.session_state['horarios'] = nuevos_horarios
            st.success("✅ Horarios guardados")
            st.rerun()
    
    if horarios_actuales:
        st.write("**Horarios guardados:**")
        for h in horarios_actuales:
            if len(h) >= 2:
                st.write(f"- {h[0]}: {h[1]}")

# ==================== TAB 3: PLAN LLAMADA ====================
with tab3:
    st.header("Plan de Llamada")
    empleados = st.session_state.get('empleados', [])
    if empleados:
        nombres = [f"{e[0]} - {e[1]}" for e in empleados]
        empleado_sel = st.selectbox("Seleccionar Aspirante:", [""] + nombres)
        if empleado_sel:
            nombre = empleado_sel.split(" - ", 1)[1]
            st.write(f"**Nombre:** {nombre}")

# ==================== TAB 4: NOVEDADES ====================
with tab4:
    st.header("Registro de Novedades")
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
            observaciones = st.text_area("📝 Observaciones:", height=100, key="nov_obs")
        
        if st.button("💾 Guardar Novedad", type="primary", use_container_width=True):
            if empleado_sel and categoria and motivo:
                nombre = empleado_sel.split(" - ", 1)[1]
                nueva_novedad = [nombre, categoria, normalizar_motivo(motivo), observaciones, hoy]
                st.session_state['novedades'].append(nueva_novedad)
                st.session_state['nov_counter'] += 1
                st.success("✅ Novedad guardada")
                st.rerun()

# ==================== TAB 5: RACIONAMIENTO ====================
with tab5:
    st.header("Registro de Racionamiento")
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
                    st.success("✅ Almuerzo registrado")
                    st.rerun()
        
        rac_hoy = [r for r in st.session_state.get('racionamiento', []) if len(r) >= 4 and r[3] == hoy]
        if rac_hoy:
            st.write(f"**Total Almuerzos:** {len(rac_hoy)}")
            for rac in rac_hoy:
                st.write(f"- {rac[0]}")

# ==================== TAB 6: FE POR AULA ====================
with tab6:
    st.header("📊 Fuerza Efectiva por Aula")
    stats = calcular_estadisticas()
    if stats and stats['aulas_dict']:
        datos = [{"Aula": a, "FE": i["total"], "Horario": i["horario"] or "Sin asignar", "P": i["total"]-i["ausentes"], "A": i["ausentes"]} for a, i in sorted(stats["aulas_dict"].items())]
        st.dataframe(pd.DataFrame(datos), use_container_width=True)

# ==================== TAB 7: REPORTES - MINUTA ====================
with tab7:
    st.header("Reportes y Minutas")
    
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
                lista = []
                for i, n in enumerate(nombres, 1):
                    grado_abr = obtener_grado_abreviado(n[0])
                    nombre_completo = obtener_nombre_completo(n[0])
                    lista.append(f"{i}. {grado_abr} {nombre_completo}")
                return "\n".join(lista)
            
            minuta = f"NOVEDADES ESC \"H\" FECHA: {fecha_minuta}\n"
            minuta += f"FE: {stats['total_general']}\n"
            minuta += f"P: {stats['presentes_total']}\n"
            minuta += f"A: {stats['ausentes_total']}\n"
            minuta += f"\n\n"
            minuta += f"FORMADOS PRIMERA OBLIGACIÓN: {numero_a_texto(stats['presentes_0620'])}\n"
            minuta += f"\n\n"
            
            # INGRESO HORARIO DIFERENCIADO
            minuta += f"INGRESO HORARIO DIFERENCIADO: {numero_a_texto(stats['total_diferenciado'])}\n"
            if stats['aulas_diferenciado']:
                for i, (aula, info) in enumerate(sorted(stats['aulas_diferenciado'].items()), 1):
                    grado_aula = "ASP III" if info['curso'] == 'Tercer Año' else "ASP I"
                    minuta += f"{i}. AULA {aula} - {info['total']} {grado_aula} - INGRESO {info['horario']}\n"
            minuta += f"\n\n"
            
            # APRESTOS
            minuta += f"APRESTOS EN SUS DOMICILIOS: {numero_a_texto(stats['total_apresto'])}\n"
            if stats['aulas_apresto']:
                for aula, cantidad in sorted(stats['aulas_apresto'].items()):
                    minuta += f"  - AULA {aula}: {cantidad} ASPIRANTES\n"
            minuta += f"\n\n"
            
            # SSD
            lista_ssd = obtener_lista_enumerada("SSD")
            if lista_ssd: minuta += f"SSD: {numero_a_texto(cant_ssd)}.-\n{lista_ssd}\n"
            else: minuta += f"SSD: {numero_a_texto(cant_ssd)}.-\n"
            minuta += f"\n\n"
            
            # AUTORIZADOS
            lista_aut = obtener_lista_enumerada("AUTORIZADO")
            if lista_aut: minuta += f"AUTORIZADOS: {numero_a_texto(cant_aut)}.-\n{lista_aut}\n"
            else: minuta += f"AUTORIZADOS: {numero_a_texto(cant_aut)}.-\n"
            minuta += f"\n\n"
            
            # A CUENTA DE LAO26
            lista_lao_cuenta = obtener_lista_enumerada("A CUENTA DE LAO")
            if lista_lao_cuenta: minuta += f"A CUENTA DE LAO26: {numero_a_texto(cant_lao_cuenta)}.-\n{lista_lao_cuenta}\n"
            else: minuta += f"A CUENTA DE LAO26: {numero_a_texto(cant_lao_cuenta)}.-\n"
            minuta += f"\n\n"
            
            # LAO26
            lista_lao26 = obtener_lista_enumerada("LAO")
            if lista_lao26: minuta += f"LAO26: {numero_a_texto(cant_lao26)}.-\n{lista_lao26}\n"
            else: minuta += f"LAO26: {numero_a_texto(cant_lao26)}.-\n"
            minuta += f"\n\n"
            
            # LES
            lista_les = obtener_lista_enumerada("LES")
            if lista_les: minuta += f"LES: {numero_a_texto(cant_les)}.-\n{lista_les}\n"
            else: minuta += f"LES: {numero_a_texto(cant_les)}.-\n"
            minuta += f"\n\n"
            
            # DESCANSO DEL SERVICIO DE ARMAS NOCTURNO
            lista_descanso = obtener_lista_enumerada("DESCANSO DE GUARDIA")
            if lista_descanso: minuta += f"DESCANSO DEL SERVICIO DE ARMAS NOCTURNO: {numero_a_texto(cant_descanso)}.-\n{lista_descanso}\n"
            else: minuta += f"DESCANSO DEL SERVICIO DE ARMAS NOCTURNO: {numero_a_texto(cant_descanso)}.-\n"
            minuta += f"\n\n"
            
            # SERVICIO DE ARMAS DIURNO
            lista_diur = obtener_lista_enumerada("GUARDIA DIURNA")
            if lista_diur: minuta += f"SERVICIO DE ARMAS DIURNO: {numero_a_texto(cant_guardia_diur)}\n{lista_diur}\n"
            else: minuta += f"SERVICIO DE ARMAS DIURNO: {numero_a_texto(cant_guardia_diur)}\n"
            minuta += f"\n\n"
            
            # RACIONAMIENTO CON LISTA
            minuta += f"RACIONAMIENTO: {numero_a_texto(len(rac_hoy))}\n"
            if rac_hoy:
                minuta += f"\n"
                for i, r in enumerate(rac_hoy, 1):
                    grado_abr = obtener_grado_abreviado(r[0])
                    nombre_completo = obtener_nombre_completo(r[0])
                    minuta += f"{i}. {grado_abr} {nombre_completo}\n"
            
            minuta = minuta.upper()
            
            st.text_area(" Minuta Generada:", minuta, height=600)
            st.download_button("📥 Descargar Minuta (TXT)", minuta, f"minuta_{datetime.now().strftime('%d%m%y')}.txt", "text/plain")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'><small>SISTEMA DE NOVEDADES ESCUADRON H - AÑO 2026</small></div>", unsafe_allow_html=True)
