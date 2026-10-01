# ⚙️ Portafolio Interactivo: Sistemas Embebidos

Bienvenido a mi repositorio de portafolio personal. Este proyecto es una **aplicación web interactiva** desarrollada en Python y Streamlit, diseñada para documentar, simular y visualizar proyectos de electrónica y sistemas embebidos.

 **Ver Aplicación en Vivo:** [coe-embedded-lab.streamlit.app](https://coe-embedded-lab.streamlit.app)

---

## 📋 Sobre el Proyecto

El objetivo de este portafolio es demostrar la capacidad de integrar hardware (ESP32, sensores, actuadores) con interfaces de software modernas. A diferencia de un repositorio tradicional de código, esta plataforma permite a cualquier usuario **interactuar con las simulaciones** directamente desde el navegador, sin necesidad de instalar software ni contar con el hardware físico.

### 🛠️ Tecnologías Utilizadas
- **Backend & Frontend:** Python 3.x, Streamlit.
- **Hardware Simulado:** ESP32 DevKit V1, Sensores Ultrasónicos, Módulos de Relé.
- **Simulación de Circuitos:** Wokwi (Integración vía iframe).
- **Control de Versiones:** Git & GitHub.

---

## 📂 Prácticas Destacadas

| Proyecto | Descripción | Tecnología | Estado |
| :--- | :--- | :--- | :---: |
| **Control de LED** | Lógica de botones y GPIOs con simulación en tiempo real. | ESP32 + Wokwi | ✅ Live |
| **Control de relé** | Etapa de potencia y aislamiento para motores DC. | ESP32 + Relé | ✅ Live |
| **Simulador de bombas** | Transferencia de líquidos con lógica de normalización y conservación de masa. | Python (Streamlit) | ✅ Live |
| **Simulador de caja térmica** | Control virtual de temperatura con foco, módulo Peltier, ventiladores y puertas. | Python (Streamlit) | ✅ Live |

---

## Simulador de bombas (Gemelo Digital)

El **Simulador de Bombas** utiliza una arquitectura web reactiva con `st.session_state` para mantener el estado de los depósitos durante la simulación.

**Características clave:**
- **Lógica de Normalización:** El sistema detecta si los tanques están fuera del rango operativo (20%-80%) y solicita al usuario una corrección antes de permitir la operación automática, previniendo desbordamientos simulados.
- **Conservación de Masa:** Algoritmo que garantiza que la suma de los volúmenes de los depósitos A y B siempre sea constante (1000ml).
- **Interfaz Reactiva:** Actualización de barras de progreso y estados en tiempo real sin recargar la página.

## Simulador de caja térmica

La caja térmica recrea en el navegador el comportamiento del programa de escritorio, sin necesitar Qt, un ESP32 ni conexión serial. Permite ajustar la temperatura objetivo y las condiciones ambientales, operar en modo automático o manual, abrir la puerta para simular ventilación y observar los actuadores y las lecturas virtuales.
