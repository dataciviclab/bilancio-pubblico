"""La catena del bilancio — dal disegno di legge al consuntivo."""

import streamlit as st
import plotly.graph_objects as go

from sources import (
    load_dlb_serie_missione,
    load_lb_serie_missione,
    load_rnd_serie_missione,
    load_consuntivo_spese_missione,
)

st.title("🔗 La catena del bilancio")

st.caption(
    "Quattro stadi: disegno di legge del governo → legge approvata dal Parlamento → "
    "previsione definitiva → spese impegnate e pagate."
)

dlb = load_dlb_serie_missione()
lb = load_lb_serie_missione()
rnd = load_rnd_serie_missione()
cons = load_consuntivo_spese_missione()

if dlb.empty or lb.empty or cons.empty:
    st.warning("Dati insufficienti per ricostruire la catena.")
    st.stop()


def tot(df, col, annualita=None):
    d = df.copy()
    if annualita is not None and "annualita" in d.columns:
        d = d[d["annualita"] == annualita]
    return d.groupby("anno", as_index=False)[col].sum()


dlb_t = tot(dlb, "cp_mld", 1).rename(columns={"cp_mld": "DLB"})
lb_t = tot(lb, "cp_mld", 1).rename(columns={"cp_mld": "LB"})
rnd_t = tot(rnd, "cp_mld", 1).rename(columns={"cp_mld": "Definitiva"})
imp_t = tot(cons, "totale_cp_mld").rename(columns={"totale_cp_mld": "Impegnato"})
pag_t = tot(cons, "pagato_cp_mld").rename(columns={"pagato_cp_mld": "Pagato"})

trend = dlb_t.merge(lb_t, on="anno", how="outer")
trend = trend.merge(rnd_t, on="anno", how="outer")
trend = trend.merge(imp_t, on="anno", how="outer")
trend = trend.merge(pag_t, on="anno", how="outer").sort_values("anno")

# --- Anno ---
anni = sorted(trend["anno"].dropna().astype(int).unique().tolist())
anno = st.selectbox("Anno di bilancio", anni, index=len(anni) - 1)

# --- KPI scostamenti ---
row = trend[trend["anno"] == anno].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("DLB (governo)", f"€ {row.get('DLB', 0):,.0f} mld")
c2.metric("LB (Parlamento)", f"€ {row.get('LB', 0):,.0f} mld", delta=f"{row.get('LB', 0) - row.get('DLB', 0):+,.0f} mld")
c3.metric("Previsione definitiva", f"€ {row.get('Definitiva', 0):,.0f} mld", delta=f"{row.get('Definitiva', 0) - row.get('LB', 0):+,.0f} mld")
c4.metric("Impegnato", f"€ {row.get('Impegnato', 0):,.0f} mld", delta=f"{row.get('Impegnato', 0) - row.get('Definitiva', 0):+,.0f} mld")

# --- Trend ---
st.subheader("I quattro stadi nel tempo")
fig = go.Figure()
for col, color, dash in [
    ("DLB", "#8e44ad", "dot"),
    ("LB", "#3498db", "solid"),
    ("Definitiva", "#f39c12", "dash"),
    ("Impegnato", "#e74c3c", "solid"),
    ("Pagato", "#2ecc71", "dot"),
]:
    if col in trend.columns:
        fig.add_trace(go.Scatter(x=trend["anno"], y=trend[col], name=col, line=dict(color=color, width=2, dash=dash)))
fig.update_layout(yaxis_title="Miliardi di €", height=420, margin={"t": 30}, legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig, width="stretch")

# --- Per missione ---
st.subheader(f"Per missione — {anno}")


def per_missione(df, col, annualita=None):
    d = df.copy()
    if annualita is not None and "annualita" in d.columns:
        d = d[d["annualita"] == annualita]
    d = d[d["anno"] == anno]
    return d.groupby("missione", as_index=False)[col].sum()


m = per_missione(dlb, "cp_mld", 1).rename(columns={"cp_mld": "DLB"})
for df, col, name, ann in [
    (lb, "cp_mld", "LB", 1),
    (rnd, "cp_mld", "Definitiva", 1),
    (cons, "totale_cp_mld", "Impegnato", None),
    (cons, "pagato_cp_mld", "Pagato", None),
]:
    part = per_missione(df, col, ann).rename(columns={col: name})
    m = m.merge(part, on="missione", how="outer")
m = m.fillna(0.0).sort_values("Impegnato", ascending=False)

top = m.head(12).sort_values("Impegnato")
fig2 = go.Figure()
for col, color in [("DLB", "#8e44ad"), ("LB", "#3498db"), ("Definitiva", "#f39c12"), ("Impegnato", "#e74c3c")]:
    fig2.add_trace(go.Bar(y=top["missione"], x=top[col], name=col, orientation="h", marker_color=color))
fig2.update_layout(barmode="group", xaxis_title="Miliardi di €", height=560, margin={"t": 30}, legend=dict(orientation="h", y=-0.12), yaxis=dict(categoryorder="array", categoryarray=top["missione"].tolist()))
st.plotly_chart(fig2, width="stretch")

st.info(
    "DLB e LB qui sono le previsioni iniziali sull'anno di bilancio (annualità 1); "
    "la definitiva è il bilancio dopo assestamento e variazioni; l'impegnato è pagato + residui. "
    "Missione e programma non esistono nei dati DLB/LB prima del 2008-2009."
)
