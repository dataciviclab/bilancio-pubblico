"""Spese per Missione - Dove va la spesa dello Stato."""

import streamlit as st
import plotly.graph_objects as go

from sources import load_spese_missione, load_spese_anno

st.title("💰 Spese per Missione")

df_miss = load_spese_missione()
df_anno = load_spese_anno()

if df_miss.empty:
    st.warning("Nessun dato.")
    st.stop()

latest = int(df_anno["anno"].max()) if not df_anno.empty else 2024

# --- KPI in alto ---
if not df_anno.empty:
    row = df_anno[df_anno["anno"] == latest].iloc[0]
    col1, col2 = st.columns(2)
    col1.metric("Spese totali CP", f"€ {row['spese_totali_cp']/1e9:,.0f} mld")
    col2.metric("Variazione %", f"{row['var_pct_cp']:+.1f}%")

# --- Top10 missioni ---
st.subheader(f"Top 10 missioni per importo ({latest})")

top10 = df_miss[df_miss["anno"] == latest].nlargest(10, "totale_cp")
fig = go.Figure(go.Bar(
    x=top10["totale_cp"] / 1e9,
    y=top10["missione"],
    orientation="h",
    marker_color="#3498db",
))
fig.update_layout(
    yaxis=dict(categoryorder="total ascending"),
    xaxis_title="Miliardi di €",
    height=400,
    margin={"t": 30},
)
st.plotly_chart(fig, width="stretch")

# --- Trend spese totali ---
st.subheader("Trend spese totali")

if not df_anno.empty:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_anno["anno"], y=df_anno["spese_totali_cp"] / 1e9,
        name="Spese CP", line=dict(color="#e74c3c", width=2),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.1)",
    ))
    fig2.update_layout(yaxis_title="Milioni di €", height=300, margin={"t": 30})
    st.plotly_chart(fig2, width="stretch")
