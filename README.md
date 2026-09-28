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

| Práctica | Descripción | Tecnología | Estado |
| :--- | :--- | :--- | :---: |
| **01. Control de LED** | Lógica de botones y GPIOs con simulación en tiempo real. | ESP32 + Wokwi | ✅ Live |
| **02. Control de Relé** | Etapa de potencia y aislamiento para motores DC. | ESP32 + Relé | ✅ Live |
| **03. Gemelo Digital** | Simulador de transferencia de líquidos con lógica de normalización y conservación de masa. | Python (Streamlit) | ✅ Live |

---

##  Destacado Técnico: Práctica 03 (Gemelo Digital)

La práctica más compleja del portafolio es el **Simulador de Bombas**. Originalmente desarrollado en Tkinter para escritorio, fue migrado a una arquitectura web reactiva utilizando `st.session_state` para mantener la persistencia de datos.

**Características clave:**
- **Lógica de Normalización:** El sistema detecta si los tanques están fuera del rango operativo (20%-80%) y solicita al usuario una corrección antes de permitir la operación automática, previniendo desbordamientos simulados.
- **Conservación de Masa:** Algoritmo que garantiza que la suma de los volúmenes de los depósitos A y B siempre sea constante (1000ml).
- **Interfaz Reactiva:** Actualización de barras de progreso y estados en tiempo real sin recargar la página.

