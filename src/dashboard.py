"""Dashboard Streamlit que consome as views do PostgreSQL.

Uso:  streamlit run src/dashboard.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st

from config import get_engine

st.set_page_config(page_title="Dashboard IoT", layout="wide")
engine = get_engine()


@st.cache_data(ttl=60)
def load_data(view_name: str) -> pd.DataFrame:
    """Carrega todos os dados de uma view."""
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)


st.title("Dashboard de Temperaturas IoT")

# KPIs gerais
local = load_data("avg_temp_por_local")
diario = load_data("temp_max_min_por_dia")
c1, c2, c3 = st.columns(3)
c1.metric("Total de leituras", f"{int(local['total_leituras'].sum()):,}")
c2.metric("Maior temperatura", f"{diario['temp_max'].max()} °C")
c3.metric("Menor temperatura", f"{diario['temp_min'].min()} °C")

# Gráfico 1
st.header("Temperatura por local do sensor (dentro x fora)")
st.plotly_chart(
    px.bar(local, x="location", y="avg_temp", color="location", text="avg_temp",
           labels={"location": "Local", "avg_temp": "Temperatura média (°C)"}),
    use_container_width=True,
)

# Gráfico 2
st.header("Leituras por hora do dia")
horas = load_data("leituras_por_hora")
st.plotly_chart(
    px.line(horas, x="hora", y="contagem", markers=True,
            labels={"hora": "Hora", "contagem": "Nº de leituras"}),
    use_container_width=True,
)

# Gráfico 3
st.header("Temperaturas máximas e mínimas por dia")
st.plotly_chart(
    px.line(diario, x="data", y=["temp_max", "temp_min"],
            labels={"data": "Data", "value": "Temperatura (°C)", "variable": "Medida"}),
    use_container_width=True,
)
