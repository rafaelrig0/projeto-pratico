import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import plotly
from pathlib import Path

ROOT = Path(__file__).parent
LOC_DADOS = ROOT / "dados" / "simulacao_producao_agricola_brasil.csv"
LOC_DB = ROOT / "database" / "prod_agricula.db"

st.set_page_config(page_title='Análise da produção agrícola', layout='wide')
st.title('Análise da produção agrícola no Brasil')
st.markdown('Análise de dados para investigar padrões de produção agrícola no Brasil. ', width="content")

st.divider()

st.subheader("KPI - Indicador-Chave de Desempenho")

@st.cache_data
def carregar_dados() -> pd.DataFrame:
    df = pd.read_csv(LOC_DADOS, encoding="utf-8")
    return df
df = carregar_dados()

def carregar_banco() -> None:
    LOC_DB.parent.mkdir(exist_ok=True)
    with sqlite3.connect(LOC_DB) as conn:
        df.to_sql("prod_agricola", conn, if_exists="replace", index=False)



with st.sidebar:
    st.header("Filtro")
    ano = st.multiselect("Ano", sorted(df["ano"].unique()))
    df_selecao = df[df["ano"].isin(ano)] if ano else df

    mes = st.multiselect("Mês", sorted(df["mes"].unique()))
    if mes:
        df_selecao = df_selecao[df_selecao["mes"].isin(mes)]
    
    regiao = st.selectbox("Região", ["Todas"] + sorted(df_selecao["regiao"].unique()))
    if regiao != "Todas":
        df_selecao = df_selecao[df_selecao["regiao"] == regiao]

    uf = st.multiselect("Estado", sorted(df_selecao["uf"].unique()))
    if uf:
        df_selecao = df_selecao[df_selecao["uf"].isin(uf)]
                        
    cultura = st.multiselect("Cultura", sorted(df_selecao["cultura"].unique()))
    if cultura:
        df_selecao = df_selecao[df_selecao["cultura"].isin(cultura)]

    nivel_produtividade = st.multiselect("Nível de Produtividade", sorted(df_selecao["nivel_produtividade"].unique()))
    if nivel_produtividade:
        df_selecao = df_selecao[df_selecao["nivel_produtividade"].isin(nivel_produtividade)]


filtrado = df_selecao
if filtrado.empty:
    st.warning("Nenhum registro encontrado!")
    st.stop()

# tab1, tab2, tab3, tab4, tab5 = st.tabs(["Visão geral", "Tempo", "Geografia", "Dados e método"])

