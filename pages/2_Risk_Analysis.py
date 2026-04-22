import streamlit as st
import plotly.express as px
from utils.load_data import load_data
from utils.query import get_risk_data, get_top_risk_clients

st.set_page_config(layout="wide")
st.title("Risk Analysis")

df = load_data(get_risk_data())

# Heatmap

corr = df[["score_credit", "montant", "taux_rejet"]].corr()

st.plotly_chart(
    px.imshow(corr, text_auto=True, color_continuous_scale="RdBu"),
)

st.divider()

# Scatter

st.plotly_chart(
    px.scatter(
        df,
        x="score_credit",
        y="montant",
        color="categorie_risque"
    ),
)

st.divider()

# Top clients

df_top = load_data(get_top_risk_clients())

def risk_label(x):
        return "🔴 High" if x == "High" else "🟠 Medium" if x == "Medium" else "🟢 Low"

df_top["categorie_risque"] = df_top["categorie_risque"].apply(risk_label)

st.dataframe(df_top)