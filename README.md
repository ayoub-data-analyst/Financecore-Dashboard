# FinanceCore Dashboard

A strategic business intelligence dashboard built with **Streamlit** and  **PostgreSQL** , designed to monitor financial performance, analyze transaction activity, and assess client risk for FinanceCore SA.

---

## Overview

FinanceCore Dashboard provides two analytical views:

* **Executive View** — High-level KPIs, monthly transaction trends, revenue by agency/product, and client segment breakdown.
* **Risk Analysis** — Credit score correlation heatmap, scatter analysis by risk category, and a ranked table of top at-risk clients.

---

## Project Structure

```
FINANCECORE_DASHBOARD/
├── app.py                    # Entry point — Streamlit home page
├── pages/
│   ├── 1_Executive_View.py   # KPIs, charts, filters, CSV export
│   └── 2_Risk_Analysis.py    # Heatmap, scatter plot, risk client table
├── utils/
│   ├── connection_db.py      # SQLAlchemy engine (cached, with logging)
│   ├── load_data.py          # Cached query executor → DataFrame
│   └── query.py              # All SQL queries (Executive + Risk)
├── .env                      # DB credentials (not committed)
├── .gitignore
├── requirements.txt
└── project.log               # Runtime logs
```

---

## Database Schema

The app connects to a **PostgreSQL** database using a star schema:

| Table                 | Description                                                            |
| --------------------- | ---------------------------------------------------------------------- |
| `fact_transactions` | Core transaction facts (montant, débits, crédits, statut, solde_net) |
| `dim_clients`       | Client dimension (segment, score_credit_client, categorie_risque)      |
| `dim_agences`       | Agency dimension                                                       |
| `dim_produits`      | Product dimension                                                      |
| `dim_dates`         | Date dimension (mois, anne)                                            |

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd FINANCECORE_DASHBOARD
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_USER=your_postgres_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

---

## Features

### Executive View (`pages/1_Executive_View.py`)

* **Sidebar filters** by Agency, Client Segment, Product, and Year
* **KPI metrics** : Total Revenue (CA), Transaction Count, Active Clients, Average Margin
* **Line chart** : Monthly debit vs. credit trends
* **Bar chart** : Revenue by agency and product
* **Pie chart** : Client distribution by segment
* **CSV export** of KPI data

### Risk Analysis (`pages/2_Risk_Analysis.py`)

* **Correlation heatmap** : Relationship between credit score, transaction amount, and rejection rate
* **Scatter plot** : Transaction amount vs. credit score, colored by risk category (High / Medium / Low)
* **Top 10 at-risk clients** table with color-coded risk labels

---

## Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Frontend        | Streamlit 1.56            |
| Charts          | Plotly / Plotly Express   |
| Database        | PostgreSQL                |
| ORM / Connector | SQLAlchemy 2.x + psycopg2 |
| Data processing | pandas, numpy             |
| Environment     | python-dotenv             |

---

## Logging

Application events and errors are written to `project.log` in the project root. The log format is:

```
YYYY/MM/DD HH:MM:SS - LEVEL - Message
```

---

## Notes

* All database queries are defined in `utils/query.py` and executed through the cached `load_data()` function, which returns an empty DataFrame on error instead of crashing the app.
* The SQLAlchemy engine is cached with `@st.cache_resource` to avoid reconnecting on every page rerender.
* Never commit your `.env` file — it is listed in `.gitignore`.
