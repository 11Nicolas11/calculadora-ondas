import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CONFIGURACIÓN PREMIUM
st.set_page_config(page_title="Simulador de Ondas", layout="wide")

st.title("Análisis de Fenómenos Ondulatorios")
st.markdown("---")

# 2. PANEL LATERAL PROFESIONAL
st.sidebar.header("Parámetros de Simulación")

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

# 3. CÁLCULOS FÍSICOS RIGUROSOS Y GENERACIÓN DE TIMELAPSE
k1 = (2 * np.pi) / lam1
omega1 = 2 * np.pi * f1
signo1 = -1 if "+x" in dir1 else 1

k2 = (2 * np.pi) / lam2
omega2 = 2 * np.pi * f2
signo2 = -1 if "+x" in dir2 else 1

x_1d = np.linspace(0, 20, 400) 
x_2d = np.linspace(-10, 10, 60)  # Un poco más de resolución para capturar el frente de la gota
y_2d = np.linspace(-10, 10, 60)
X, Y = np.meshgrid(x_2d, y_2d)

# Posición de los dos focos de perturbación (donde caen las gotas)
foco1_x, foco1_y = -3, 0
foco2_x, foco2_y = 3, 0
R1 = np.sqrt((X - foco1_x)**2 + (Y - foco1_y)**2)
R2 = np.sqrt((X - foco2_x)**2 + (Y - foco2_y)**2)

# Velocidades de fase individuales de la onda (v = lambda * f)
v1 = lam1 * f1
v2 = lam2 * f2

# Extendemos el tiempo a un rango mayor para ver la propagación completa desde el centro
tiempos = np.linspace(0, 3.0, 30)

# 4. PESTAÑAS SEPARADAS
tab1, tab2, tab3, tab4 = st.tabs([
    "Guía de Uso",
    "Análisis Individual (1D)", 
    "Interferencia y Superposición", 
    "💧 Simulación 2D (Cubeta 3D)"
])

with tab1:
    st.header("Guía de Uso del Simulador")
    st.markdown("""
    Esta pestaña ayuda a comprender el uso de la herramienta. Las siguientes pestañas contienen la animación interactiva fluida.
     
    ### ¿Cómo usar los controles de movimiento?
    * Al abrir cualquier pestaña de análisis, aparecerá un botón de **"▶️ Play"** o **"▶️ Iniciar Animación"** en la gráfica.
    * Presione el botón para iniciar el movimiento armónico continuo de las ondas en el navegador.
    * Al modificar cualquier parámetro en la barra lateral, la animación se recalculará instantáneamente.
    """)

with tab2:
    st.subheader("Propiedades Físicas de la Onda 1")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Número de onda (k)", f"{k1:.2f} rad/m")
    col2.metric("Frec. angular (ω)", f"{omega1:.2f} rad/s")
    col3.metric("Velocidad de propagación (v)", f"{v1:.2f} m/s")
    col4.metric("Período (T)", f"{(1/f1):.2f} s")
    
    st.latex(rf"y_1(x,t) = {A1:.2f} \sin({k1:.2f}x {'-' if signo1 == -1 else '+'} {omega1:.2f}t + {fase1:.2f})")
    
    fig1 = go.Figure(
        data=[go.Scatter(x=x_1d, y=A1 * np.sin(k1 * x_1d + signo1 * omega1 * tiempos[0] + fase1), mode='lines', name='Onda 1', line=dict(color='#00F0FF', width=3), fill='tozeroy', fillcolor='rgba(0, 240, 255, 0.1)')],
        layout=go.Layout(
            xaxis_title="Posición x (m)", yaxis_title="Desplazamiento y (m)",
            yaxis=dict(range=[-(A1 + 0.5), (A1 + 0.5)], zeroline=True), template="plotly_dark",
            updatemenus=[dict(type="buttons", showactive=False, buttons=[dict(label="▶️ Play", method="animate", args=[None, {"frame": {"duration": 40, "redraw": True}, "fromcurrent": True}])])]
        ),
        frames=[go.Frame(data=[go.Scatter(x=x_1d, y=A1 * np.sin(k1 * x_1d + signo1 * omega1 * t + fase1))]) for t in tiempos]
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab3:
    st.subheader("Principio de Superposición 1D")
    st.latex(r"y_{res}(x,t) = y_1(x,t) + y_2(x,t)")
    
    frames_superposicion = []
    for t in tiempos:
        y1_t = A1 * np.sin(k1 * x_1d + signo1 * omega1 * t + fase1)
        y2_t = A2 * np.sin(k2 * x_1d + signo2 * omega2 * t + fase2)
        frames_superposicion.append(go.Frame(data=[
            go.Scatter(x=x_1d, y=y1_t),
            go.Scatter(x=x_1d, y=y2_t),
            go.Scatter(x=x_1d, y=y1_t + y2_t)
        ]))

    max_amp = A1 + A2
    fig2 = go.Figure(
        data=[
            go.Scatter(x=x_1d, y=A1 * np.sin(k1 * x_1d + signo1 * omega1 * tiempos[0] + fase1), mode='lines', name='Onda 1', line=dict(color='#00F0FF', width=1, dash='dot')),
            go.Scatter(x=x_1d, y=A2 * np.sin(k2 * x_1d + signo2 * omega2 * tiempos[0] + fase2), mode='lines', name='Onda 2', line=dict(color='#FF0055', width=1, dash='dot')),
            go.Scatter(x=x_1d, y=A1 * np.sin(k1 * x_1d + signo1 * omega1 * tiempos[0] + fase1) + A2 * np.sin(k2 * x_1d + signo2 * omega2 * tiempos[0] + fase2), mode='lines', name='Onda Resultante', line=dict(color='#00FF66', width=4), fill='tozeroy', fillcolor='rgba(0, 255, 102, 0.1)')
        ],
        layout=go.Layout(
            xaxis_title="Posición x (m)", yaxis_title="Desplazamiento y (m)",
            yaxis=dict(range=[-(max_amp + 0.5), (max_amp + 0.5)], zeroline=True), template="plotly_dark",
            updatemenus=[dict(type="buttons", showactive=False, buttons=[dict(label="▶️ Play", method="animate", args=[None, {"frame": {"duration": 40, "redraw": True}, "fromcurrent": True}])])]
        ),
        frames=frames_superposicion
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.subheader("Simulación Física de Cubeta de Ondas (Impacto Dinámico)")
    st.markdown("Simula la caída de gotas de agua sobre una superficie líquida inicialmente en reposo absoluto.")

    # Inicializamos el estado del botón en Streamlit para congelar la cubeta en calma si no se pulsa
    if "impacto_activo" not in st.session_state:
        st.session_state.impacto_activo = False

    # Botón de acción para liberar la gota
    if st.button("💧 Dejar caer gota (Iniciar Impacto)", type="primary"):
        st.session_state.impacto_activo = True

    # Superficie en calma total por defecto (Z = 0)
    Z_calma = np.zeros_like(X)
    max_z = A1 + A2

    if st.session_state.impacto_activo:
        frames_3d = []
        for t in tiempos:
            # Física real de fluidos: Las ondas solo existen donde el frente temporal (v*t) ya ha alcanzado el radio R
            # Además se incluye un factor de amortiguamiento (1 / (1 + 0.1*R)) para simular la pérdida de energía del agua
            mask1 = np.where(v1 * t >= R1, 1.0, 0.0)
            mask2 = np.where(v2 * t >= R2, 1.0, 0.0)
            
            Z1_t = A1 * np.sin(k1 * R1 - omega1 * t + fase1) * mask1 / (1.0 + 0.1 * R1)
            Z2_t = A2 * np.sin(k2 * R2 - omega2 * t + fase2) * mask2 / (1.0 + 0.1 * R2)
            
            frames_3d.append(go.Frame(data=[go.Surface(z=Z1_t + Z2_t)]))
            
        # El fotograma 0 arranca con la superficie plana (la gota tocando el centro)
        fig3 = go.Figure(
            data=[go.Surface(z=Z_calma, x=X, y=Y, colorscale='Blues', opacity=0.95, cmin=-max_z, cmax=max_z)],
            layout=go.Layout(
                template="plotly_dark",
                scene=dict(
                    xaxis=dict(title="Eje X (m)"),
                    yaxis=dict(title="Eje Y (m)"),
                    zaxis=dict(title="Amplitud Z (m)", range=[-(max_z + 0.2), (max_z + 0.2)])
                ),
                margin=dict(l=0, r=0, b=0, t=10),
                updatemenus=[dict(
                    type="buttons",
                    showactive=False,
                    y=0.1, x=0.05,
                    buttons=[dict(label="▶️ Ver Expansión de Onda (Play)", method="animate", args=[None, {"frame": {"duration": 60, "redraw": True}, "fromcurrent": False}])])
                ]
            ),
            frames=frames_3d
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.success("¡Impacto generado con éxito! Haz clic en el botón '▶️ Ver Expansión de Onda (Play)' que apareció abajo a la izquierda de la gráfica para ver cómo se propaga el agua.")
    else:
        # Gráfica fija que muestra el agua plana antes del impacto
        fig3 = go.Figure(
            data=[go.Surface(z=Z_calma, x=X, y=Y, colorscale='Blues', opacity=0.8, cmin=-max_z, cmax=max_z)],
            layout=go.Layout(
                template="plotly_dark",
                scene=dict(
                    xaxis=dict(title="Eje X (m)"),
                    yaxis=dict(title="Eje Y (m)"),
                    zaxis=dict(title="Amplitud Z (m)", range=[-(max_z + 0.2), (max_z + 0.2)])
                ),
                margin=dict(l=0, r=0, b=0, t=10)
            )
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.info("El agua está en calma. Presiona el botón rojo de arriba para dejar caer la gota.")
