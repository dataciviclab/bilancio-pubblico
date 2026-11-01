"""Entrate - Come finanzia lo Stato le sue spese."""

import streamlit as st
import plotly.graph_objects as go

from sources import load_entrate_anno, load_trend_tributarie, load_entrate_titolo

st.title("📈 Entrate dello Stato")

df_anno = load_entrate_anno()
df_trib = load_trend_tributarie()
df_titolo = load_entrate_titolo()

if df_anno.empty:
    st.warning("Nessun dato.")
    st.stop()

latest = int(df_anno["anno"].max())
prev = latest - 1

# --- KPI in alto ---
latest_row = df_anno[df_anno["anno"] == latest].iloc[0]
trib_row = df_trib[df_trib["anno"] == latest].iloc[0] if latest in df_trib["anno"].values else None

col1, col2, col3 = st.columns(3)
delta_ent = f"{latest_row['var_pct_cp']:+.1f}%" if latest_row["var_pct_cp"] == latest_row["var_pct_cp"] else None
col1.metric("Entrate totali CP", f"€ {latest_row['entrate_totali_cp']/1e9:,.0f} mld", delta=delta_ent)
if trib_row is not None:
    trib_prev = df_trib[df_trib["anno"] == prev].iloc[0] if prev in df_trib["anno"].values else None
    delta_trib = None
    if trib_prev is not None:
        delta_trib = f"{(trib_row['quota_tributarie_cp'] - trib_prev['quota_tributarie_cp'])*100:+.1f}pp"
    col2.metric("Quota tributarie", f"{trib_row['quota_tributarie_cp']*100:.1f}%", delta=delta_trib)
col3.metric("Anni disponibili", f"{len(df_anno)}")

# --- Trend entrate totali ---
st.subheader("Trend entrate totali (Previsioni Definitive CP)")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_anno["anno"], y=df_anno["entrate_totali_cp"] / 1e9,
    name="Entrate totali", line=dict(color="#2ecc71", width=2),
    fill="tozeroy", fillcolor="rgba(46,204,113,0.1)",
))
fig.update_layout(yaxis_title="Milioni di €", height=350, margin={"t": 30})
st.plotly_chart(fig, width="stretch")

# --- Quote tributarie ---
st.subheader("Peso delle entrate tributarie")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=df_trib["anno"], y=df_trib["quota_tributarie_cp"] * 100,
    name="Tributarie %", line=dict(color="#e74c3c", width=2),
))
fig2.add_hline(y=60, line_dash="dash", line_color="gray", annotation_text="60%")
fig2.update_layout(yaxis_title="% sul totale", height=300, margin={"t": 30})
st.plotly_chart(fig2, width="stretch")

# --- Top titoli ---
st.subheader(f"Composizione entrate per Titolo ({latest})")

titoli = df_titolo[df_titolo["anno"] == latest].copy()
if not titoli.empty:
    titoli = titoli.sort_values("totale_cp", ascending=False)
    fig3 = go.Figure(go.Bar(
        x=titoli["titolo_breve"], y=titoli["totale_cp"] / 1e9,
        marker_color="#3498db",
    ))
    fig3.update_layout(
        yaxis_title="Miliardi di €",
        height=350,
        margin={"t": 30},
        xaxis=dict(categoryorder="total descending"),
    )
    st.plotly_chart(fig3, width="stretch")
