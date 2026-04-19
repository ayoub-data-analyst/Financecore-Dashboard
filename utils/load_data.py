import pandas as pd
import streamlit as st
from utils.get_engine import get_engine

@st.cache_data
def load_data(query):
    engine = get_engine()
    return pd.read_sql(query, engine)