import streamlit as st

st.set_page_config(page_title="Portafolio Carlos Ordóñez", page_icon="⚙️")

st.title("⚙️ Portafolio de Sistemas Embebidos")
st.write("¡Hola! Esta es mi aplicación web de Streamlit corriendo desde mi PC.")
st.success("Si ves esto, ¡la configuración local fue un éxito! 🚀")

st.markdown("---")
st.subheader("Próximas prácticas:")
st.markdown("- [ ] Práctica 1: Control de LED")
st.markdown("- [ ] Práctica 2: Control de Relé")
st.markdown("- [ ] Práctica 3: Simulador de Bombas (Gemelo Digital)")

CAPACIDAD_ML = 1000
NIVEL_MINIMO_ML = 200
NIVEL_MAXIMO_ML = 800
PASO_ML = 10

_estado_inicial = {
	"nivel_a_ml": 500,
	"nivel_b_ml": 500,
	"direccion": 0,
	"simulacion_activa": False,
	"interruptor_a": 0,
	"interruptor_b": 0,
	"normalizacion_activa": False,
	"accion_pendiente": None,
	"objetivo_normalizacion_ml": None,
	"modo_bombas": "Automático",
	"estado_bombas": "Sistema detenido",
}

for _clave, _valor in _estado_inicial.items():
	if _clave not in st.session_state:
		st.session_state[_clave] = _valor


def _detener_bombas():
	st.session_state.direccion = 0
	st.session_state.simulacion_activa = False
	st.session_state.interruptor_a = 0
	st.session_state.interruptor_b = 0
	st.session_state.normalizacion_activa = False
	st.session_state.accion_pendiente = None
	st.session_state.objetivo_normalizacion_ml = None
	st.session_state.estado_bombas = "Sistema detenido"


def _iniciar_bomba(direccion):
	nivel_a = st.session_state.nivel_a_ml
	if not NIVEL_MINIMO_ML <= nivel_a <= NIVEL_MAXIMO_ML:
		st.session_state.accion_pendiente = direccion
		st.session_state.objetivo_normalizacion_ml = (
			NIVEL_MAXIMO_ML if nivel_a > NIVEL_MAXIMO_ML else NIVEL_MINIMO_ML
		)
		st.session_state.estado_bombas = "Confirme la normalización para continuar"
		return

	st.session_state.interruptor_a = 0
	st.session_state.interruptor_b = 0
	st.session_state.direccion = direccion
	st.session_state.simulacion_activa = True
	st.session_state.normalizacion_activa = False
	st.session_state.estado_bombas = (
		"Bomba activa: A recibe líquido de B"
		if direccion == 1
		else "Bomba activa: A envía líquido hacia B"
	)


def _activar_interruptor(deposito, direccion):
	st.session_state.direccion = 0
	st.session_state.simulacion_activa = False
	st.session_state.normalizacion_activa = False
	if deposito == "a":
		st.session_state.interruptor_a = (
			0 if st.session_state.interruptor_a == direccion else direccion
		)
		st.session_state.interruptor_b = 0
	else:
		st.session_state.interruptor_b = (
			0 if st.session_state.interruptor_b == direccion else direccion
		)
		st.session_state.interruptor_a = 0

	interruptores_activos = (
		st.session_state.interruptor_a != 0
		or st.session_state.interruptor_b != 0
	)
	if interruptores_activos:
		accion = "llenado" if direccion == 1 else "vaciado"
		st.session_state.estado_bombas = (
			f"Control manual activo: {accion} del depósito {deposito.upper()}"
		)
	else:
		st.session_state.estado_bombas = "Sistema detenido"


def _avanzar_ciclo():
	if st.session_state.normalizacion_activa:
		diferencia = (
			st.session_state.objetivo_normalizacion_ml
			- st.session_state.nivel_a_ml
		)
		cambio = max(-PASO_ML, min(PASO_ML, diferencia))
		st.session_state.nivel_a_ml += cambio
		st.session_state.nivel_b_ml = CAPACIDAD_ML - st.session_state.nivel_a_ml
		if st.session_state.nivel_a_ml == st.session_state.objetivo_normalizacion_ml:
			st.session_state.normalizacion_activa = False
			accion = st.session_state.accion_pendiente
			st.session_state.accion_pendiente = None
			st.session_state.objetivo_normalizacion_ml = None
			if accion is not None:
				st.session_state.direccion = accion
				st.session_state.simulacion_activa = True
				st.session_state.estado_bombas = "Rango operativo alcanzado; bomba activa"
			else:
				st.session_state.estado_bombas = "Rango operativo alcanzado"
		return

	if st.session_state.interruptor_a:
		st.session_state.nivel_a_ml = max(
			0,
			min(
				CAPACIDAD_ML,
				st.session_state.nivel_a_ml + PASO_ML * st.session_state.interruptor_a,
			),
		)
		st.session_state.nivel_b_ml = CAPACIDAD_ML - st.session_state.nivel_a_ml
	elif st.session_state.interruptor_b:
		st.session_state.nivel_b_ml = max(
			0,
			min(
				CAPACIDAD_ML,
				st.session_state.nivel_b_ml + PASO_ML * st.session_state.interruptor_b,
			),
		)
		st.session_state.nivel_a_ml = CAPACIDAD_ML - st.session_state.nivel_b_ml
	elif st.session_state.simulacion_activa:
		st.session_state.nivel_a_ml = max(
			NIVEL_MINIMO_ML,
			min(
				NIVEL_MAXIMO_ML,
				st.session_state.nivel_a_ml + PASO_ML * st.session_state.direccion,
			),
		)
		st.session_state.nivel_b_ml = CAPACIDAD_ML - st.session_state.nivel_a_ml

	limite_auto = st.session_state.nivel_a_ml in (
		NIVEL_MINIMO_ML,
		NIVEL_MAXIMO_ML,
	)
	limite_manual = (
		st.session_state.interruptor_a == 1
		and st.session_state.nivel_a_ml == CAPACIDAD_ML
	) or (
		st.session_state.interruptor_a == -1
		and st.session_state.nivel_a_ml == 0
	) or (
		st.session_state.interruptor_b == 1
		and st.session_state.nivel_b_ml == CAPACIDAD_ML
	) or (
		st.session_state.interruptor_b == -1
		and st.session_state.nivel_b_ml == 0
	)
	if (st.session_state.simulacion_activa and limite_auto) or limite_manual:
		nivel_a = st.session_state.nivel_a_ml
		nivel_b = st.session_state.nivel_b_ml
		_detener_bombas()
		st.session_state.estado_bombas = (
			f"Límite alcanzado: A={nivel_a} ml / B={nivel_b} ml"
		)


st.markdown("---")
st.header("Práctica 3: Bombas (Simulador)")
st.caption("Transferencia simulada entre depósitos, sin hardware externo.")

st.markdown(
	"""
	<style>
	.stApp, [data-testid="stAppViewContainer"] { background: #10151b; color: #e8edf2; }
	[data-testid="stHeader"] { background: transparent; }
	[data-testid="stMarkdownContainer"], [data-testid="stRadio"] { color: #e8edf2; }
	div.stButton > button { background: #202a34; color: #edf2f6; border: 1px solid #46515d; }
	div.stButton > button:hover { background: #2b3946; border-color: #6a7886; color: #ffffff; }
	.tank-panel { background: #171c22; border: 1px solid #303944; border-radius: 8px; padding: 18px; }
	.tank-heading { color: #e8edf2; font-size: 1rem; font-weight: 700; margin-bottom: 8px; }
	.tank-track { height: 24px; background: #0c1116; border: 1px solid #46515d; border-radius: 4px; overflow: hidden; }
	.tank-fill { height: 100%; transition: width 120ms linear; }
	.tank-a { background: #2785d8; }
	.tank-b { background: #28a879; }
	.tank-value { color: #c8d1da; font-size: .9rem; margin-top: 8px; }
	</style>
	""",
	unsafe_allow_html=True,
)


@st.fragment(run_every="1s")
def _simulador_bombas():
	st.radio(
		"Modo de operación",
		("Automático", "Manual"),
		horizontal=True,
		key="modo_bombas",
	)

	if st.session_state.modo_bombas == "Automático":
		controles = st.columns(3)
		if controles[0].button("Llenar depósito A", use_container_width=True):
			_iniciar_bomba(1)
		if controles[1].button("Vaciar depósito A", use_container_width=True):
			_iniciar_bomba(-1)
		if controles[2].button("Detener", use_container_width=True):
			_detener_bombas()
	else:
		for deposito, columna in (("a", 0), ("b", 1)):
			with st.container(border=True):
				st.markdown(f"**Depósito {deposito.upper()}**")
				controles = st.columns(2)
				if controles[0].button(
					"Llenar", key=f"llenar_{deposito}", use_container_width=True
				):
					_activar_interruptor(deposito, 1)
				if controles[1].button(
					"Vaciar", key=f"vaciar_{deposito}", use_container_width=True
				):
					_activar_interruptor(deposito, -1)
		if st.button("Detener control manual", use_container_width=True):
			_detener_bombas()

	if st.session_state.accion_pendiente is not None:
		nivel = st.session_state.nivel_a_ml
		destino = st.session_state.objetivo_normalizacion_ml
		st.warning(
			f"El nivel de A está fuera del rango operativo 20%-80% "
			f"({nivel} ml). Se transferirá hasta {destino} ml antes de iniciar la bomba."
		)
		with st.form("confirmar_normalizacion"):
			st.info("La normalización conservará el volumen total de ambos depósitos.")
			confirmar = st.form_submit_button("Confirmar normalización")
		if confirmar:
			st.session_state.normalizacion_activa = True
			st.session_state.estado_bombas = "Normalizando nivel del depósito A..."

	if (
		st.session_state.simulacion_activa
		or st.session_state.normalizacion_activa
		or st.session_state.interruptor_a
		or st.session_state.interruptor_b
	):
		_avanzar_ciclo()

	niveles = (
		("Depósito A", st.session_state.nivel_a_ml, "tank-a"),
		("Depósito B", st.session_state.nivel_b_ml, "tank-b"),
	)
	columnas = st.columns(2)
	for columna, (nombre, nivel, clase) in zip(columnas, niveles):
		porcentaje = nivel / CAPACIDAD_ML * 100
		with columna:
			st.markdown(
				f'<div class="tank-panel"><div class="tank-heading">{nombre}</div>'
				f'<div class="tank-track"><div class="tank-fill {clase}" '
				f'style="width: {porcentaje:.1f}%"></div></div>'
				f'<div class="tank-value">{nivel} / {CAPACIDAD_ML} ml · '
				f'{porcentaje:.0f}%</div></div>',
				unsafe_allow_html=True,
			)

	st.progress(
		st.session_state.nivel_a_ml / CAPACIDAD_ML,
		text=f"Balance de masa: {st.session_state.nivel_a_ml} + "
		f"{st.session_state.nivel_b_ml} = {CAPACIDAD_ML} ml",
	)
	st.caption(st.session_state.estado_bombas)


_simulador_bombas()