import streamlit as st

from practicas.bombas.app import render as render_bombas
from practicas.caja_termica.app import render as render_caja_termica
from practicas.led.app import render as render_led
from practicas.rele.app import render as render_rele

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
	render_led()
elif pagina == "⚙️ Relé":
	render_rele()
elif pagina == "🌊 Bombas":
	render_bombas()
elif pagina == "🌡️ Caja térmica":
	render_caja_termica()
