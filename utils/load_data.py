import pandas as pd
import streamlit as st
from sqlalchemy import text
from utils.connection_db import get_engine

@st.cache_data
def load_data(query):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()