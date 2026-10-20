"""Dashboard Streamlit. Rode: streamlit run app.py"""
import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Aderência à dieta", layout="wide")
st.title("🥗 Aderência à dieta (dados sintéticos)")

@st.cache_data
def consulta(sql: str) -> pd.DataFrame:
    with sqlite3.connect("dieta.db") as con:
        return pd.read_sql(sql, con)

total = consulta("SELECT COUNT(*) n, 100.0*AVG(dentro_da_dieta) pct FROM refeicoes").iloc[0]
dias = consulta("SELECT COUNT(*) n FROM (SELECT data FROM refeicoes GROUP BY data "
                "HAVING MIN(dentro_da_dieta)=1)").iloc[0, 0]
c1, c2, c3 = st.columns(3)
c1.metric("Refeições registradas", int(total.n))
c2.metric("Dentro da dieta", f"{total.pct:.1f}%")
c3.metric("Dias 100% na dieta", int(dias))

esq, dir_ = st.columns(2)
with esq:
    st.subheader("Por tipo de refeição")
    st.bar_chart(consulta("SELECT tipo_refeicao, 100.0*AVG(dentro_da_dieta) AS pct "
                          "FROM refeicoes GROUP BY tipo_refeicao"), x="tipo_refeicao", y="pct")
with dir_:
    st.subheader("Comer fora x em casa")
    st.bar_chart(consulta("SELECT CASE comeu_fora WHEN 1 THEN 'fora' ELSE 'casa' END AS local, "
                          "100.0*AVG(dentro_da_dieta) AS pct FROM refeicoes GROUP BY comeu_fora"),
                 x="local", y="pct")

st.subheader("Evolução semanal")
st.line_chart(consulta("SELECT strftime('%Y-%W', data) AS semana, 100.0*AVG(dentro_da_dieta) AS pct "
                       "FROM refeicoes GROUP BY semana"), x="semana", y="pct")
