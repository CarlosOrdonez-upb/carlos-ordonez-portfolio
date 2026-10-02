import streamlit.components.v1 as components


def render():
	components.html(
		r"""
		<!doctype html>
		<html lang="es">
		<head>
			<meta charset="utf-8">
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<style>
				:root {
					color-scheme: dark;
					font-family: "Segoe UI", sans-serif;
					background: #0d1117;
					color: #e6edf3;
				}
				* { box-sizing: border-box; }
				body { margin: 0; background: #0d1117; }
				.simulator {
					padding: 1rem;
					border: 1px solid #30363d;
					border-radius: 12px;
					background: #10161f;
				}
				h2 { margin: 0 0 .3rem; font-size: 1.35rem; }
				.subtitle { margin: 0 0 1rem; color: #9da7b3; line-height: 1.5; }
				.layout { display: grid; grid-template-columns: minmax(0, 1.65fr) minmax(230px, .8fr); gap: 1rem; }
				.visual, .controls {
					border: 1px solid #30363d;
					border-radius: 10px;
					background: #161b22;
				}
				.visual { padding: .6rem; min-width: 0; }
				svg { display: block; width: 100%; height: auto; }
				.controls { padding: 1rem; }
				.metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: .55rem; margin-bottom: .75rem; }
				.metric { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: .65rem; }
				.metric-label { display: block; color: #9da7b3; font-size: .75rem; margin-bottom: .25rem; }
				.metric-value { font-size: 1.1rem; font-weight: 700; }
				.control { margin: .8rem 0; }
				label { display: block; font-size: .88rem; font-weight: 600; margin-bottom: .35rem; }
				select, input[type="range"] { width: 100%; }
				select {
					background: #0d1117; color: #e6edf3; border: 1px solid #484f58;
					border-radius: 6px; padding: .55rem;
				}
				input[type="range"] { accent-color: #2ea043; }
				.range-value { float: right; color: #9da7b3; font-weight: 400; }
				.buttons { display: grid; grid-template-columns: 1fr 1fr; gap: .5rem; margin-top: 1rem; }
				button {
					border: 1px solid #2ea043; border-radius: 6px; padding: .65rem .5rem;
					background: #238636; color: white; font-weight: 650; cursor: pointer;
					transition: background .2s ease, transform .2s ease;
				}
				button:hover { background: #2ea043; transform: translateY(-1px); }
				button.secondary { background: #21262d; border-color: #484f58; }
				button.secondary:hover { background: #30363d; }
				.status { margin-top: .8rem; border-left: 3px solid #58a6ff; padding: .6rem .7rem; background: #0d1117; font-size: .88rem; }
				.legend { color: #9da7b3; font-size: .75rem; line-height: 1.45; margin: .75rem 0 0; }
				.room { transition: fill .45s ease; }
				.door { transition: transform .75s cubic-bezier(.2,.8,.2,1); transform-box: view-box; }
				.door-left { transform-origin: 202px 235px; }
				.door-right { transform-origin: 698px 235px; }
				.doors-open .door-left { transform: rotate(-66deg); }
				.doors-open .door-right { transform: rotate(66deg); }
				.fan-rotor { transform-box: fill-box; transform-origin: center; }
				.fans-on .fan-rotor { animation: spin .75s linear infinite; }
				@keyframes spin { to { transform: rotate(360deg); } }
				.airflow {
					fill: none; stroke: rgba(255,255,255,.72); stroke-width: 4;
					stroke-dasharray: 8 13; opacity: 0; transition: opacity .3s ease;
					animation: air 1.1s linear infinite;
				}
				.air-on .airflow { opacity: .75; }
				@keyframes air { to { stroke-dashoffset: -42; } }
				.particles { opacity: 0; transition: opacity .25s ease; }
				.mode-heating .heat-particles, .mode-cooling .snow-particles,
				.mode-purge .purge-particles { opacity: 1; }
				.heat-particle, .snow-particle, .purge-particle {
					animation-duration: 2.8s; animation-iteration-count: infinite;
					animation-timing-function: ease-in-out;
				}
				.heat-particle { fill: #ff5a36; filter: drop-shadow(0 0 5px #ff4d36); animation-name: rise; }
				@keyframes rise {
					0% { transform: translateY(45px) scale(.65); opacity: 0; }
					20% { opacity: 1; }
					100% { transform: translateY(-100px) scale(1.05); opacity: 0; }
				}
				.snow-particle { fill: #dff7ff; font: 25px sans-serif; animation-name: fall; }
				@keyframes fall {
					0% { transform: translateY(-75px) rotate(0deg); opacity: 0; }
					15% { opacity: 1; }
					100% { transform: translateY(90px) rotate(100deg); opacity: 0; }
				}
				.purge-particle { fill: #b8c0c8; animation-name: exhaust; }
				@keyframes exhaust {
					0% { transform: translateX(-100px); opacity: 0; }
					15% { opacity: .9; }
					100% { transform: translateX(370px); opacity: 0; }
				}
				.p1 { animation-delay: -.2s; }
				.p2 { animation-delay: -.8s; }
				.p3 { animation-delay: -1.4s; }
				.p4 { animation-delay: -2s; }
				.p5 { animation-delay: -.5s; }
				.p6 { animation-delay: -1.1s; }
				.p7 { animation-delay: -1.7s; }
				.p8 { animation-delay: -2.3s; }
				.component-label { fill: #e6edf3; font: 13px "Segoe UI", sans-serif; font-weight: 600; }
				.frame-label { fill: #d2a679; font: 12px "Segoe UI", sans-serif; }
				@media (max-width: 720px) {
					.layout { grid-template-columns: 1fr; }
					.controls { order: -1; }
					.simulator { padding: .65rem; }
				}
			</style>
		</head>
		<body>
			<main class="simulator">
				<h2>Simulador de caja térmica</h2>
				<p class="subtitle">Control virtual de temperatura con foco, módulo Peltier,
					ventiladores y puertas. No necesita ESP32 ni conexión serial.</p>
				<div class="metrics">
					<div class="metric"><span class="metric-label">Temperatura</span><span class="metric-value" id="tempValue">24.0 °C</span></div>
					<div class="metric"><span class="metric-label">Objetivo</span><span class="metric-value" id="targetValue">35.0 °C</span></div>
					<div class="metric"><span class="metric-label">Humedad</span><span class="metric-value" id="humidityValue">55%</span></div>
				</div>
				<div class="layout">
					<div class="visual">
						<svg id="thermalSvg" viewBox="0 0 900 470" role="img" aria-labelledby="svgTitle svgDesc">
							<title id="svgTitle">Caja térmica animada</title>
							<desc id="svgDesc">Cámara térmica con foco, celda Peltier, dos ventiladores, partículas de aire y puertas móviles.</desc>
							<defs>
								<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
									<stop offset="0" stop-color="#bd8753"/>
									<stop offset="1" stop-color="#75451f"/>
								</linearGradient>
								<clipPath id="insideClip"><rect x="174" y="82" width="552" height="306" rx="4"/></clipPath>
								<marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
									<path d="M0,0 L0,6 L7,3 z" fill="#e6edf3"/>
								</marker>
							</defs>
							<rect x="145" y="53" width="610" height="370" rx="18" fill="url(#wall)" stroke="#e0b887" stroke-width="4"/>
							<rect class="room" id="room" x="170" y="78" width="560" height="320" rx="6" fill="#9bd7f5" stroke="#513219" stroke-width="4"/>
							<g clip-path="url(#insideClip)">
								<path class="airflow" d="M255 290 C330 325 410 325 450 250 S570 170 650 205" marker-end="url(#arrow)"/>
								<path class="airflow" d="M645 285 C565 345 465 345 435 280 S330 180 255 210" marker-end="url(#arrow)"/>
								<g class="particles heat-particles">
									<circle class="heat-particle p1" cx="240" cy="335" r="8"/><circle class="heat-particle p2" cx="300" cy="300" r="6"/>
									<circle class="heat-particle p3" cx="365" cy="350" r="9"/><circle class="heat-particle p4" cx="425" cy="315" r="7"/>
									<circle class="heat-particle p5" cx="490" cy="345" r="6"/><circle class="heat-particle p6" cx="550" cy="305" r="9"/>
									<circle class="heat-particle p7" cx="610" cy="345" r="7"/><circle class="heat-particle p8" cx="675" cy="310" r="8"/>
								</g>
								<g class="particles snow-particles">
									<text class="snow-particle p1" x="230" y="160">❄</text><text class="snow-particle p2" x="295" y="185">❄</text>
									<text class="snow-particle p3" x="360" y="150">❄</text><text class="snow-particle p4" x="425" y="180">❄</text>
									<text class="snow-particle p5" x="490" y="155">❄</text><text class="snow-particle p6" x="555" y="185">❄</text>
									<text class="snow-particle p7" x="620" y="150">❄</text><text class="snow-particle p8" x="675" y="180">❄</text>
								</g>
								<g class="particles purge-particles">
									<circle class="purge-particle p1" cx="195" cy="160" r="6"/><circle class="purge-particle p2" cx="220" cy="205" r="8"/>
									<circle class="purge-particle p3" cx="190" cy="250" r="5"/><circle class="purge-particle p4" cx="230" cy="300" r="7"/>
									<circle class="purge-particle p5" cx="200" cy="345" r="6"/><circle class="purge-particle p6" cx="215" cy="180" r="5"/>
									<circle class="purge-particle p7" cx="190" cy="280" r="8"/><circle class="purge-particle p8" cx="225" cy="330" r="5"/>
								</g>
								<g id="heater">
									<rect x="410" y="96" width="80" height="28" rx="8" fill="#333b42" stroke="#111820" stroke-width="3"/>
									<path d="M425 110 Q433 96 441 110 T457 110 T473 110" fill="none" stroke="#ffcc55" stroke-width="5" stroke-linecap="round"/>
									<text class="component-label" x="435" y="145">Foco</text>
								</g>
								<g id="peltier">
									<rect x="397" y="355" width="106" height="25" rx="4" fill="#333b42" stroke="#111820" stroke-width="3"/>
									<path d="M410 360v15m12-15v15m12-15v15m12-15v15m12-15v15m12-15v15m12-15v15" stroke="#75d5ff" stroke-width="4"/>
									<text class="component-label" x="417" y="402">Módulo Peltier</text>
								</g>
								<g id="fan1" transform="translate(250 235)">
									<circle r="42" fill="#c8d2d0" stroke="#586b6b" stroke-width="4"/>
									<circle r="34" fill="#aebbb9" stroke="#7d8b89" stroke-width="2"/>
									<g class="fan-rotor">
										<path d="M0-5 Q-19-12 -19-29 Q-18-39 -8-35 Q4-27 4-7Z" fill="#34464a"/>
										<path d="M4 2 Q12 19 29 18 Q39 17 35 8 Q27-4 7-5Z" fill="#34464a"/>
										<path d="M-4 4 Q-19 13 -18 29 Q-17 39 -8 35 Q4 27 5 7Z" fill="#34464a"/>
										<circle r="7" fill="#e6b35d"/>
									</g>
								</g>
								<g id="fan2" transform="translate(650 235)">
									<circle r="42" fill="#c8d2d0" stroke="#586b6b" stroke-width="4"/>
									<circle r="34" fill="#aebbb9" stroke="#7d8b89" stroke-width="2"/>
									<g class="fan-rotor">
										<path d="M0-5 Q-19-12 -19-29 Q-18-39 -8-35 Q4-27 4-7Z" fill="#34464a"/>
										<path d="M4 2 Q12 19 29 18 Q39 17 35 8 Q27-4 7-5Z" fill="#34464a"/>
										<path d="M-4 4 Q-19 13 -18 29 Q-17 39 -8 35 Q4 27 5 7Z" fill="#34464a"/>
										<circle r="7" fill="#e6b35d"/>
									</g>
								</g>
								<text class="component-label" x="217" y="295">Ventilador</text>
								<text class="component-label" x="617" y="295">Ventilador</text>
							</g>
							<g class="door door-left">
								<rect x="202" y="187" width="96" height="96" rx="8" fill="#83aeb8" fill-opacity=".82" stroke="#d8e3e5" stroke-width="4"/>
								<path d="M210 195v80" stroke="#e6edf3" stroke-opacity=".6" stroke-width="2"/>
								<rect x="280" y="222" width="8" height="26" rx="4" fill="#e6b35d"/>
							</g>
							<g class="door door-right">
								<rect x="602" y="187" width="96" height="96" rx="8" fill="#83aeb8" fill-opacity=".82" stroke="#d8e3e5" stroke-width="4"/>
								<path d="M690 195v80" stroke="#e6edf3" stroke-opacity=".6" stroke-width="2"/>
								<rect x="608" y="222" width="8" height="26" rx="4" fill="#e6b35d"/>
							</g>
							<text class="frame-label" x="349" y="445">Cámara térmica · simulación visual</text>
						</svg>
					</div>
					<aside class="controls">
						<div class="control">
							<label for="mode">Modo de operación</label>
							<select id="mode"><option>Automático</option><option>Manual</option></select>
						</div>
						<div class="control" id="manualControl" hidden>
							<label for="manualAction">Acción manual</label>
							<select id="manualAction"><option>Calentar</option><option>Enfriar</option><option>Mantener</option></select>
						</div>
						<div class="control">
							<label for="target">Temperatura objetivo <span class="range-value" id="targetLabel">35.0 °C</span></label>
							<input id="target" type="range" min="20" max="50" value="35" step="0.5">
						</div>
						<div class="control">
							<label for="ambient">Temperatura ambiente <span class="range-value" id="ambientLabel">22.0 °C</span></label>
							<input id="ambient" type="range" min="10" max="40" value="22" step="0.5">
						</div>
						<div class="control">
							<label for="humidity">Humedad ambiente <span class="range-value" id="humidityLabel">50%</span></label>
							<input id="humidity" type="range" min="20" max="90" value="50" step="1">
						</div>
						<div class="buttons">
							<button id="startButton" type="button">Iniciar</button>
							<button class="secondary" id="doorButton" type="button">Abrir puertas</button>
						</div>
						<div class="status" id="status" aria-live="polite">Simulación detenida.</div>
						<p class="legend">Rojo: calentamiento · ❄: enfriamiento · Gris: extracción de aire.<br>El color del interior cambia gradualmente con la temperatura.</p>
					</aside>
				</div>
			</main>
			<script>
				const svg = document.getElementById("thermalSvg");
				const room = document.getElementById("room");
				const modeSelect = document.getElementById("mode");
				const manualControl = document.getElementById("manualControl");
				const manualAction = document.getElementById("manualAction");
				const target = document.getElementById("target");
				const ambient = document.getElementById("ambient");
				const ambientHumidity = document.getElementById("humidity");
				const startButton = document.getElementById("startButton");
				const doorButton = document.getElementById("doorButton");
				const tempValue = document.getElementById("tempValue");
				const targetValue = document.getElementById("targetValue");
				const humidityValue = document.getElementById("humidityValue");
				const status = document.getElementById("status");
				let temperature = 24;
				let humidity = 55;
				let running = false;
				let doorOpen = false;
				let lastFrame = performance.now();

				function updateSliderLabels() {
					document.getElementById("targetLabel").textContent = `${Number(target.value).toFixed(1)} °C`;
					document.getElementById("ambientLabel").textContent = `${Number(ambient.value).toFixed(1)} °C`;
					document.getElementById("humidityLabel").textContent = `${ambientHumidity.value}%`;
					targetValue.textContent = `${Number(target.value).toFixed(1)} °C`;
				}

				function blendColor(a, b, amount) {
					const start = a.match(/[A-Fa-f0-9]{2}/g).map(value => parseInt(value, 16));
					const end = b.match(/[A-Fa-f0-9]{2}/g).map(value => parseInt(value, 16));
					const color = start.map((value, index) =>
						Math.round(value + (end[index] - value) * amount)
							.toString(16).padStart(2, "0")
					).join("");
					return `#${color}`;
				}

				function temperatureColor(value) {
					if (value < 25) return blendColor("#64b5e8", "#d3d8d6", (value - 10) / 15);
					return blendColor("#d3d8d6", "#f5a39a", Math.min(1, (value - 25) / 15));
				}

				function setModeClass(nextMode) {
					svg.classList.remove("mode-heating", "mode-cooling", "mode-purge", "mode-idle");
					svg.classList.add(`mode-${nextMode}`);
					const active = running && nextMode !== "idle";
					svg.classList.toggle("fans-on", running && nextMode === "purge");
					svg.classList.toggle("air-on", active);
					document.getElementById("heater").style.opacity = nextMode === "heating" ? "1" : ".55";
					document.getElementById("peltier").style.opacity = nextMode === "cooling" ? "1" : ".55";
				}

				function updateFrame(now) {
					const elapsed = Math.min((now - lastFrame) / 1000, .1);
					lastFrame = now;
					let action = "idle";
					let message = running ? "Temperatura estable; actuadores en espera." : "Simulación detenida.";

					if (running) {
						if (doorOpen) {
							action = "purge";
							const ambientTemp = Number(ambient.value);
							const ambientHum = Number(ambientHumidity.value);
							temperature += Math.max(-.15, Math.min(.15, (ambientTemp - temperature) * .03)) * elapsed;
							humidity += Math.max(-.5, Math.min(.5, (ambientHum - humidity) * .03)) * elapsed;
							message = "Extrayendo aire; las partículas grises muestran el flujo hacia el exterior.";
						} else {
							let requestedAction = "Automático";
							if (modeSelect.value === "Manual") requestedAction = manualAction.value;
							else if (temperature < Number(target.value) - .3) requestedAction = "Calentar";
							else if (temperature > Number(target.value) + .3) requestedAction = "Enfriar";

							if (requestedAction === "Calentar" && temperature < 50) {
								action = "heating";
								temperature = Math.min(50, temperature + .24 * elapsed);
								humidity = Math.max(20, humidity - .03 * elapsed);
								message = "Calentando: el foco está activo y el aire caliente circula.";
							} else if (requestedAction === "Enfriar" && temperature > 10) {
								action = "cooling";
								temperature = Math.max(10, temperature - .28 * elapsed);
								humidity = Math.min(90, humidity + .03 * elapsed);
								message = "Enfriando: el módulo Peltier está activo y el aire frío circula.";
							}
						}
					}

					setModeClass(action);
					svg.classList.toggle("doors-open", doorOpen);
					room.setAttribute("fill", temperatureColor(temperature));
					tempValue.textContent = `${temperature.toFixed(1)} °C`;
					humidityValue.textContent = `${Math.round(humidity)}%`;
					status.textContent = message;
					requestAnimationFrame(updateFrame);
				}

				target.addEventListener("input", updateSliderLabels);
				ambient.addEventListener("input", updateSliderLabels);
				ambientHumidity.addEventListener("input", updateSliderLabels);
				modeSelect.addEventListener("change", () => {
					manualControl.hidden = modeSelect.value !== "Manual";
				});
				startButton.addEventListener("click", () => {
					running = !running;
					startButton.textContent = running ? "Detener" : "Iniciar";
					startButton.setAttribute("aria-pressed", String(running));
				});
				doorButton.addEventListener("click", () => {
					doorOpen = !doorOpen;
					doorButton.textContent = doorOpen ? "Cerrar puertas" : "Abrir puertas";
					doorButton.classList.toggle("secondary", doorOpen);
					doorButton.setAttribute("aria-pressed", String(doorOpen));
				});
				updateSliderLabels();
				requestAnimationFrame(updateFrame);
			</script>
		</body>
		</html>
		""",
		height=680,
		scrolling=True,
	)
