"""La catena del bilancio — dove si genera lo scostamento tra gli stadi."""

import pandas as pd
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
    "Il percorso della spesa: disegno di legge del governo → legge approvata → "
    "previsione definitiva → impegni → pagamenti. Qui si vede **dove** si genera lo scostamento; "
    "l'esito per missione è in **Promesse vs Realtà**."
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

anni = sorted(trend["anno"].dropna().astype(int).unique().tolist())
anno = st.selectbox("Anno di bilancio", anni, index=len(anni) - 1)
row = trend[trend["anno"] == anno].iloc[0]


def value(col):
    v = row.get(col)
    return 0.0 if pd.isna(v) else float(v)


steps = ["DLB", "LB", "Definitiva", "Impegnato", "Pagato"]
vals = {s: value(s) for s in steps}
ys = [
    vals["DLB"],
    vals["LB"] - vals["DLB"],
    vals["Definitiva"] - vals["LB"],
    vals["Impegnato"] - vals["Definitiva"],
    vals["Pagato"] - vals["Impegnato"],
]
measures = ["absolute", "relative", "relative", "relative", "relative"]
texts = [f"{y:,.0f}" if m == "absolute" else f"{y:+,.0f}" for y, m in zip(ys, measures)]

# --- Waterfall degli scostamenti ---
st.subheader(f"Gli scostamenti tra gli stadi — {anno}")

fig = go.Figure(
    go.Waterfall(
        x=steps,
        y=ys,
        measure=measures,
        text=texts,
        textposition="outside",
        connector=dict(line=dict(color="#bdc3c7")),
        increasing=dict(marker_color="#27ae60"),
        decreasing=dict(marker_color="#c0392b"),
        totals=dict(marker_color="#3498db"),
    )
)
fig.update_layout(
    yaxis_title="Miliardi di €",
    height=420,
    margin={"t": 40},
    showlegend=False,
)
st.plotly_chart(fig, width="stretch")

# --- Tabella scostamenti ---
scost = pd.DataFrame(
    {
        "Passaggio": ["DLB → LB (Parlamento)", "LB → definitiva (assestamento)", "Definitiva → impegnato", "Impegnato → pagato"],
        "Variazione (mld)": [ys[1], ys[2], ys[3], ys[4]],
    }
)
st.dataframe(scost, width="stretch", hide_index=True)

# --- Trend dei cinque stadi ---
st.subheader("I cinque stadi nel tempo")
fig2 = go.Figure()
for col, color, dash in [
    ("DLB", "#8e44ad", "dot"),
    ("LB", "#3498db", "solid"),
    ("Definitiva", "#f39c12", "dash"),
    ("Impegnato", "#e74c3c", "solid"),
    ("Pagato", "#2ecc71", "dot"),
]:
    if col in trend.columns:
        fig2.add_trace(go.Scatter(x=trend["anno"], y=trend[col], name=col, line=dict(color=color, width=2, dash=dash)))
fig2.update_layout(yaxis_title="Miliardi di €", height=420, margin={"t": 30}, legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig2, width="stretch")

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
]:
    part = per_missione(df, col, ann).rename(columns={col: name})
    m = m.merge(part, on="missione", how="outer")
m = m.fillna(0.0).sort_values("Impegnato", ascending=False)

top = m.head(12).sort_values("Impegnato")
fig3 = go.Figure()
for col, color in [("DLB", "#8e44ad"), ("LB", "#3498db"), ("Definitiva", "#f39c12"), ("Impegnato", "#e74c3c")]:
    fig3.add_trace(go.Bar(y=top["missione"], x=top[col], name=col, orientation="h", marker_color=color))
fig3.update_layout(
    barmode="group",
    xaxis_title="Miliardi di €",
    height=560,
    margin={"t": 30},
    legend=dict(orientation="h", y=-0.12),
    yaxis=dict(categoryorder="array", categoryarray=top["missione"].tolist()),
)
st.plotly_chart(fig3, width="stretch")

st.info(
    "DLB e LB sono le previsioni iniziali sull'anno di bilancio (annualità 1); "
    "la definitiva è il bilancio dopo assestamento e variazioni; l'impegnato è pagato + residui. "
    "Missione e programma non esistono nei dati DLB/LB prima del 2008-2009."
)
