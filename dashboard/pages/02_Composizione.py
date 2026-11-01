"""Composizione Spesa - Come lo Stato divide i suoi soldi."""

import streamlit as st
import plotly.graph_objects as go

from sources import load_composizione_spesa

st.title("🧩 Composizione della Spesa dello Stato")

df = load_composizione_spesa()
if df.empty:
    st.warning("Nessun dato.")
    st.stop()

latest = int(df["anno"].max())
row = df[df["anno"] == latest].iloc[0]

# --- KPI in alto ---
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Investimenti reali",
    f"{row['pct_investimenti']:.1f}%",
    help=f"Trend: {df['pct_investimenti'].iloc[0]:.1f}% nel {int(df['anno'].iloc[0])}",
)
col2.metric(
    "Debito totale",
    f"{row['quota_debito_totale_pct']:.1f}%",
    help="Interessi + rimborso",
)
col3.metric("Trasferimenti", f"{row['pct_trasferimenti']:.1f}%")
col4.metric("Funzionamento", f"{row['pct_funzionamento']:.1f}%")

st.info(
    "**Trasferimenti** = a regioni, enti locali, famiglie, imprese. "
    "**Investimenti reali** = investimenti fissi lordi. "
    "**Debito** = oneri (interessi) + rimborso."
)

# --- Trend area chart ---
st.subheader(f"Evoluzione composizione spesa ({int(df['anno'].min())}-{latest})")

fig = go.Figure()
for col_name, label, color in [
    ("trasferimenti_mld", "Trasferimenti", "#3498db"),
    ("onere_debito_mld", "Debito (interessi)", "#e74c3c"),
    ("investimenti_mld", "Investimenti reali", "#2ecc71"),
    ("funzionamento_mld", "Funzionamento", "#f39c12"),
    ("rimborso_debito_mld", "Rimborso debito", "#c0392b"),
    ("altri_mld", "Altri", "#95a5a6"),
]:
    fig.add_trace(
        go.Scatter(
            x=df["anno"],
            y=df[col_name],
            name=label,
            stackgroup="one",
            line=dict(width=0.5, color=color),
            fillcolor=color,
        )
    )

fig.update_layout(
    yaxis_title="Milioni di €",
    height=450,
    legend=dict(orientation="h", y=-0.2),
    margin={"t": 30},
)
st.plotly_chart(fig, width="stretch")

# --- Quote percentuali ---
st.subheader("Quote percentuali sul totale")

fig2 = go.Figure()
for col_name, label, color in [
    ("pct_trasferimenti", "Trasferimenti", "#3498db"),
    ("pct_onere_debito", "Interessi debito", "#e74c3c"),
    ("pct_investimenti", "Investimenti reali", "#2ecc71"),
    ("pct_funzionamento", "Funzionamento", "#f39c12"),
    ("pct_rimborso_debito", "Rimborso debito", "#c0392b"),
]:
    fig2.add_trace(
        go.Scatter(
            x=df["anno"],
            y=df[col_name],
            name=label,
            line=dict(width=2),
        )
    )

fig2.update_layout(
    yaxis_title="% sul totale",
    height=400,
    legend=dict(orientation="h", y=-0.2),
    margin={"t": 30},
)
st.plotly_chart(fig2, width="stretch")
