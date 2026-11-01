"""Consuntivo — cosa è stato impegnato, pagato e incassato."""

import streamlit as st
import plotly.graph_objects as go

from sources import (
    load_consuntivo_spese_anno,
    load_consuntivo_spese_missione,
    load_consuntivo_entrate_anno,
    load_consuntivo_entrate_titolo,
)

st.title("🧾 Consuntivo")

spese = load_consuntivo_spese_anno()
missioni = load_consuntivo_spese_missione()
entrate = load_consuntivo_entrate_anno()
titoli = load_consuntivo_entrate_titolo()

if spese.empty:
    st.warning("Consuntivo spese non disponibile.")
    st.stop()

anni = sorted(spese["anno"].dropna().astype(int).unique().tolist())
anno = st.selectbox("Anno", anni, index=len(anni) - 1)
row = spese[spese["anno"] == anno].iloc[0]

# --- KPI ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Previsione definitiva", f"€ {row['prev_def_cp_mld']:,.0f} mld")
tasso_pag = (row["pagato_cp_mld"] / row["prev_def_cp_mld"] * 100) if row["prev_def_cp_mld"] else 0
c2.metric("Pagato (competenza)", f"€ {row['pagato_cp_mld']:,.0f} mld", delta=f"{tasso_pag:.1f}% della previsione")
c3.metric("Residui da pagare", f"€ {row['rimasto_cp_mld']:,.0f} mld")
c4.metric("Economie di spesa", f"€ {abs(row['economie_cp_mld']):,.0f} mld")

# --- Trend spese ---
st.subheader("Spese: pagato, residui ed economie")
fig = go.Figure()
fig.add_trace(go.Bar(x=spese["anno"], y=spese["pagato_cp_mld"], name="Pagato", marker_color="#2ecc71"))
fig.add_trace(go.Bar(x=spese["anno"], y=spese["rimasto_cp_mld"], name="Residui da pagare", marker_color="#e67e22"))
fig.add_trace(go.Scatter(x=spese["anno"], y=spese["prev_def_cp_mld"], name="Previsione definitiva", line=dict(color="#3498db", width=3)))
fig.update_layout(barmode="stack", yaxis_title="Miliardi di €", height=420, margin={"t": 30}, legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig, width="stretch")

# --- Missioni con più residui ---
st.subheader(f"Missioni con più residui — {anno}")
mm = missioni[missioni["anno"] == anno].sort_values("rimasto_cp_mld", ascending=False).head(12).iloc[::-1]
fig2 = go.Figure()
fig2.add_trace(go.Bar(y=mm["missione"], x=mm["pagato_cp_mld"], name="Pagato", orientation="h", marker_color="#2ecc71"))
fig2.add_trace(go.Bar(y=mm["missione"], x=mm["rimasto_cp_mld"], name="Residui", orientation="h", marker_color="#e67e22"))
fig2.update_layout(barmode="stack", xaxis_title="Miliardi di €", height=480, margin={"t": 30}, legend=dict(orientation="h", y=-0.12))
st.plotly_chart(fig2, width="stretch")

# --- Entrate ---
if not entrate.empty:
    st.subheader("Entrate: accertato e versato")
    e = entrate[entrate["anno"] == anno].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Accertato", f"€ {e['totale_cp_mld']:,.0f} mld")
    c2.metric("Versato", f"€ {e['versato_cp_mld']:,.0f} mld")
    c3.metric("Da riscuotere", f"€ {e['rimasto_riscuotere_cp_mld']:,.0f} mld")

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=entrate["anno"], y=entrate["totale_cp_mld"], name="Accertato", line=dict(color="#9b59b6", width=3)))
    fig3.add_trace(go.Scatter(x=entrate["anno"], y=entrate["versato_cp_mld"], name="Versato", line=dict(color="#3498db", width=3)))
    fig3.add_trace(go.Scatter(x=entrate["anno"], y=entrate["prev_def_cp_mld"], name="Previsione definitiva", line=dict(color="#f39c12", width=2, dash="dot")))
    fig3.update_layout(yaxis_title="Miliardi di €", height=380, margin={"t": 30}, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig3, width="stretch")

    if not titoli.empty:
        tt = titoli[titoli["anno"] == anno].sort_values("totale_cp_mld", ascending=False)
        st.dataframe(
            tt[["titolo", "prev_def_cp_mld", "totale_cp_mld", "versato_cp_mld", "rimasto_riscuotere_cp_mld"]].rename(
                columns={
                    "titolo": "Titolo",
                    "prev_def_cp_mld": "Previsione",
                    "totale_cp_mld": "Accertato",
                    "versato_cp_mld": "Versato",
                    "rimasto_riscuotere_cp_mld": "Da riscuotere",
                }
            ),
            width="stretch",
            hide_index=True,
        )
        st.caption("Il Titolo IV (accensione di prestiti) è una partita finanziaria, non un'entrata corrente.")

st.info(
    "Qui il 'pagato' è la quota di competenza del rendiconto per capitolo. "
    "I pagamenti di cassa (OP/RSF) sono nella pagina Pagamenti e possono differire."
)
