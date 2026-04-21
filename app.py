import streamlit as st

# App Configuration

st.set_page_config(
    page_title="FinanceCore Dashboard",
    layout="wide"
)


# Home Page

st.title("FinanceCore Dashboard")

st.markdown("""
Welcome to the **FinanceCore SA Strategic Dashboard**.

### Objectives:
- Monitor financial performance  
- Analyze transaction activity 
- Identify and assess client risk  

### Available Pages:
- **Executive View** → High-level KPIs and performance overview  
- **Risk Analysis** → Advanced insights into client risk  

---
Use the sidebar on the left to navigate between pages.
""")


# Footer

st.markdown("---")
st.caption("FinanceCore Dashboard | Data Analyst Project")