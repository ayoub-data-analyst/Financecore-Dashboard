# EXECUTIVE

def get_kpis_filtered():
    return """
    SELECT
        ROUND(SUM(t.solde_net)::numeric, 2) AS ca_total,
        COUNT(*) AS total_transactions,
        COUNT(DISTINCT t.client_id) AS clients_actifs,
        ROUND(AVG(t.solde_net)::numeric, 2) AS marge_moyenne
    FROM fact_transactions t
    JOIN dim_clients c ON t.client_id = c.client_id
    JOIN dim_agences a ON t.agence_id = a.agence_id
    JOIN dim_produits p ON t.produit_id = p.produit_id
    JOIN dim_dates d ON t.date_id = d.date_id
    WHERE 1=1
    """

def get_monthly_transactions():
    return """
    SELECT
        d.mois,
        ROUND(SUM(t."débits")::numeric, 2) AS total_debit,
        ROUND(SUM(t."crédits")::numeric, 2) AS total_credit
    FROM fact_transactions t
    JOIN dim_dates d ON t.date_id = d.date_id
    JOIN dim_clients c ON t.client_id = c.client_id
    JOIN dim_agences a ON t.agence_id = a.agence_id
    JOIN dim_produits p ON t.produit_id = p.produit_id
    WHERE 1=1
    """

def get_ca_agence():
    return """
    SELECT
        a.agence,
        p.produit,
        ROUND(SUM(t.montant)::numeric, 2) AS total_ca
    FROM fact_transactions t
    JOIN dim_produits p ON t.produit_id = p.produit_id
    JOIN dim_agences a ON t.agence_id = a.agence_id
    JOIN dim_clients c ON t.client_id = c.client_id
    JOIN dim_dates d ON t.date_id = d.date_id
    WHERE 1=1
    """

def get_client_segment():
    return """
    SELECT segment_client, COUNT(*) AS total
    FROM dim_clients
    GROUP BY segment_client
    """


# RISK

def get_risk_data():
    return """
    SELECT
        c.score_credit_client AS score_credit,
        t.montant,
        CASE WHEN t.statut = 'Rejete' THEN 1 ELSE 0 END AS taux_rejet,
        c.categorie_risque
    FROM fact_transactions t
    JOIN dim_clients c ON t.client_id = c.client_id
    """

def get_top_risk_clients():
    return """
    SELECT
        c.client_id,
        c.score_credit_client AS score_credit,
        ROUND(AVG(CASE WHEN t.statut = 'Rejete' THEN 1 ELSE 0 END)::numeric,2) AS taux_rejet,
        ROUND(SUM(t.montant)::numeric,2) AS montant_total,
        c.categorie_risque
    FROM fact_transactions t
    JOIN dim_clients c ON t.client_id = c.client_id
    GROUP BY c.client_id, c.score_credit_client, c.categorie_risque
    ORDER BY score_credit ASC
    LIMIT 10
    """