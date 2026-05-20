import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# 1. CONFIGURACIÓN PREMIUM
st.set_page_config(page_title="Simulador de Ondas", layout="wide")

st.title("Análisis de Fenómenos Ondulatorios")
st.markdown("---")

# 2. PANEL LATERAL PROFESIONAL
st.sidebar.header("Parámetros de Simulación")

# --- NUEVA SECCIÓN DE ANIMACIÓN ---
st.sidebar.subheader("Controles de Animación")
animar = st.sidebar.toggle("▶️ Iniciar Movimiento", value=False)
velocidad_animacion = st.sidebar.slider("Velocidad", 0.01, 0.1, 0.03, step=0.01)

# El tiempo base que el usuario puede setear manualmente
t_manual = st.sidebar.number_input("Tiempo base (t) [s]", value=0.0, step=0.1, format="%.2f")

# Gestión del tiempo dinámico para la animación
if animar:
    if "tiempo_dinamico" not in st.session_state:
        st.session_state.tiempo_dinamico = t_manual
    else:
        st.session_state.tiempo_dinamico += velocidad_animacion
    t = st.session_state.tiempo_dinamico
else:
    # Si se apaga la animación, vuelve al control manual o se congela en el punto actual
    if "tiempo_dinamico" in st.session_state:
        del st.session_state.tiempo_dinamico
    t = t_manual
# ----------------------------------

with st.sidebar.expander("Parámetros: Onda 1", expanded=True):
    A1 = st.number_input("Amplitud (A1) [m]", value=1.0, step=0.1, format="%.2f")
    f1 = st.number_input("Frecuencia (f1) [Hz]", min_value=0.01, value=1.0, step=0.1, format="%.2f")
    lam1 = st.number_input("Long. de Onda (λ1) [m]", min_value=0.01, value=5.0, step=0.1, format="%.2f")
    fase1 = st.number_input("Fase (ϕ1) [rad]", value=0.0, step=0.1, format="%.2f")
    dir1 = st.selectbox("Dirección Onda 1", ["+x (Hacia la derecha)", "-x (Hacia la izquierda)"])

with st.sidebar.expander("Parámetros: Onda 2", expanded=False):
    A2 = st.number_input("Amplitud (A2) [m]", value=1.0, step=0.1, format="%.2f")
    f2 = st.number_input("Frecuencia (f2) [Hz]", min_value=0.01, value=1.0, step=0.1, format="%.2f")
    lam2 = st.number_input("Long. de Onda (λ2) [m]", min_value=0.01, value=5.0, step=0.1, format="%.2f")
    fase2 = st.number_input("Fase (ϕ2) [rad]", value=3.14, step=0.1, format="%.2f")
    dir2 = st.selectbox("Dirección Onda 2", ["-x (Hacia la izquierda)", "+x (Hacia la derecha)"])

# 3. CÁLCULOS FÍSICOS RIGUROSOS
k1 = (2 * np.pi) / lam1
omega1 = 2 * np.pi * f1
signo1 = -1 if "+x" in dir1 else 1

k2 = (2 * np.pi) / lam2
omega2 = 2 * np.pi * f2
signo2 = -1 if "+x" in dir2 else 1

x_1d = np.linspace(0, 20, 1000) 
y1 = A1 * np.sin(k1 * x_1d + signo1 * omega1 * t + fase1)
y2 = A2 * np.sin(k2 * x_1d + signo2 * omega2 * t + fase2)
y_res = y1 + y2

# 4. PESTAÑAS SEPARADAS (Guía vs. Análisis Técnico)
tab1, tab2, tab3, tab4 = st.tabs([
    "Guía de Uso",
    "Análisis Individual (1D)", 
    "Interferencia y Superposición", 
    "💧 Simulación 2D (Cubeta 3D)"
])

with tab1:
    st.header("Guía de Uso del Simulador")
    st.markdown("""
    Esta pestaña está diseñada para ayudar a comprender el uso de la herramienta. Las siguientes pestañas contienen el análisis matemático formal.
    
    ### ¿Cómo interactuar con el simulador?
    Utilice el panel lateral izquierdo para ingresar las variables de estado.
    * **Iniciar Movimiento:** Activa el avance cronológico automático para ver las ondas propagarse.
    * **Tiempo (t):** Modifica manualmente o visualiza el avance del tiempo en segundos.
    * **Amplitud (A):** Modifica el desplazamiento máximo desde el punto de equilibrio.
    * **Frecuencia (f):** Cambia el número de ciclos que ocurren en un segundo.
    * **Longitud de onda (λ):** Ajusta la distancia espacial entre dos crestas consecutivas en el medio.
    * **Dirección:** Define si la perturbación viaja hacia la parte positiva ($+x$) o negativa ($-x$) del eje.
    """)

with tab2:
    st.subheader("Propiedades Físicas de la Onda 1")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Número de onda (k)", f"{k1:.2f} rad/m")
    col2.metric("Frec. angular (ω)", f"{omega1:.2f} rad/s")
    col3.metric("Velocidad de propagación (v)", f"{(lam1*f1):.2f} m/s")
    col4.metric("Período (T)", f"{(1/f1):.2f} s")
    
    st.latex(rf"y_1(x,t) = {A1:.2f} \sin({k1:.2f}x {'-' if signo1 == -1 else '+'} {omega1:.2f}t + {fase1:.2f})")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x_1d, y=y1, mode='lines', name='Onda 1', line=dict(color='#00F0FF', width=3), fill='tozeroy', fillcolor='rgba(0, 240, 255, 0.1)'))
    fig1.update_layout(xaxis_title="Posición x (m)", yaxis_title="Desplazamiento y (m)", yaxis=dict(range=[-10.5, 10.5], zeroline=True), template="plotly_dark", margin=dict(t=10, b=10))
    st.plotly_chart(fig1, use_container_width=True)

with tab3:
    st.subheader("Principio de Superposición 1D")
    st.latex(r"y_{res}(x,t) = y_1(x,t) + y_2(x,t)")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x_1d, y=y1, mode='lines', name='Onda 1', line=dict(color='#00F0FF', width=1, dash='dot')))
    fig2.add_trace(go.Scatter(x=x_1d, y=y2, mode='lines', name='Onda 2', line=dict(color='#FF0055', width=1, dash='dot')))
    fig2.add_trace(go.Scatter(x=x_1d, y=y_res, mode='lines', name='Onda Resultante', line=dict(color='#00FF66', width=4), fill='tozeroy', fillcolor='rgba(0, 255, 102, 0.1)'))
    
    fig2.update_layout(xaxis_title="Posición x (m)", yaxis_title="Desplazamiento y (m)", yaxis=dict(range=[-21, 21], zeroline=True), template="plotly_dark", margin=dict(t=10, b=10))
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.subheader("Interferencia Bidimensional (Frentes de Onda Circulares)")
    st.latex(r"z(x,y,t) = A_1 \sin(k_1 r_1 - \omega_1 t + \phi_1) + A_2 \sin(k_2 r_2 - \omega_2 t + \phi_2)")
    
    x_2d = np.linspace(-10, 10, 80)
    y_2d = np.linspace(-10, 10, 80)
    X, Y = np.meshgrid(x_2d, y_2d)
    
    foco1_x, foco1_y = -3, 0
    foco2_x, foco2_y = 3, 0
    
    R1 = np.sqrt((X - foco1_x)**2 + (Y - foco1_y)**2)
    R2 = np.sqrt((X - foco2_x)**2 + (Y - foco2_y)**2)
    
    Z1 = A1 * np.sin(k1 * R1 - omega1 * t + fase1)
    Z2 = A2 * np.sin(k2 * R2 - omega2 * t + fase2)
    Z_res = Z1 + Z2
    
    fig3 = go.Figure(data=[go.Surface(z=Z_res, x=X, y=Y, colorscale='Blues', opacity=0.9)])
    fig3.update_layout(
        template="plotly_dark",
        scene=dict(xaxis_title="Eje X (m)", yaxis_title="Eje Y (m)", zaxis_title="Amplitud Z (m)", zaxis=dict(range=[-10, 10])),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- EJECUTAR EL RE-RENDERIZADO SI LA ANIMACIÓN ESTÁ ACTIVA ---
if animar:
    time.sleep(0.01)  # Pequeña pausa para no saturar la CPU
    st.rerun()
