import streamlit as st
import streamlit.components.v1 as components


def render():
	st.header("⚙️ Control de relé")
	st.caption("Simulación del control de un relé realizada en Wokwi.")
	components.html(
		'<iframe src="https://wokwi.com/projects/476381886558822401?embed=1" '
		'title="Simulación de control de relé en Wokwi" width="100%" height="600" '
		'style="border: 1px solid #30363d; border-radius: 6px;" allowfullscreen></iframe>',
		height=600,
		scrolling=False,
	)
