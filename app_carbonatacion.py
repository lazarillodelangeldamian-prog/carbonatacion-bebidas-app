
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIGURACIÓN DE LA APP
# =========================

st.set_page_config(
    page_title="Estimación de Costos y Ciclo de Vida - Carbonatación",
    page_icon="🥤",
    layout="wide"
)

st.title("🥤 Plataforma para estimación de costos y ciclo de vida")
st.subheader("Proceso de carbonatación de bebidas")

st.write("""
Esta plataforma permite estimar los costos principales del proceso de carbonatación
de bebidas, así como indicadores básicos de ciclo de vida relacionados con el consumo
de energía y las emisiones indirectas de CO₂.
""")

# =========================
# BARRA LATERAL
# =========================

st.sidebar.header("Datos de entrada")

st.sidebar.subheader("Producción")

volumen_lote = st.sidebar.number_input(
    "Volumen del lote producido (L)",
    min_value=1.0,
    value=100.0,
    step=10.0
)

num_botellas = st.sidebar.number_input(
    "Número de botellas producidas",
    min_value=1,
    value=200,
    step=10
)

st.sidebar.subheader("Materia prima")

precio_agua = st.sidebar.number_input(
    "Precio del agua ($/L)",
    min_value=0.0,
    value=0.02,
    step=0.01
)

precio_jarabe = st.sidebar.number_input(
    "Precio del jarabe o concentrado ($/L)",
    min_value=0.0,
    value=25.0,
    step=1.0
)

fraccion_jarabe = st.sidebar.slider(
    "Porcentaje de jarabe en la bebida (%)",
    min_value=0.0,
    max_value=50.0,
    value=12.0,
    step=1.0
)

st.sidebar.subheader("Carbonatación")

consumo_co2 = st.sidebar.number_input(
    "Consumo de CO₂ (kg CO₂/L bebida)",
    min_value=0.0,
    value=0.007,
    step=0.001,
    format="%.4f"
)

precio_co2 = st.sidebar.number_input(
    "Precio del CO₂ ($/kg)",
    min_value=0.0,
    value=35.0,
    step=1.0
)

st.sidebar.subheader("Energía")

potencia_equipo = st.sidebar.number_input(
    "Potencia del equipo de carbonatación (kW)",
    min_value=0.0,
    value=1.5,
    step=0.5
)

tiempo_operacion = st.sidebar.number_input(
    "Tiempo de operación (h)",
    min_value=0.0,
    value=2.0,
    step=0.5
)

precio_electricidad = st.sidebar.number_input(
    "Precio de electricidad ($/kWh)",
    min_value=0.0,
    value=3.0,
    step=0.5
)

st.sidebar.subheader("Ciclo de vida")

factor_emision = st.sidebar.number_input(
    "Factor de emisión eléctrica (kg CO₂-eq/kWh)",
    min_value=0.0,
    value=0.45,
    step=0.05
)

# =========================
# CÁLCULOS
# =========================

volumen_jarabe = volumen_lote * (fraccion_jarabe / 100)
volumen_agua = volumen_lote - volumen_jarabe

co2_total = volumen_lote * consumo_co2
energia_total = potencia_equipo * tiempo_operacion

costo_agua = volumen_agua * precio_agua
costo_jarabe = volumen_jarabe * precio_jarabe
costo_co2 = co2_total * precio_co2
costo_energia = energia_total * precio_electricidad

costo_total = costo_agua + costo_jarabe + costo_co2 + costo_energia
costo_por_botella = costo_total / num_botellas

emisiones_energia = energia_total * factor_emision
emisiones_por_botella = emisiones_energia / num_botellas

# =========================
# RESULTADOS PRINCIPALES
# =========================

st.header("1. Resultados principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Costo total del lote", f"${costo_total:,.2f}")

with col2:
    st.metric("Costo por botella", f"${costo_por_botella:,.2f}")

with col3:
    st.metric("CO₂ consumido", f"{co2_total:.3f} kg")

with col4:
    st.metric("Energía consumida", f"{energia_total:.2f} kWh")

# =========================
# BALANCE DE INSUMOS
# =========================

st.header("2. Balance de insumos")

datos_insumos = {
    "Concepto": [
        "Agua",
        "Jarabe o concentrado",
        "CO₂",
        "Energía eléctrica"
    ],
    "Cantidad": [
        volumen_agua,
        volumen_jarabe,
        co2_total,
        energia_total
    ],
    "Unidad": [
        "L",
        "L",
        "kg",
        "kWh"
    ],
    "Costo ($)": [
        costo_agua,
        costo_jarabe,
        costo_co2,
        costo_energia
    ]
}

df_insumos = pd.DataFrame(datos_insumos)
st.dataframe(df_insumos, use_container_width=True)

# =========================
# GRÁFICA DE COSTOS
# =========================

st.header("3. Distribución de costos")

costos = {
    "Agua": costo_agua,
    "Jarabe": costo_jarabe,
    "CO₂": costo_co2,
    "Energía": costo_energia
}

fig, ax = plt.subplots()
ax.bar(costos.keys(), costos.values())
ax.set_ylabel("Costo ($)")
ax.set_title("Distribución de costos del proceso")
st.pyplot(fig)

# =========================
# CICLO DE VIDA
# =========================

st.header("4. Indicadores básicos de ciclo de vida")

col5, col6 = st.columns(2)

with col5:
    st.metric("Emisiones por energía", f"{emisiones_energia:.3f} kg CO₂-eq")

with col6:
    st.metric("Emisiones por botella", f"{emisiones_por_botella:.5f} kg CO₂-eq/botella")

st.write("""
El análisis de ciclo de vida considerado en esta plataforma es simplificado.
Se enfoca únicamente en el consumo energético del proceso de carbonatación.
Para un análisis más completo se podrían incluir fabricación de envases,
transporte, refrigeración, limpieza del equipo, tratamiento de agua y disposición final.
""")

# =========================
# INTERPRETACIÓN AUTOMÁTICA
# =========================

st.header("5. Interpretación de resultados")

if costo_jarabe > costo_co2 and costo_jarabe > costo_energia:
    st.success("El mayor costo del proceso proviene del jarabe o concentrado.")
elif costo_co2 > costo_jarabe and costo_co2 > costo_energia:
    st.warning("El mayor costo del proceso proviene del CO₂ utilizado en la carbonatación.")
elif costo_energia > costo_jarabe and costo_energia > costo_co2:
    st.warning("El mayor costo del proceso proviene del consumo energético.")
else:
    st.info("Los costos principales se encuentran relativamente equilibrados.")

st.write(f"""
Para un lote de **{volumen_lote:.1f} L**, se producen aproximadamente **{num_botellas} botellas**.
El costo total estimado es de **${costo_total:,.2f}**, con un costo unitario de
**${costo_por_botella:,.2f} por botella**.
""")

# =========================
# DESCARGA DE RESULTADOS
# =========================

st.header("6. Descargar resultados")

csv = df_insumos.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Descargar tabla de resultados en CSV",
    data=csv,
    file_name="resultados_carbonatacion.csv",
    mime="text/csv"
)

# =========================
# PIE DE PÁGINA
# =========================

st.markdown("---")
st.write("Desarrollado en Streamlit para el análisis técnico-económico del proceso de carbonatación de bebidas.")
