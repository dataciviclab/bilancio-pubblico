"""Promesse vs Realtà — l'esito: quanto la previsione iniziale è stata rispettata."""

import streamlit as st
import plotly.graph_objects as go

from sources import (
    load_lb_serie_missione,
    load_rnd_serie_missione,
    load_consuntivo_spese_missione,
)

st.title("⚖️ Promesse vs Realtà")

st.caption(
    "Quanto la Legge di Bilancio è stata rispettata: scostamento tra previsione iniziale "
    "e spese effettivamente impegnate e pagate. Per il percorso tra gli stadi vedi "
    "**Catena del Bilancio**; per gli obiettivi e i target dichiarati vedi "
    "**Cosa promette lo Stato**."
)

df_lb = load_lb_serie_missione()
df_rnd = load_rnd_serie_missione()
df_cons = load_consuntivo_spese_missione()

if df_lb.empty or df_cons.empty:
    st.warning("Dati insufficienti: servono LB serie e consuntivo spese.")
    st.stop()


def per_missione(df, value, annualita=None):
    d = df.copy()
    if annualita is not None and "annualita" in d.columns:
        d = d[d["annualita"] == annualita]
    return d.groupby(["anno", "missione"], as_index=False)[value].sum()


lb = per_missione(df_lb, "cp_mld", annualita=1)
rnd = per_missione(df_rnd, "cp_mld", annualita=1)
impegnato = per_missione(df_cons, "totale_cp_mld")
pagato = per_missione(df_cons, "pagato_cp_mld")

anni = sorted(set(lb["anno"]) & set(impegnato["anno"]))
if not anni:
    st.warning("Nessun anno in comune tra LB e consuntivo.")
    st.stop()

anno = st.selectbox("Anno di bilancio", anni, index=len(anni) - 1)


def tot(df, col, a):
    return float(df[df["anno"] == a][col].sum())


v_lb = tot(lb, "cp_mld", anno)
v_rnd = tot(rnd, "cp_mld", anno)
v_imp = tot(impegnato, "totale_cp_mld", anno)
v_pag = tot(pagato, "pagato_cp_mld", anno)

# --- KPI: l'esito dell'anno ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 LB (previsione)", f"€ {v_lb:,.0f} mld")
c2.metric("📅 Previsione definitiva", f"€ {v_rnd:,.0f} mld", delta=f"{v_rnd - v_lb:+,.0f} mld")
c3.metric("🧾 Impegnato", f"€ {v_imp:,.0f} mld", delta=f"{v_imp - v_lb:+,.0f} mld vs LB")
c4.metric("💸 Pagato", f"€ {v_pag:,.0f} mld", delta=f"{(v_pag / v_imp - 1) * 100:+.1f}%" if v_imp else None)

# --- Base per missione ---
base = lb[lb["anno"] == anno][["missione", "cp_mld"]].rename(columns={"cp_mld": "LB"})
base = base.merge(
    rnd[rnd["anno"] == anno][["missione", "cp_mld"]].rename(columns={"cp_mld": "Prev. definitiva"}),
    on="missione",
    how="outer",
)
base = base.merge(
    impegnato[impegnato["anno"] == anno][["missione", "totale_cp_mld"]].rename(columns={"totale_cp_mld": "Impegnato"}),
    on="missione",
    how="outer",
)
base = base.merge(
    pagato[pagato["anno"] == anno][["missione", "pagato_cp_mld"]].rename(columns={"pagato_cp_mld": "Pagato"}),
    on="missione",
    how="outer",
)
base = base.fillna(0.0)

base["Gap mld"] = base["LB"] - base["Impegnato"]
base["Gap %"] = base.apply(
    lambda r: round((r["LB"] - r["Impegnato"]) / r["Impegnato"] * 100, 1) if r["Impegnato"] else None,
    axis=1,
)

# --- Dove la promessa è stata disattesa ---
st.subheader(f"Dove la promessa è stata disattesa — {anno}")

gap = base.reindex(base["Gap mld"].abs().sort_values(ascending=False).index).head(12)
gap = gap.sort_values("Gap mld")
colors = ["#c0392b" if v > 0 else "#27ae60" for v in gap["Gap mld"]]

fig = go.Figure(
    go.Bar(
        x=gap["Gap mld"],
        y=gap["missione"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:+,.1f}" for v in gap["Gap mld"]],
        textposition="outside",
    )
)
fig.add_vline(x=0, line_color="gray", line_width=1)
fig.update_layout(
    xaxis_title="LB − impegnato (miliardi di €)",
    height=480,
    margin={"t": 30, "l": 10},
    yaxis=dict(categoryorder="array", categoryarray=gap["missione"].tolist()),
)
st.plotly_chart(fig, width="stretch")

st.caption(
    "Rosso: si è speso meno del previsto nella Legge di Bilancio. "
    "Verde: si è speso più del previsto."
)

# --- Tabella completa ---
st.subheader(f"Dettaglio per missione — {anno}")
st.dataframe(
    base.sort_values("Impegnato", ascending=False)[
        ["missione", "LB", "Prev. definitiva", "Impegnato", "Pagato", "Gap mld", "Gap %"]
    ].rename(columns={"missione": "Missione"}),
    width="stretch",
    hide_index=True,
)

st.info(
    "**Come leggere i numeri.** LB = previsioni iniziali della Legge di Bilancio. "
    "Previsione definitiva = bilancio dopo assestamento e variazioni. "
    "Impegnato = pagato + rimasto da pagare (consuntivo di competenza). "
    "Il pagato qui è la quota di competenza, non i pagamenti di cassa: quelli sono nella pagina Pagamenti."
)
