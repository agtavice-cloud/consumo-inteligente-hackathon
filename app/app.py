import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Consumo Inteligente",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("customer_features_cluster_ICI.csv")
    return df

df = carregar_dados()

def classificar_ici(ici):
    if ici >= 80:
        return "Excelente"
    elif ici >= 60:
        return "Bom"
    elif ici >= 40:
        return "Moderado"
    else:
        return "Crítico"

df["ICI_Classificacao"] = df["ICI"].apply(classificar_ici)

st.title("📊 Consumo Inteligente")
st.subheader("Sistema Inteligente de Análise de Perfil de Consumo e Geração de Insights")

st.markdown("""
Este aplicativo apresenta o **Índice de Consumo Inteligente (ICI)**, 
os perfis de consumo gerados por Machine Learning e recomendações automáticas 
para apoiar decisões de negócio.
""")

# KPIs principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Clientes", f"{df['CustomerID'].nunique():,.0f}")

with col2:
    st.metric("Receita Total", f"R$ {df['Monetary'].sum()/1000000:,.2f} Mi")

with col3:
    st.metric("ICI Médio", f"{df['ICI'].mean():.1f}")

with col4:
    st.metric("Ticket Médio", f"R$ {df['AvgInvoiceTicket'].mean():.2f}")

st.divider()

# Filtros
st.sidebar.header("Filtros")


nomes_cluster = {
    0:"Premium",
    1:"Crítico",
    2:"Moderado",
    3:"Recorrente"
}

df["NomeCluster"]= df["Cluster"].map(nomes_cluster)
cluster_opcoes = sorted(df["NomeCluster"].unique())
cluster_selecionado = st.sidebar.multiselect(
    "Selecione o Cluster",
    options=cluster_opcoes,
    default=cluster_opcoes
)

df_filtrado = df[df["NomeCluster"].isin(cluster_selecionado)]

st.subheader("📌 Visão Geral por Cluster")

col5, col6 = st.columns(2)

with col5:
    st.bar_chart(df_filtrado.groupby("Cluster")["ICI"].mean())

with col6:
    st.bar_chart(df_filtrado.groupby("Cluster")["Monetary"].sum())

st.divider()

# Consulta por cliente
st.subheader("🔎 Consulta Individual de Cliente")

cliente = st.selectbox(
    "Selecione um CustomerID",
    sorted(df_filtrado["CustomerID"].unique())
)

cliente_df = df_filtrado[df_filtrado["CustomerID"] == cliente].iloc[0]

col7, col8, col9 = st.columns(3)

with col7:
    st.metric("ICI do Cliente", f"{cliente_df['ICI']:.1f}")

with col8:
    st.metric("Cluster", int(cliente_df["Cluster"]))

with col9:
    st.metric("Gasto Total", f"R$ {cliente_df['Monetary']:,.2f}")

col10, col11, col12 = st.columns(3)

with col10:
    st.metric("Frequência", f"{cliente_df['Frequency']:.0f}")

with col11:
    st.metric("Ticket Médio", f"R$ {cliente_df['AvgInvoiceTicket']:,.2f}")

with col12:
    st.metric("Price Index", f"{cliente_df['PriceIndex']:.2f}")

st.markdown("### 💡 Recomendação Automática")
st.info(cliente_df["Recomendacao"])

st.divider()

# Tabela final
st.subheader("📋 Base de Clientes com ICI e Recomendações")

st.dataframe(
    df_filtrado[
        [
            "CustomerID",
            "Cluster",
            "ICI",
            "Recency",
            "Frequency",
            "Monetary",
            "AvgInvoiceTicket",
            "PriceIndex",
            "Recomendacao"
        ]
    ],
    use_container_width=True
)