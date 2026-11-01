"""Panoramica - Visione d'insieme del bilancio dello Stato."""

import streamlit as st
import plotly.graph_objects as go

from sources import load_saldi_anno, load_composizione_spesa, load_pagamenti_anno, load_costo_debito, get_last_updated, load_lb_spese_anno

st.title("🇮🇹 Bilancio dello Stato Italiano")
st.sidebar.caption(f"Aggiornato: {get_last_updated()}")

# --- Load data ---
df_saldi = load_saldi_anno()
df_comp = load_composizione_spesa()
df_pag = load_pagamenti_anno()
df_deb = load_costo_debito()
df_lb = load_lb_spese_anno()

if df_saldi.empty:
    st.warning("Nessun dato disponibile. Esegui `make run` prima.")
    st.stop()

latest = int(df_saldi["anno"].max())
prev = latest - 1
row = df_saldi[df_saldi["anno"] == latest].iloc[0]
row_prev = df_saldi[df_saldi["anno"] == prev].iloc[0] if prev in df_saldi["anno"].values else None

# --- KPI in alto ---
if not df_lb.empty:
    lb_latest = int(df_lb["anno"].max())
    lb_row = df_lb[df_lb["anno"] == lb_latest].iloc[0]
    col1, col2, col3 = st.columns(3)
else:
    col1, col2, col3 = st.columns(3)

delta_deficit = None
if row_prev is not None:
    d = abs(row["saldo_netto_da_finanziare"]) - abs(row_prev["saldo_netto_da_finanziare"])
    delta_deficit = f"{d/1e9:+,.0f} mld"
col1.metric(
    "📉 Deficit",
    f"€ {abs(row['saldo_netto_da_finanziare'])/1e9:,.0f} mld",
    delta=delta_deficit,
    help=f"Saldo netto da finanziare {latest}",
)
delta_avanzo = None
if row_prev is not None:
    delta_avanzo = f"{(row['avanzo_primario'] - row_prev['avanzo_primario'])/1e9:+,.0f} mld"
col2.metric(
    "⚖️ Avanzo Primario",
    f"€ {row['avanzo_primario']/1e9:,.0f} mld",
    delta=delta_avanzo,
)
if not df_lb.empty:
    col3.metric(
        "📋 Previsione governo (LB)",
        f"€ {lb_row['lb_totale_cp_mld']:.0f} mld",
        help=f"Legge di Bilancio {lb_latest} — previsioni iniziali",
    )
else:
    col3.metric("📋 Previsione governo (LB)", "N/D")

# --- Trend Saldo Netto ---
st.subheader(f"Evoluzione saldi (2003-{latest})")

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_saldi["anno"],
    y=df_saldi["saldo_netto_da_finanziare"] / 1e9,
    name="Saldo netto",
    marker_color=["#e74c3c" if v < 0 else "#2ecc71" for v in df_saldi["saldo_netto_da_finanziare"] / 1e9],
))
fig.add_hline(y=0, line_dash="dash", line_color="gray")
fig.update_layout(
    yaxis_title="Milioni di €",
    height=350,
    margin={"t": 30},
    showlegend=False,
)
st.plotly_chart(fig, width="stretch")

# --- Composizione Spesa ---
st.subheader("Composizione della spesa")

if not df_comp.empty:
    latest_comp = min(latest, int(df_comp["anno"].max()))
    row_comp = df_comp[df_comp["anno"] == latest_comp].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔵 Trasferimenti", f"{row_comp['trasferimenti_mld']:.0f} mld", f"{row_comp['pct_trasferimenti']:.0f}%")
    c2.metric("🔴 Debito", f"{row_comp['onere_debito_mld'] + row_comp['rimborso_debito_mld']:.0f} mld",
              f"{row_comp['quota_debito_totale_pct']:.0f}%")
    c3.metric("🟢 Investimenti", f"{row_comp['investimenti_mld']:.0f} mld",
              f"{row_comp['pct_investimenti']:.0f}%")
    c4.metric("🟡 Funzionamento", f"{row_comp['funzionamento_mld']:.0f} mld",
              f"{row_comp['pct_funzionamento']:.0f}%")

    st.caption(f"Anno: {latest_comp} · Totale: {row_comp['totale_mld']:.0f} mld")

# --- Trend Debito Bilancio ---
st.subheader("Interessi pagati sul debito")

if not df_deb.empty:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_deb["anno"],
        y=df_deb["interessi_pagati"] / 1e9,
        name="Interessi pagati",
        line={"color": "#e74c3c", "width": 2},
        fill="tozeroy",
        fillcolor="rgba(231,76,60,0.1)",
    ))
    fig3.update_layout(
        yaxis_title="Milioni di €",
        height=300,
        margin={"t": 30},
    )
    st.plotly_chart(fig3, width="stretch")
