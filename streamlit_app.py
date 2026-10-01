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
	.thermal-box {
		border: 8px solid #8b5a2b;
		border-radius: 14px;
		padding: 1.5rem;
		min-height: 180px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		color: #0d1117;
		transition: background .4s ease;
	}
	.thermal-box h3 { color: #0d1117; margin: 0; }
	.thermal-components {
		display: flex;
		justify-content: space-between;
		gap: .5rem;
		flex-wrap: wrap;
	}
	.thermal-component {
		padding: .4rem .65rem;
		background: rgba(255,255,255,.75);
		border-radius: 6px;
		font-weight: 600;
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
		"💡 LED",
		"⚙️ Relé",
		"🌊 Bombas",
		"🌡️ Caja térmica",
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
elif pagina == "💡 LED":
	st.header("💡 Control de LED")
	st.caption("Simulación del control de un LED realizada en Wokwi.")
	components.html(
		'<iframe src="https://wokwi.com/projects/476381725083303937?embed=1" '
		'title="Simulación de control de LED en Wokwi" width="100%" height="600" '
		'style="border: 1px solid #30363d; border-radius: 6px;" allowfullscreen></iframe>',
		height=600,
		scrolling=False,
	)
elif pagina == "⚙️ Relé":
	st.header("⚙️ Control de relé")
	st.caption("Simulación del control de un relé realizada en Wokwi.")
	components.html(
		'<iframe src="https://wokwi.com/projects/476381886558822401?embed=1" '
		'title="Simulación de control de relé en Wokwi" width="100%" height="600" '
		'style="border: 1px solid #30363d; border-radius: 6px;" allowfullscreen></iframe>',
		height=600,
		scrolling=False,
	)
elif pagina == "🌊 Bombas":
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

	st.header("Simulador de bombas")
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
elif pagina == "🌡️ Caja térmica":
	valores_iniciales = {
		"temperatura_caja": 24.0,
		"humedad_caja": 55.0,
		"simulacion_caja_activa": False,
		"puerta_caja_abierta": False,
		"accion_manual_caja": "Mantener",
	}
	for clave, valor in valores_iniciales.items():
		if clave not in st.session_state:
			st.session_state[clave] = valor

	st.header("Simulador de caja térmica")
	st.caption(
		"Control virtual de temperatura con foco calefactor, módulo Peltier, "
		"ventiladores y puertas. No requiere ESP32 ni conexión serial."
	)

	@st.fragment(run_every="500ms")
	def simulador_caja_termica():
		columnas_ajustes = st.columns(3)
		with columnas_ajustes[0]:
			modo = st.selectbox(
				"Modo de operación",
				["Automático", "Manual"],
				key="modo_caja_termica",
			)
			objetivo = st.slider(
				"Temperatura objetivo (°C)",
				min_value=20.0,
				max_value=50.0,
				value=35.0,
				step=0.5,
				key="objetivo_caja_termica",
			)
		with columnas_ajustes[1]:
			temperatura_ambiente = st.slider(
				"Temperatura ambiente (°C)",
				min_value=10.0,
				max_value=40.0,
				value=22.0,
				step=0.5,
				key="ambiente_caja_termica",
			)
			humedad_ambiente = st.slider(
				"Humedad ambiente (%)",
				min_value=20,
				max_value=90,
				value=50,
				key="humedad_ambiente_caja",
			)
		with columnas_ajustes[2]:
			if st.button(
				"Detener simulación" if st.session_state.simulacion_caja_activa
				else "Iniciar simulación",
				use_container_width=True,
				type="primary",
			):
				st.session_state.simulacion_caja_activa = (
					not st.session_state.simulacion_caja_activa
				)
			if st.button(
				"Cerrar puerta" if st.session_state.puerta_caja_abierta
				else "Abrir puerta",
				use_container_width=True,
			):
				st.session_state.puerta_caja_abierta = (
					not st.session_state.puerta_caja_abierta
				)

		if modo == "Manual":
			st.caption("Selecciona una acción para los actuadores:")
			acciones = st.columns(3)
			for columna, accion in zip(
				acciones, ("Calentar", "Enfriar", "Mantener")
			):
				if columna.button(accion, use_container_width=True):
					st.session_state.accion_manual_caja = accion

		temperatura = st.session_state.temperatura_caja
		humedad = st.session_state.humedad_caja
		foco_activo = False
		peltier_activo = False
		ventiladores_activos = False
		if st.session_state.simulacion_caja_activa:
			if st.session_state.puerta_caja_abierta:
				temperatura += max(
					-0.15, min(0.15, (temperatura_ambiente - temperatura) * 0.03)
				)
				humedad += max(
					-0.5, min(0.5, (humedad_ambiente - humedad) * 0.03)
				)
				ventiladores_activos = True
				estado = "Ventilando la caja con la puerta abierta."
			else:
				accion = (
					"Automático" if modo == "Automático"
					else st.session_state.accion_manual_caja
				)
				if accion == "Automático":
					if temperatura < objetivo - 0.3:
						accion = "Calentar"
					elif temperatura > objetivo + 0.3:
						accion = "Enfriar"
					else:
						accion = "Mantener"

				if accion == "Calentar":
					temperatura = min(50.0, temperatura + 0.12)
					humedad = max(20.0, humedad - 0.015)
					foco_activo = True
					ventiladores_activos = True
					estado = "Calentando hasta alcanzar la temperatura objetivo."
				elif accion == "Enfriar":
					temperatura = max(10.0, temperatura - 0.14)
					humedad = min(90.0, humedad + 0.015)
					peltier_activo = True
					ventiladores_activos = True
					estado = "Enfriando hasta alcanzar la temperatura objetivo."
				else:
					estado = "Temperatura estable; actuadores en espera."
			st.session_state.temperatura_caja = temperatura
			st.session_state.humedad_caja = humedad
		else:
			estado = "Simulación detenida."

		temperatura = st.session_state.temperatura_caja
		humedad = st.session_state.humedad_caja
		indicadores = st.columns(3)
		indicadores[0].metric("Temperatura", f"{temperatura:.1f} °C")
		indicadores[1].metric("Objetivo", f"{objetivo:.1f} °C")
		indicadores[2].metric("Humedad", f"{humedad:.0f}%")
		st.progress(
			max(0.0, min(1.0, (temperatura - 10.0) / 40.0)),
			text="Rango del sensor: 10–50 °C",
		)

		if temperatura < 25:
			color_caja = "#9bd7f5"
		elif temperatura < 30:
			color_caja = "#d3d8d6"
		else:
			color_caja = "#f5a39a"
		puerta = "Abierta" if st.session_state.puerta_caja_abierta else "Cerrada"
		st.markdown(
			f'<div class="thermal-box" style="background:{color_caja}">'
			f'<h3>Cámara térmica · {temperatura:.1f} °C</h3>'
			'<div class="thermal-components">'
			f'<span class="thermal-component">Foco: {"Activo" if foco_activo else "Apagado"}</span>'
			f'<span class="thermal-component">Peltier: {"Activo" if peltier_activo else "Apagado"}</span>'
			f'<span class="thermal-component">Ventiladores: {"Activos" if ventiladores_activos else "Detenidos"}</span>'
			f'<span class="thermal-component">Puerta: {puerta}</span>'
			'</div></div>',
			unsafe_allow_html=True,
		)
		st.markdown(
			f'<div class="status-line">{estado}</div>',
			unsafe_allow_html=True,
		)

	simulador_caja_termica()