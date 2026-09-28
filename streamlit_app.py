import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Portafolio Carlos Ordóñez", page_icon="⚙️")

st.markdown(
	"""
	<style>
	.stApp {
		background: #0d1117;
		color: #e6edf3;
		font-family: 'Segoe UI', sans-serif;
	}
	[data-testid="stSidebar"] { background: #161b22; }
	.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {
		font-family: 'Segoe UI', sans-serif;
	}
	.stButton button, .stLinkButton a {
		background: #238636;
		border: 1px solid #2ea043;
		color: #ffffff;
		font-weight: 600;
	}
	.stButton button:hover, .stLinkButton a:hover {
		background: #2ea043;
		border-color: #3fb950;
		color: #ffffff;
	}
	.tank-panel {
		background: #161b22;
		border: 1px solid #30363d;
		border-radius: 8px;
		padding: 1rem 1.2rem;
		margin-bottom: 0.75rem;
	}
	.tank-panel h3 { margin: 0 0 .25rem; color: #e6edf3; }
	.tank-subtitle { color: #8b949e; font-size: .9rem; }
	.status-line {
		border-left: 3px solid #58a6ff;
		padding: .55rem .8rem;
		background: #161b22;
		color: #e6edf3;
	}
	</style>
	""",
	unsafe_allow_html=True,
)

st.sidebar.title("Portafolio")
pagina = st.sidebar.radio(
	"Navegación",
	[
		"🏠 Inicio",
		"💡 Práctica 1: LED",
		"⚙️ Práctica 2: Relé",
		"🌊 Práctica 3: Bombas",
	],
	label_visibility="collapsed",
)

if pagina == "🏠 Inicio":
	st.title("Portafolio Interactivo de Sistemas Embebidos")
	st.write(
		"Dashboard desarrollado para visualizar y simular proyectos de electrónica "
		"y control en tiempo real, sin necesidad de hardware físico."
	)
	with st.container(border=True):
		st.subheader("GitHub")
		st.write("Código fuente y proyectos de Carlos Ordóñez.")
		st.link_button(
			"Visitar mi GitHub",
			"https://github.com/CarlosOrdonez-upb",
			type="primary",
		)
elif pagina == "💡 Práctica 1: LED":
	st.header("💡 Práctica 1: LED")
	st.caption("Simulación del control de un LED realizada en Wokwi.")
	components.html(
		'<iframe src="https://wokwi.com/projects/476381725083303937?embed=1" '
		'title="Simulación de control de LED en Wokwi" width="100%" height="600" '
		'style="border: 1px solid #30363d; border-radius: 6px;" allowfullscreen></iframe>',
		height=600,
		scrolling=False,
	)
elif pagina == "⚙️ Práctica 2: Relé":
	st.header("⚙️ Práctica 2: Relé")
	st.caption("Simulación del control de un relé realizada en Wokwi.")
	components.html(
		'<iframe src="https://wokwi.com/projects/476381886558822401?embed=1" '
		'title="Simulación de control de relé en Wokwi" width="100%" height="600" '
		'style="border: 1px solid #30363d; border-radius: 6px;" allowfullscreen></iframe>',
		height=600,
		scrolling=False,
	)
elif pagina == "🌊 Práctica 3: Bombas":
	CAPACIDAD_ML = 1000
	NIVEL_MINIMO_ML = 200
	NIVEL_MAXIMO_ML = 800
	PASO_ML = 10

	valores_iniciales = {
		"nivel_a_ml": 500,
		"nivel_b_ml": 500,
		"direccion": 0,
		"simulacion_activa": False,
		"interruptor_a": 0,
		"interruptor_b": 0,
		"normalizacion_activa": False,
		"objetivo_normalizacion_ml": None,
		"accion_pendiente": None,
		"accion_confirmacion": None,
		"estado_simulador": "Sistema detenido",
		"modo_anterior": "Automático",
	}
	for clave, valor in valores_iniciales.items():
		if clave not in st.session_state:
			st.session_state[clave] = valor

	st.header("Práctica 3: Bombas (Simulador)")
	st.caption("Transferencia virtual entre dos depósitos de 1000 ml, sin hardware.")

	@st.fragment(run_every="100ms")
	def simulador_bombas():
		nivel_a = st.session_state.nivel_a_ml
		nivel_b = CAPACIDAD_ML - nivel_a
		st.session_state.nivel_b_ml = nivel_b

		modo = st.radio(
			"Modo de operación",
			["Automático", "Manual"],
			horizontal=True,
			key="modo_bombas",
		)
		if modo != st.session_state.modo_anterior:
			st.session_state.direccion = 0
			st.session_state.simulacion_activa = False
			st.session_state.interruptor_a = 0
			st.session_state.interruptor_b = 0
			st.session_state.normalizacion_activa = False
			st.session_state.objetivo_normalizacion_ml = None
			st.session_state.accion_pendiente = None
			st.session_state.accion_confirmacion = None
			st.session_state.estado_simulador = "Sistema detenido al cambiar de modo."
			st.session_state.modo_anterior = modo

		if modo == "Automático":
			columnas = st.columns(3)
			if columnas[0].button("Llenar depósito A", use_container_width=True):
				st.session_state.interruptor_a = 0
				st.session_state.interruptor_b = 0
				st.session_state.normalizacion_activa = False
				st.session_state.accion_pendiente = None
				if nivel_a < NIVEL_MINIMO_ML or nivel_a > NIVEL_MAXIMO_ML:
					st.session_state.accion_confirmacion = 1
					st.session_state.estado_simulador = "Confirma la normalización del nivel."
				else:
					st.session_state.accion_confirmacion = None
					st.session_state.direccion = 1
					st.session_state.simulacion_activa = True
					st.session_state.estado_simulador = "Llenado automático de A en curso."

			if columnas[1].button("Vaciar depósito A", use_container_width=True):
				st.session_state.interruptor_a = 0
				st.session_state.interruptor_b = 0
				st.session_state.normalizacion_activa = False
				st.session_state.accion_pendiente = None
				if nivel_a < NIVEL_MINIMO_ML or nivel_a > NIVEL_MAXIMO_ML:
					st.session_state.accion_confirmacion = -1
					st.session_state.estado_simulador = "Confirma la normalización del nivel."
				else:
					st.session_state.accion_confirmacion = None
					st.session_state.direccion = -1
					st.session_state.simulacion_activa = True
					st.session_state.estado_simulador = "Vaciado automático de A en curso."

			if columnas[2].button("Detener", use_container_width=True):
				st.session_state.direccion = 0
				st.session_state.simulacion_activa = False
				st.session_state.interruptor_a = 0
				st.session_state.interruptor_b = 0
				st.session_state.normalizacion_activa = False
				st.session_state.objetivo_normalizacion_ml = None
				st.session_state.accion_pendiente = None
				st.session_state.accion_confirmacion = None
				st.session_state.estado_simulador = "Sistema detenido"
		else:
			interruptores = st.columns(4)
			acciones_manuales = (
				(interruptores[0], "Llenar A", "a", 1),
				(interruptores[1], "Vaciar A", "a", -1),
				(interruptores[2], "Llenar B", "b", 1),
				(interruptores[3], "Vaciar B", "b", -1),
			)
			for columna, etiqueta, deposito, direccion in acciones_manuales:
				if columna.button(etiqueta, use_container_width=True):
					st.session_state.direccion = 0
					st.session_state.simulacion_activa = False
					st.session_state.normalizacion_activa = False
					st.session_state.accion_confirmacion = None
					clave = f"interruptor_{deposito}"
					otro = "interruptor_b" if deposito == "a" else "interruptor_a"
					st.session_state[clave] = (
						0 if st.session_state[clave] == direccion else direccion
					)
					st.session_state[otro] = 0
					st.session_state.estado_simulador = (
						"Sistema detenido"
						if st.session_state[clave] == 0
						else f"Control manual activo: {etiqueta.lower()}."
					)

		if st.session_state.accion_confirmacion is not None:
			if nivel_a > NIVEL_MAXIMO_ML:
				st.warning(
					f"El depósito A está al {nivel_a / CAPACIDAD_ML:.0%} "
					f"({nivel_a} ml), por encima del máximo operativo de 800 ml. "
					"La normalización transferirá el excedente al depósito B."
				)
				objetivo = NIVEL_MAXIMO_ML
			else:
				st.warning(
					f"El depósito A está al {nivel_a / CAPACIDAD_ML:.0%} "
					f"({nivel_a} ml), por debajo del mínimo operativo de 200 ml. "
					"La normalización transferirá líquido desde el depósito B."
				)
				objetivo = NIVEL_MINIMO_ML

			with st.form("confirmar_normalizacion"):
				confirmar = st.form_submit_button("Confirmar normalización")
			if confirmar:
				st.session_state.objetivo_normalizacion_ml = objetivo
				st.session_state.normalizacion_activa = True
				st.session_state.accion_pendiente = st.session_state.accion_confirmacion
				st.session_state.accion_confirmacion = None
				st.session_state.estado_simulador = "Ajustando el nivel al rango operativo."

		if st.session_state.normalizacion_activa:
			diferencia = st.session_state.objetivo_normalizacion_ml - st.session_state.nivel_a_ml
			cambio = max(-PASO_ML, min(PASO_ML, diferencia))
			st.session_state.nivel_a_ml += cambio
			st.session_state.nivel_b_ml = CAPACIDAD_ML - st.session_state.nivel_a_ml
			if st.session_state.nivel_a_ml == st.session_state.objetivo_normalizacion_ml:
				st.session_state.normalizacion_activa = False
				st.session_state.objetivo_normalizacion_ml = None
				st.session_state.direccion = st.session_state.accion_pendiente
				st.session_state.accion_pendiente = None
				st.session_state.simulacion_activa = True
				st.session_state.estado_simulador = "Rango operativo alcanzado; bomba en curso."

		elif st.session_state.simulacion_activa:
			nuevo_nivel = st.session_state.nivel_a_ml + PASO_ML * st.session_state.direccion
			st.session_state.nivel_a_ml = max(
				NIVEL_MINIMO_ML, min(NIVEL_MAXIMO_ML, nuevo_nivel)
			)
			st.session_state.nivel_b_ml = CAPACIDAD_ML - st.session_state.nivel_a_ml
			if st.session_state.nivel_a_ml in (NIVEL_MINIMO_ML, NIVEL_MAXIMO_ML):
				st.session_state.simulacion_activa = False
				st.session_state.direccion = 0
				st.session_state.estado_simulador = "Límite operativo alcanzado."

		elif st.session_state.interruptor_a != 0:
			st.session_state.nivel_a_ml = max(
				0,
				min(CAPACIDAD_ML, st.session_state.nivel_a_ml + PASO_ML * st.session_state.interruptor_a),
			)
			st.session_state.nivel_b_ml = CAPACIDAD_ML - st.session_state.nivel_a_ml
			if st.session_state.nivel_a_ml in (0, CAPACIDAD_ML):
				st.session_state.interruptor_a = 0
				st.session_state.estado_simulador = "Límite del depósito alcanzado."

		elif st.session_state.interruptor_b != 0:
			nivel_b_nuevo = st.session_state.nivel_b_ml + PASO_ML * st.session_state.interruptor_b
			st.session_state.nivel_b_ml = max(0, min(CAPACIDAD_ML, nivel_b_nuevo))
			st.session_state.nivel_a_ml = CAPACIDAD_ML - st.session_state.nivel_b_ml
			if st.session_state.nivel_b_ml in (0, CAPACIDAD_ML):
				st.session_state.interruptor_b = 0
				st.session_state.estado_simulador = "Límite del depósito alcanzado."

		nivel_a = st.session_state.nivel_a_ml
		nivel_b = CAPACIDAD_ML - nivel_a
		st.session_state.nivel_b_ml = nivel_b
		st.caption("Capacidad total conservada: 1000 ml")

		tanques = st.columns(2)
		with tanques[0]:
			st.markdown(
				f'<div class="tank-panel"><h3>Depósito A</h3>'
				f'<div class="tank-subtitle">{nivel_a} / {CAPACIDAD_ML} ml · '
				f'{nivel_a / CAPACIDAD_ML:.0%}</div></div>',
				unsafe_allow_html=True,
			)
			st.progress(nivel_a / CAPACIDAD_ML, text=f"Nivel A: {nivel_a} ml")
		with tanques[1]:
			st.markdown(
				f'<div class="tank-panel"><h3>Depósito B</h3>'
				f'<div class="tank-subtitle">{nivel_b} / {CAPACIDAD_ML} ml · '
				f'{nivel_b / CAPACIDAD_ML:.0%}</div></div>',
				unsafe_allow_html=True,
			)
			st.progress(nivel_b / CAPACIDAD_ML, text=f"Nivel B: {nivel_b} ml")

		st.markdown(
			f'<div class="status-line">{st.session_state.estado_simulador}</div>',
			unsafe_allow_html=True,
		)

	simulador_bombas()