"""Cosa promette lo Stato — la programmazione per obiettivi delle Note Integrative."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sources import (
    load_ni_azioni,
    load_ni_indicatori,
    load_ni_obiettivi,
    load_ni_priorita,
)

st.title("🎯 Cosa promette lo Stato")

st.caption(
    "Le **Note Integrative** sono il documento allegato al bilancio che spiega *perché* "
    "si spende: priorità politiche → obiettivi → indicatori con target. A rendiconto "
    "riportano anche il valore raggiunto. Per l'esito in euro vedi **Promesse vs Realtà**."
)

df_ind = load_ni_indicatori()
df_az = load_ni_azioni()
df_obj = load_ni_obiettivi()
df_pri = load_ni_priorita()

if df_ind.empty or df_az.empty:
    st.warning("Dati Note Integrative non disponibili.")
    st.stop()

anni = sorted(df_ind["anno"].dropna().unique().tolist())
if not anni:
    st.warning("Nessun anno disponibile.")
    st.stop()

anno = st.selectbox("Anno di bilancio", anni, index=len(anni) - 1)

rnd = df_ind[(df_ind["anno"] == anno) & (df_ind["fase"] == "RND")]
lb_ind = df_ind[(df_ind["anno"] == anno) & (df_ind["fase"] == "LB")]
lb_az = df_az[(df_az["anno"] == anno) & (df_az["fase"] == "LB")]

if rnd.empty:
    st.warning(f"Nessun dato di rendiconto per il {anno}.")
    st.stop()

# --- KPI: quanto è misurabile e quanto è stato centrato ---
n_ind = int(rnd["n_indicatori"].sum())
n_num = int(rnd["n_target_numerico"].sum())
n_confr = int(rnd["n_confrontabili"].sum())
n_ragg = int(rnd["n_target_raggiunto"].sum())
pct_num = 100 * n_num / n_ind if n_ind else 0
pct_ragg = 100 * n_ragg / n_confr if n_confr else 0
ministri = int(rnd["n_ministri_coperti"].max())

pri_anno = df_pri[(df_pri["anno"] == anno) & (df_pri["fase"] == "RND")]
n_pri = int(pri_anno["n_priorita"].sum())
n_pnrr = int(pri_anno["n_con_pnrr"].sum())
pct_pnrr = 100 * n_pnrr / n_pri if n_pri else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Indicatori dichiarati", f"{n_ind:,}", help=f"{ministri} amministrazioni")
c2.metric(
    "Con target numerico",
    f"{pct_num:.0f}%",
    help=f"{n_num:,} su {n_ind:,}: il resto è testo, intervallo o booleano",
)
c3.metric(
    "Target centrati",
    f"{pct_ragg:.0f}%",
    help=f"{n_ragg:,} su {n_confr:,} confrontabili (target e rendiconto numerici, stessa unità)",
    delta=f"{n_confr:,} confrontabili",
    delta_color="off",
)
c4.metric(
    "Priorità che citano il PNRR",
    f"{pct_pnrr:.0f}%",
    help=f"{n_pnrr} su {n_pri} priorità politiche",
)

st.caption(
    f"Anno {anno}: {ministri} amministrazioni coperte. La copertura non è uniforme tra anni "
    "e fasi: è esposta come `n_ministri_coperti` nei mart."
)

# --- Chi spende di più misura peggio ---
st.subheader("Chi spende di più, misura peggio?")

spesa = (
    lb_az.groupby("stp", as_index=False)["stanziamento_cp_mld"]
    .sum()
    .rename(columns={"stanziamento_cp_mld": "spesa_mld"})
)
fin = rnd.groupby("stp", as_index=False).agg(
    amministrazione=("amministrazione", "max"),
    n_indicatori=("n_indicatori", "sum"),
    pct_numeric=("pct_target_numerico", "mean"),
    pct_raggiunto=("pct_target_raggiunto", "mean"),
)

# Quota di indicatori "di realizzazione finanziaria": misurano la spesa, non il risultato.
fin_tipo = (
    rnd.assign(
        n_fin=lambda d: d["n_indicatori"].where(
            d["tipo_indicatore"].str.contains("finanziaria", na=False), 0
        )
    )
    .groupby("stp", as_index=False)
    .agg(n_ind=("n_indicatori", "sum"), n_fin=("n_fin", "sum"))
)
fin_tipo["pct_fin"] = (100 * fin_tipo["n_fin"] / fin_tipo["n_ind"].replace(0, pd.NA)).fillna(0)

scatter = spesa.merge(fin, on="stp", how="inner").merge(fin_tipo, on="stp", how="left")

if not scatter.empty:
    fig = go.Figure(
        go.Scatter(
            x=scatter["spesa_mld"],
            y=scatter["pct_fin"],
            mode="markers+text",
            text=scatter["amministrazione"].str.replace("MINISTERO ", "", regex=False).str.title(),
            textposition="top center",
            textfont={"size": 9},
            marker={
                "size": (scatter["n_ind"].fillna(0) ** 0.5) * 3,
                "color": scatter["pct_numeric"],
                "colorscale": "Blues",
                "showscale": True,
                "colorbar": {"title": "% target<br>numerico"},
                "line": {"width": 1, "color": "white"},
            },
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Spesa: € %{x:,.1f} mld<br>"
                "Indicatori finanziari: %{y:.0f}%<br>"
                "<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        xaxis_title="Stanziamento LB (miliardi di €)",
        yaxis_title="Indicatori che misurano spesa (%)",
        height=480,
        margin={"t": 20, "l": 10},
    )
    st.plotly_chart(fig, width="stretch")

    st.caption(
        "Ogni punto è un ministero. A destra ci sono i ministeri che spendono di più; "
        "in alto quelli i cui indicatori misurano l'avanzamento della spesa invece del risultato. "
        "Il colore è la quota di indicatori con target numerico: più chiaro, meno misurabile."
    )

# --- I target si auto-avverano? ---
st.subheader("Quali indicatori vengono centrati")

per_tipo = (
    rnd.groupby("tipo_indicatore", as_index=False)
    .agg(
        n=("n_indicatori", "sum"),
        confr=("n_confrontabili", "sum"),
        ragg=("n_target_raggiunto", "sum"),
    )
    .query("confr > 0")
)
per_tipo["pct"] = 100 * per_tipo["ragg"] / per_tipo["confr"]
per_tipo = per_tipo.sort_values("pct")

fig = go.Figure(
    go.Bar(
        x=per_tipo["pct"],
        y=per_tipo["tipo_indicatore"].str.replace("Indicatore di ", "", regex=False),
        orientation="h",
        marker_color="#3498db",
        text=[
            f"{p:.0f}%  ({r:,}/{c:,})"
            for p, r, c in zip(per_tipo["pct"], per_tipo["ragg"], per_tipo["confr"])
        ],
        textposition="outside",
    )
)
fig.update_layout(
    xaxis_title="Target centrati (%)",
    xaxis_range=[0, 108],
    height=300,
    margin={"t": 20, "l": 10},
)
st.plotly_chart(fig, width="stretch")

st.caption(
    "Gli indicatori «di realizzazione finanziaria» misurano quanto si è speso: "
    "centrarli è quasi tautologico. Gli indicatori di risultato (output) sono i più difficili."
)

# --- Il PNRR nel linguaggio della programmazione ---
st.subheader("Il PNRR nel linguaggio della programmazione")

pnrr = (
    df_pri[df_pri["fase"] == "RND"]
    .groupby("anno", as_index=False)
    .agg(n_priorita=("n_priorita", "sum"), n_pnrr=("n_con_pnrr", "sum"))
)
pnrr["pct"] = 100 * pnrr["n_pnrr"] / pnrr["n_priorita"].replace(0, pd.NA)

fig = go.Figure(
    go.Scatter(
        x=pnrr["anno"],
        y=pnrr["pct"],
        mode="lines+markers+text",
        text=[f"{p:.0f}%" if pd.notna(p) else "" for p in pnrr["pct"]],
        textposition="top center",
        line={"color": "#e67e22", "width": 3},
        marker={"size": 8},
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    )
)
fig.update_layout(
    xaxis_title="Anno di bilancio",
    yaxis_title="Priorità che citano il PNRR (%)",
    yaxis_range=[0, 40],
    height=320,
    margin={"t": 20},
)
st.plotly_chart(fig, width="stretch")

# --- Strategici vs strutturali ---
st.subheader("Obiettivi: politica o amministrazione?")

obj_lb = df_obj[(df_obj["anno"] == anno) & (df_obj["fase"] == "LB")]
if not obj_lb.empty:
    obj = (
        obj_lb.groupby(["amministrazione", "natura_obiettivo"], as_index=False)["n_obiettivi"]
        .sum()
        .pivot(index="amministrazione", columns="natura_obiettivo", values="n_obiettivi")
        .fillna(0)
    )
    obj["totale"] = obj.sum(axis=1)
    obj = obj.sort_values("totale", ascending=False).head(15)

    fig = go.Figure()
    for natura, colore in (("STRATEGICO", "#2980b9"), ("STRUTTURALE", "#95a5a6")):
        if natura in obj.columns:
            fig.add_bar(
                x=obj[natura],
                y=[a.replace("MINISTERO ", "").title() for a in obj.index],
                name=natura.title(),
                orientation="h",
                marker_color=colore,
            )
    fig.update_layout(
        barmode="stack",
        xaxis_title="Numero di obiettivi",
        height=460,
        margin={"t": 20, "l": 10},
        legend={"orientation": "h", "y": 1.02},
    )
    st.plotly_chart(fig, width="stretch")

    st.caption(
        "Strategico = politica pubblica di settore. Strutturale = attività continuativa "
        "dell'amministrazione. Un rapporto molto sbilanciato verso lo strutturale dice "
        "che la programmazione è soprattutto gestione ordinaria."
    )

# --- Dettaglio per amministrazione ---
st.subheader(f"Dettaglio per amministrazione — {anno}")

dettaglio = rnd.groupby("stp", as_index=False).agg(
    amministrazione=("amministrazione", "max"),
    indicatori=("n_indicatori", "sum"),
    target_numerico=("n_target_numerico", "sum"),
    confrontabili=("n_confrontabili", "sum"),
    centrati=("n_target_raggiunto", "sum"),
)
dettaglio["pct_target_numerico"] = (
    100 * dettaglio["target_numerico"] / dettaglio["indicatori"]
).round(1)
dettaglio["pct_centrati"] = (
    100 * dettaglio["centrati"] / dettaglio["confrontabili"].replace(0, pd.NA)
).round(1)
dettaglio = dettaglio.merge(
    spesa.rename(columns={"spesa_mld": "spesa_lb_mld"}), on="stp", how="left"
)

st.dataframe(
    dettaglio.sort_values("spesa_lb_mld", ascending=False)[
        [
            "amministrazione",
            "spesa_lb_mld",
            "indicatori",
            "pct_target_numerico",
            "confrontabili",
            "pct_centrati",
        ]
    ].rename(
        columns={
            "amministrazione": "Amministrazione",
            "spesa_lb_mld": "Spesa LB (mld)",
            "indicatori": "Indicatori",
            "pct_target_numerico": "% target numerico",
            "confrontabili": "Confrontabili",
            "pct_centrati": "% centrati",
        }
    ),
    width="stretch",
    hide_index=True,
)

st.info(
    "**Come leggere i numeri.** Il target è il valore dichiarato nella Legge di Bilancio; "
    "il confronto con il rendiconto è calcolato solo quando entrambi i valori sono numerici "
    'e nella stessa unità. I valori nella fonte sono testo libero (`">= 91%"`, `"3.020.000,00"`, '
    '`"SI"`, `"25% <= x <= 50%"`): intervalli, booleani e prosa restano nel testo originale '
    "e non entrano nel calcolo."
)
