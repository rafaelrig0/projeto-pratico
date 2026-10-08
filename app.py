import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Análise da Produção Agrícola no Brasil",
    layout="wide"
)

ROOT = Path(__file__).parent
LOC_DADOS = ROOT / "dados" / "simulacao_producao_agricola_brasil.csv"
LOC_DB = ROOT / "database" / "prod_agricula.db"

@st.cache_data
def carregar_dados() -> pd.DataFrame:
    return pd.read_csv(
        LOC_DADOS,
        encoding="utf-8"
    )
df = carregar_dados()

def carregar_banco() -> None:
    LOC_DB.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(LOC_DB) as conn:
        df.to_sql(
            "prod_agricola",
            conn,
            if_exists="replace",
            index=False
        )
carregar_banco()


st.title("Análise da Produção Agrícola no Brasil")
st.markdown(
    """
    Dashboard desenvolvido para analisar padrões da produção agrícola
    brasileira entre 2015 e 2024, considerando produção, produtividade,
    área plantada, regiões, culturas, condições climáticas, valor econômico
    e exportações.
    """
)

st.divider()

with st.sidebar:
    st.header("Filtros")

    ano = st.multiselect(
        "Ano",
        sorted(df["ano"].unique())
    )

    df_selecao = (
        df[df["ano"].isin(ano)]
        if ano
        else df.copy()
    )

    mes = st.multiselect(
        "Mês",
        sorted(df_selecao["mes"].unique())
    )

    if mes:
        df_selecao = df_selecao[
            df_selecao["mes"].isin(mes)
        ]

    regiao = st.selectbox(
        "Região",
        ["Todas"] + sorted(df_selecao["regiao"].unique())
    )

    if regiao != "Todas":
        df_selecao = df_selecao[
            df_selecao["regiao"] == regiao
        ]

    uf = st.multiselect(
        "Estado",
        sorted(df_selecao["uf"].unique())
    )

    if uf:
        df_selecao = df_selecao[
            df_selecao["uf"].isin(uf)
        ]

    cultura = st.multiselect(
        "Cultura",
        sorted(df_selecao["cultura"].unique())
    )

    if cultura:
        df_selecao = df_selecao[
            df_selecao["cultura"].isin(cultura)
        ]

    nivel_produtividade = st.multiselect(
        "Nível de Produtividade",
        sorted(df_selecao["nivel_produtividade"].unique())
    )

    if nivel_produtividade:
        df_selecao = df_selecao[
            df_selecao["nivel_produtividade"].isin(
                nivel_produtividade
            )
        ]


filtrado = df_selecao

if filtrado.empty:
    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )
    st.stop()

producao_total = filtrado["producao_toneladas"].sum()
area_total = filtrado["area_plantada_ha"].sum()
valor_total = filtrado["valor_producao"].sum()
produtividade_media = filtrado["produtividade"].mean()
exportacoes_total = filtrado["exportacoes"].sum()
chuva_media = filtrado["chuva_mm"].mean()
temperatura_media = filtrado["temperatura_media"].mean()

prod_cultura = (
    filtrado
    .groupby("cultura")["producao_toneladas"]
    .sum()
    .sort_values(ascending=False)
)
cultura_top = prod_cultura.index[0]


prod_uf = (
    filtrado
    .groupby("uf")
    .agg(
        producao=("producao_toneladas", "sum"),
        produtividade=("produtividade", "mean"),
        area=("area_plantada_ha", "sum"),
        valor=("valor_producao", "sum"),
        exportacoes=("exportacoes", "sum")
    )
    .sort_values(
        "produtividade",
        ascending=False
    )
)
uf_top = prod_uf.index[0]

st.subheader("Indicadores-chave de desempenho")
k1, k2, k3 = st.columns(3)
k1.metric("Produção total", f"{producao_total:,.0f} t")
k2.metric("Cultura mais produzida", cultura_top)
k3.metric("Estado mais produtivo", uf_top)

k4, k5, k6 = st.columns(3)
k4.metric("Área plantada total", f"{area_total:,.0f} ha")
k5.metric("Valor econômico total", f"R$ {valor_total:,.0f}")
k6.metric("Média de produtividade", f"{produtividade_media:.2f} t/ha")


st.write("")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Visão Geral", "Evolução Temporal", "Análise Regional", "Clima e Exportações", "Dados e Metodologia"])

with tab1:
    st.subheader("Visão Geral da Produção")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "**Ranking de culturas por produção**"
        )

        d = (
            prod_cultura
            .reset_index()
            .sort_values("producao_toneladas")
        )

        fig = px.bar(
            d,
            x="producao_toneladas",
            y="cultura",
            orientation="h",
            labels={
                "producao_toneladas": "Produção (t)",
                "cultura": ""
            }
        )

        fig.update_layout(
            margin=dict(t=10, b=10)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:
        st.markdown(
            "**Valor econômico por cultura**"
        )

        d = (
            filtrado
            .groupby("cultura")["valor_producao"]
            .sum()
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            d,
            x="valor_producao",
            y="cultura",
            orientation="h",
            labels={
                "valor_producao": "Valor (R$)",
                "cultura": ""
            }
        )

        fig.update_layout(
            margin=dict(t=10, b=10)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    c3, c4 = st.columns(2)

    with c3:
        st.markdown(
            "**Produtividade média por cultura**"
        )

        d = (
            filtrado
            .groupby("cultura")["produtividade"]
            .mean()
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            d,
            x="produtividade",
            y="cultura",
            orientation="h",
            labels={
                "produtividade": "Produtividade média (t/ha)",
                "cultura": ""
            }
        )

        fig.update_layout(
            margin=dict(t=10, b=10)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c4:
        st.markdown(
            "**Distribuição por nível de produtividade**"
        )

        d = (
            filtrado["nivel_produtividade"]
            .value_counts()
            .reset_index()
        )

        d.columns = [
            "nivel",
            "registros"
        ]

        fig = px.pie(
            d,
            names="nivel",
            values="registros",
            hole=0.45
        )

        fig.update_layout(
            margin=dict(t=10, b=10)
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.divider()

    st.subheader("Interpretação dos resultados")
    st.write(
        f"No período e nos filtros selecionados, a cultura "
        f"com maior volume de produção é **{cultura_top}**, "
        f"enquanto **{uf_top}** apresenta a maior produtividade "
        f"média entre os estados analisados."
    )

    st.write(
        f"A produção acumulada é de aproximadamente "
        f"**{producao_total:,.0f} toneladas**, distribuída entre "
        f"{filtrado['cultura'].nunique()} culturas e "
        f"{filtrado['uf'].nunique()} estados."
    )

    st.write(
        f"A produtividade média observada é de "
        f"**{produtividade_media:.2f} t/ha**, enquanto a área "
        f"plantada total corresponde a aproximadamente "
        f"**{area_total:,.0f} hectares**."
    )

with tab2:
    st.subheader("Evolução Temporal da Produção")
    st.markdown(
        "**Produção total por ano**"
    )

    d = (
        filtrado
        .groupby("ano")["producao_toneladas"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        d,
        x="ano",
        y="producao_toneladas",
        markers=True,
        labels={
            "producao_toneladas": "Produção (t)",
            "ano": "Ano"
        }
    )

    fig.update_xaxes(
        dtick=1
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "**Sazonalidade: produção por mês**"
        )

        d = (
            filtrado
            .groupby("mes")["producao_toneladas"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            d,
            x="mes",
            y="producao_toneladas",
            labels={
                "producao_toneladas": "Produção (t)",
                "mes": "Mês"
            }
        )

        fig.update_xaxes(
            dtick=1
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    with c2:
        st.markdown(
            "**Valor econômico por ano**"
        )

        d = (
            filtrado
            .groupby("ano")
            .agg(
                valor=("valor_producao", "sum"),
                produtividade=("produtividade", "mean")
            )
            .reset_index()
        )

        fig = px.bar(
            d,
            x="ano",
            y="valor",
            labels={
                "valor": "Valor (R$)",
                "ano": "Ano"
            }
        )

        fig.update_xaxes(
            dtick=1
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        st.caption(
            "Produtividade média por ano: "
            + " | ".join(
                f"{int(a)}: {p:.1f} t/ha"
                for a, p in zip(
                    d["ano"],
                    d["produtividade"]
                )
            )
        )

    st.markdown(
        "**Produção anual por cultura**"
    )

    d = (
        filtrado
        .groupby(
            ["ano", "cultura"]
        )["producao_toneladas"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        d,
        x="ano",
        y="producao_toneladas",
        color="cultura",
        markers=True,
        labels={
            "producao_toneladas": "Produção (t)",
            "ano": "Ano",
            "cultura": "Cultura"
        }
    )

    fig.update_xaxes(
        dtick=1
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    st.subheader(
        "Heatmap sazonal da produção"
    )

    d = filtrado.pivot_table(
        index="mes",
        columns="ano",
        values="producao_toneladas",
        aggfunc="sum",
        fill_value=0
    )

    fig = px.imshow(
        d,
        aspect="auto",
        color_continuous_scale="Greens",
        labels={
            "color": "Produção (t)",
            "x": "Ano",
            "y": "Mês"
        }
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Interpretação")

    st.write(
        "A evolução temporal permite observar como a produção agrícola "
        "se comporta ao longo dos anos e identificar períodos de maior "
        "ou menor produção. O heatmap também permite visualizar a "
        "sazonalidade, destacando os meses que concentram os maiores "
        "volumes de produção."
    )

with tab3:
    st.subheader(
        "Análise Regional"
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            "**Produtividade média por estado**"
        )

        d = (
            prod_uf
            .reset_index()
            .sort_values("produtividade")
        )

        fig = px.bar(
            d,
            x="produtividade",
            y="uf",
            orientation="h",
            labels={
                "produtividade":
                    "Produtividade média (t/ha)",
                "uf": "UF"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:
        st.markdown(
            "**Produção total por estado**"
        )

        d = (
            prod_uf
            .reset_index()
            .sort_values("producao")
        )

        fig = px.bar(
            d,
            x="producao",
            y="uf",
            orientation="h",
            labels={
                "producao": "Produção (t)",
                "uf": "UF"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    c3, c4 = st.columns(2)

    with c3:
        st.markdown(
            "**Participação das regiões na produção**"
        )

        d = (
            filtrado
            .groupby("regiao")["producao_toneladas"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            d,
            names="regiao",
            values="producao_toneladas",
            hole=0.45
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c4:
        st.markdown(
            "**Área plantada e valor por região**"
        )

        d = (
            filtrado
            .groupby("regiao")
            .agg(
                area=("area_plantada_ha", "sum"),
                valor=("valor_producao", "sum")
            )
            .reset_index()
        )

        fig = px.scatter(
            d,
            x="area",
            y="valor",
            size="valor",
            color="regiao",
            labels={
                "area": "Área plantada (ha)",
                "valor": "Valor (R$)",
                "regiao": "Região"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.divider()

    st.subheader(
        "Desempenho das regiões"
    )

    d = (
        filtrado
        .groupby("regiao")
        .agg(
            produção=("producao_toneladas", "sum"),
            área=("area_plantada_ha", "sum"),
            produtividade=("produtividade", "mean"),
            valor=("valor_producao", "sum"),
            exportações=("exportacoes", "sum")
        )
        .sort_values(
            "produtividade"
        )
        .reset_index()
    )

    st.dataframe(
        d.style.format({
            "produção": "{:,.0f}",
            "área": "{:,.0f}",
            "produtividade": "{:.2f}",
            "valor": "R$ {:,.0f}",
            "exportações": "{:,.0f}"
        }),
        width="stretch"
    )

    st.divider()

    st.subheader(
        "Produção por estado e cultura"
    )

    tabela_cultura = filtrado.pivot_table(
        index="uf",
        columns="cultura",
        values="producao_toneladas",
        aggfunc="sum",
        fill_value=0
    )

    st.markdown(
        "**Tabela dinâmica**"
    )

    st.dataframe(
        tabela_cultura.style.format("{:,.0f}"),
        width="stretch"
    )

    st.markdown(
        "**Heatmap: produção por estado e cultura**"
    )

    fig = px.imshow(
        tabela_cultura,
        aspect="auto",
        color_continuous_scale="Greens",
        labels={
            "color": "Produção (t)",
            "x": "Cultura",
            "y": "UF"
        }
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Interpretação")

    st.write(
        "A análise regional evidencia diferenças na produção e na "
        "produtividade entre os estados e regiões brasileiras. A "
        "distribuição da produção também permite identificar quais "
        "regiões possuem maior participação no setor agrícola e quais "
        "apresentam menor desempenho no período analisado."
    )

with tab4:
    st.subheader(
        "Clima, Produtividade e Exportações"
    )

    c1, c2 = st.columns(2)


    with c1:

        st.markdown(
            "**Chuva × produtividade**"
        )

        fig = px.scatter(
            filtrado,
            x="chuva_mm",
            y="produtividade",
            color="cultura",
            hover_data=[
                "ano",
                "mes",
                "uf"
            ],
            labels={
                "chuva_mm": "Chuva (mm)",
                "produtividade":
                    "Produtividade (t/ha)",
                "cultura": "Cultura"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:
        st.markdown(
            "**Temperatura × produtividade**"
        )

        fig = px.scatter(
            filtrado,
            x="temperatura_media",
            y="produtividade",
            color="cultura",
            hover_data=[
                "ano",
                "mes",
                "uf"
            ],
            labels={
                "temperatura_media":
                    "Temperatura média (°C)",
                "produtividade":
                    "Produtividade (t/ha)",
                "cultura": "Cultura"
            }
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.divider()

    st.subheader(
        "Indicadores climáticos"
    )

    cor_chuva = filtrado[
        "chuva_mm"
    ].corr(
        filtrado["produtividade"]
    )

    cor_temperatura = filtrado[
        "temperatura_media"
    ].corr(
        filtrado["produtividade"]
    )

    k1, k2, k3 = st.columns(3)

    k1.metric("Chuva média", f"{chuva_media:.2f} mm"
    )

    k2.metric("Temperatura média", f"{temperatura_media:.2f} °C"
    )

    k3.metric("Exportações totais", f"{exportacoes_total:,.0f}"
    )

    c1, c2 = st.columns(2)

    c1.metric("Correlação chuva × produtividade", f"{cor_chuva:.3f}"
    )

    c2.metric("Correlação temperatura × produtividade", f"{cor_temperatura:.3f}"
    )

    st.divider()

    st.subheader(
        "Evolução das exportações"
    )

    d = (
        filtrado
        .groupby("ano")["exportacoes"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        d,
        x="ano",
        y="exportacoes",
        markers=True,
        labels={
            "ano": "Ano",
            "exportacoes": "Exportações"
        }
    )

    fig.update_xaxes(
        dtick=1
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown(
        "**Exportações por cultura**"
    )

    d = (
        filtrado
        .groupby("cultura")["exportacoes"]
        .sum()
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        d,
        x="exportacoes",
        y="cultura",
        orientation="h",
        labels={
            "exportacoes": "Exportações",
            "cultura": "Cultura"
        }
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.subheader("Interpretação")

    st.write(
        "A análise climática permite observar a relação entre chuva, "
        "temperatura e produtividade agrícola. Já a evolução das "
        "exportações mostra como o desempenho das culturas se relaciona "
        "com sua participação econômica."
    )


with tab5:
    st.subheader(
        "Dados filtrados"
    )
    st.caption(
        f"{len(filtrado):,} de {len(df):,} registros"
    )
    st.dataframe(
        filtrado,
        width="stretch",
        hide_index=True
    )

    st.write(
        "O conjunto de dados contém informações sobre ano, mês, "
        "região, estado, cultura, área plantada, produção, "
        "produtividade, chuva, temperatura, valor econômico, "
        "exportações e nível de produtividade."
    )

    st.divider()

    st.markdown(
        "### Indicadores utilizados"
    )

    st.markdown(
        """
        - **Produção total:** soma de `producao_toneladas`.
        - **Cultura mais produzida:** cultura com maior produção acumulada.
        - **Estado mais produtivo:** UF com maior produtividade média.
        - **Área plantada total:** soma de `area_plantada_ha`.
        - **Valor econômico total:** soma de `valor_producao`.
        - **Média de produtividade:** média simples de `produtividade`.
        - **Exportações totais:** soma de `exportacoes`.
        - **Correlação climática:** correlação de Pearson entre chuva,
          temperatura e produtividade.
        """
    )

    st.divider()

    st.subheader(
        "Conclusão Executiva"
    )

    st.write(
        f"A análise da produção agrícola no período selecionado "
        f"identifica **{cultura_top}** como a cultura com maior "
        f"volume produzido e **{uf_top}** como o estado com maior "
        f"produtividade média."
    )
    st.write(
        f"O conjunto analisado apresenta uma produção acumulada de "
        f"**{producao_total:,.0f} toneladas**, distribuída em uma "
        f"área total de aproximadamente **{area_total:,.0f} hectares**. "
        f"O valor econômico associado à produção é de aproximadamente "
        f"**R$ {valor_total:,.0f}**."
    )
    st.write(
        f"A produtividade média encontrada foi de "
        f"**{produtividade_media:.2f} t/ha**, enquanto as exportações "
        f"somaram aproximadamente **{exportacoes_total:,.0f}** no "
        f"recorte selecionado."
    )
    st.write(
        "A análise temporal permite identificar tendências e períodos "
        "de maior concentração da produção. A comparação regional "
        "evidencia diferenças entre estados e regiões, enquanto a "
        "análise por cultura permite identificar os principais "
        "produtos agrícolas do conjunto analisado."
    )
    st.write(
        "A análise climática permite investigar a relação entre "
        "chuva, temperatura e produtividade."
    )

    st.divider()

    st.info(
        """
        Os dados utilizados neste projeto são uma **simulação criada
        para fins educacionais**. Os resultados apresentados pelo
        dashboard não representam necessariamente a produção agrícola
        real do Brasil.
        """
    )