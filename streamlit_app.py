import streamlit as st

from practicas.bombas.app import render as render_bombas
from practicas.caja_termica.app import render as render_caja_termica
from practicas.led.app import render as render_led
from practicas.rele.app import render as render_rele

st.set_page_config(
	page_title="Portafolio Carlos Ordóñez",
	page_icon="⚙️",
	layout="wide",
)

st.markdown(
	"""
	<style>
	.stApp {
		background: #0d1117;
		color: #e6edf3;
		font-family: 'Segoe UI', sans-serif;
	}
	[data-testid="stSidebar"] { background: #161b22; }
	[data-testid="stMainBlockContainer"] {
		max-width: 100%;
		padding-left: clamp(1rem, 3vw, 3rem);
		padding-right: clamp(1rem, 3vw, 3rem);
	}
	.st-key-portfolio_header {
		position: sticky;
		top: 3rem;
		z-index: 1000;
		padding: .7rem 0;
		margin-bottom: 1.25rem;
		border-bottom: 1px solid #30363d;
		background: rgba(13, 17, 23, .96);
		backdrop-filter: blur(12px);
	}
	.portfolio-header-content {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
	}
	.portfolio-header-content strong { font-size: 1rem; }
	.portfolio-header-content p {
		margin: .2rem 0 0;
		color: #9da7b3;
		font-size: .875rem;
	}
	.portfolio-header-content a {
		flex-shrink: 0;
		color: #58a6ff;
		font-size: .875rem;
		font-weight: 600;
		text-decoration: none;
	}
	.portfolio-header-content a:hover { text-decoration: underline; }
	@media (max-width: 640px) {
		[data-testid="stMainBlockContainer"] {
			padding-left: 1rem;
			padding-right: 1rem;
		}
		.portfolio-header-content { align-items: flex-start; }
		.portfolio-header-content p { font-size: .8rem; }
	}
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
	"Proyectos",
	[
		"💡 LED",
		"⚙️ Relé",
		"🌊 Bombas",
		"🌡️ Caja térmica",
	],
	label_visibility="collapsed",
)

with st.container(key="portfolio_header"):
	st.markdown(
		"""
		<div class="portfolio-header-content">
			<div>
				<strong>Portafolio interactivo de sistemas embebidos</strong>
				<p>Simulaciones de electrónica y control, sin necesidad de hardware físico.</p>
			</div>
			<a href="https://github.com/CarlosOrdonez-upb" target="_blank"
				rel="noopener noreferrer">GitHub ↗</a>
		</div>
		""",
		unsafe_allow_html=True,
	)

if pagina == "💡 LED":
	render_led()
elif pagina == "⚙️ Relé":
	render_rele()
elif pagina == "🌊 Bombas":
	render_bombas()
elif pagina == "🌡️ Caja térmica":
	render_caja_termica()
