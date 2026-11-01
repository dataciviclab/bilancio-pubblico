"""Promesse vs Realtà — Legge di Bilancio, previsione definitiva e consuntivo di competenza."""

import streamlit as st
import plotly.graph_objects as go

from sources import (
    load_lb_serie_missione,
    load_rnd_serie_missione,
    load_consuntivo_spese_missione,
)

st.title("⚖️ Promesse vs Realtà")

st.caption(
    "Confronto tra ciò che il governo ha stanziato nella Legge di Bilancio, "
    "la previsione definitiva e ciò che è stato effettivamente impegnato e pagato."
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
latest = anno

# --- Trend aggregato ---
st.subheader("Previsione vs realtà, anno per anno")

lb_tot = lb.groupby("anno", as_index=False)["cp_mld"].sum()
rnd_tot = rnd.groupby("anno", as_index=False)["cp_mld"].sum()
imp_tot = impegnato.groupby("anno", as_index=False)["totale_cp_mld"].sum()
pag_tot = pagato.groupby("anno", as_index=False)["pagato_cp_mld"].sum()

fig = go.Figure()
fig.add_trace(go.Scatter(x=lb_tot["anno"], y=lb_tot["cp_mld"], name="LB (previsione iniziale)", line=dict(color="#3498db", width=3)))
fig.add_trace(go.Scatter(x=rnd_tot["anno"], y=rnd_tot["cp_mld"], name="Previsione definitiva", line=dict(color="#f39c12", width=2, dash="dot")))
fig.add_trace(go.Scatter(x=imp_tot["anno"], y=imp_tot["totale_cp_mld"], name="Impegnato (consuntivo)", line=dict(color="#e74c3c", width=3)))
fig.add_trace(go.Scatter(x=pag_tot["anno"], y=pag_tot["pagato_cp_mld"], name="Pagato (consuntivo)", line=dict(color="#2ecc71", width=2)))
fig.update_layout(yaxis_title="Miliardi di €", height=400, margin={"t": 30}, legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig, width="stretch")

# --- KPI anno selezionato ---
def val(df, col, a):
    row = df[df["anno"] == a]
    return float(row[col].sum()) if not row.empty else 0.0


v_lb = val(lb_tot, "cp_mld", latest)
v_rnd = val(rnd_tot, "cp_mld", latest)
v_imp = val(imp_tot, "totale_cp_mld", latest)
v_pag = val(pag_tot, "pagato_cp_mld", latest)

c1, c2, c3, c4 = st.columns(4)
c1.metric("📋 LB (previsione)", f"€ {v_lb:,.0f} mld")
c2.metric("📅 Previsione definitiva", f"€ {v_rnd:,.0f} mld", delta=f"{v_rnd - v_lb:+,.0f} mld")
c3.metric("🧾 Impegnato", f"€ {v_imp:,.0f} mld", delta=f"{v_imp - v_rnd:+,.0f} mld")
c4.metric("💸 Pagato", f"€ {v_pag:,.0f} mld", delta=f"{(v_pag / v_imp - 1) * 100:+.1f}%" if v_imp else None)

# --- Per missione ---
st.subheader(f"Per missione — {latest}")

base = lb[lb["anno"] == latest][["missione", "cp_mld"]].rename(columns={"cp_mld": "LB"})
base = base.merge(rnd[rnd["anno"] == latest][["missione", "cp_mld"]].rename(columns={"cp_mld": "Prev. definitiva"}), on="missione", how="outer")
base = base.merge(impegnato[impegnato["anno"] == latest][["missione", "totale_cp_mld"]].rename(columns={"totale_cp_mld": "Impegnato"}), on="missione", how="outer")
base = base.merge(pagato[pagato["anno"] == latest][["missione", "pagato_cp_mld"]].rename(columns={"pagato_cp_mld": "Pagato"}), on="missione", how="outer")
base = base.fillna(0.0)

base["Gap LB→impegnato %"] = base.apply(
    lambda r: round((r["LB"] - r["Impegnato"]) / r["Impegnato"] * 100, 1) if r["Impegnato"] else None,
    axis=1,
)
base = base.sort_values("Impegnato", ascending=False)

top = base.head(12).iloc[::-1]
fig2 = go.Figure()
fig2.add_trace(go.Bar(y=top["missione"], x=top["LB"], name="LB", orientation="h", marker_color="#3498db"))
fig2.add_trace(go.Bar(y=top["missione"], x=top["Impegnato"], name="Impegnato", orientation="h", marker_color="#e74c3c"))
fig2.add_trace(go.Bar(y=top["missione"], x=top["Pagato"], name="Pagato", orientation="h", marker_color="#2ecc71"))
fig2.update_layout(barmode="group", xaxis_title="Miliardi di €", height=520, margin={"t": 30}, legend=dict(orientation="h", y=-0.12))
st.plotly_chart(fig2, width="stretch")

st.dataframe(
    base[["missione", "LB", "Prev. definitiva", "Impegnato", "Pagato", "Gap LB→impegnato %"]].rename(
        columns={"missione": "Missione"}
    ),
    width="stretch",
    hide_index=True,
)

st.info(
    "**Come leggere i numeri.** LB = previsioni iniziali della Legge di Bilancio. "
    "Previsione definitiva = bilancio dopo assestamento e variazioni. "
    "Impegnato = pagato + rimasto da pagare (consuntivo di competenza). "
    "Il pagato qui è la quota di competenza, non i pagamenti di cassa: quelli sono nella pagina Pagamenti."
)
