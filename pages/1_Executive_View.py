import streamlit as st
import plotly.express as px
from utils.load_data import load_data
from utils.query import (
    get_kpis_filtered,
    get_monthly_transactions,
    get_ca_agence,
    get_client_segment
)

st.set_page_config(layout="wide")
st.title("Executive Dashboard")


# Filters

st.sidebar.markdown("### Filters")

df_agence = load_data("SELECT agence FROM dim_agences")
agence = st.sidebar.selectbox(
    "Agence",
    ["All"] + sorted(df_agence["agence"].unique().tolist()),
    key="agence"
)

df_segment = load_data("SELECT DISTINCT segment_client FROM dim_clients")
segment = st.sidebar.selectbox(
    "Segment",
    ["All"] + sorted(df_segment["segment_client"].unique().tolist()),
    key="segment"
)

df_produit = load_data("SELECT produit FROM dim_produits")
produit = st.sidebar.selectbox(
    "Produit",
    ["All"] + sorted(df_produit["produit"].unique().tolist()),
    key="produit"
)

df_annee = load_data("SELECT DISTINCT anne FROM dim_dates ORDER BY anne")
annee = st.sidebar.selectbox(
    "Année",
    ["All"] + df_annee["anne"].tolist(),
    key="annee"
)


# WHERE builder

def build_where():
    filters = []

    if agence != "All":
        filters.append(f"a.agence = '{agence}'")
    if segment != "All":
        filters.append(f"c.segment_client = '{segment}'")
    if produit != "All":
        filters.append(f"p.produit = '{produit}'")
    if annee != "All":
        filters.append(f"d.anne = {annee}")

    return " AND " + " AND ".join(filters) if filters else ""

where = build_where()


# KPIs

df_kpis = load_data(get_kpis_filtered() + where)

if not df_kpis.empty:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("CA", df_kpis["ca_total"][0] or 0)
    col2.metric("Transactions", df_kpis["total_transactions"][0] or 0)
    col3.metric("Clients", df_kpis["clients_actifs"][0] or 0)
    col4.metric("Marge", round(df_kpis["marge_moyenne"][0] or 0, 2))

st.divider()


# Line Chart
df_line = load_data(get_monthly_transactions() + where + " GROUP BY d.mois ORDER BY d.mois")

if not df_line.empty:
    st.plotly_chart(
        px.line(df_line, x="mois", y=["total_debit", "total_credit"]),
        use_container_width=True
    )


# Bar Chart

df_bar = load_data(get_ca_agence() + where + " GROUP BY a.agence, p.produit ORDER BY total_ca DESC")

if not df_bar.empty:
    st.plotly_chart(
        px.bar(df_bar, x="agence", y="total_ca", color="produit"),
        use_container_width=True
    )


# Pie

df_pie = load_data(get_client_segment())

if not df_pie.empty:
    st.plotly_chart(
        px.pie(df_pie, names="segment_client", values="total"),
        use_container_width=True
    )


# Export

if not df_kpis.empty:
    st.download_button(
        "Export CSV",
        df_kpis.to_csv(index=False),
        "kpis.csv"
    )