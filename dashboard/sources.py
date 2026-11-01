"""Data sources for the Bilancio Pubblico Intelligence dashboard.

Uses lab_connectors to read from GCS in production, local files in dev.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from lab_connectors.duckdb.queries import load_mart_flat, load_mart_table

PREFIX = "bilancio-pubblico/"


def _mart(slug: str, table: str, year: int | None = None) -> pd.DataFrame:
    """Load a single mart table via lab_connectors."""
    if year is None:
        return load_mart_flat(slug, table, prefix=PREFIX)
    return load_mart_table(slug, table, year, prefix=PREFIX)


def get_last_updated() -> str:
    """Best-effort last updated from GCS (or N/A)."""
    return "N/A"


# --- Saldi ---


@st.cache_data(ttl=3600, show_spinner=False)
def load_saldi_anno():
    return _mart("bdap_saldi_stato", "mart_saldi_anno", 2025)


@st.cache_data(ttl=3600, show_spinner=False)
def load_composizione_spesa():
    return _mart("bdap_spese_stato", "mart_investimenti_vs_corrente", 2025)


@st.cache_data(ttl=3600, show_spinner=False)
def load_avanzo_primario():
    return _mart("bdap_saldi_stato", "mart_avanzo_primario", 2025)


# --- Entrate ---


@st.cache_data(ttl=3600, show_spinner=False)
def load_entrate_anno():
    return _mart("bdap_entrate_stato", "mart_entrate_anno", 2025)


@st.cache_data(ttl=3600, show_spinner=False)
def load_entrate_titolo():
    return _mart("bdap_entrate_stato", "mart_entrate_titolo_natura_anno", 2025)


@st.cache_data(ttl=3600, show_spinner=False)
def load_trend_tributarie():
    return _mart("bdap_entrate_stato", "mart_trend_tributarie", 2025)


# --- Spese ---


@st.cache_data(ttl=3600, show_spinner=False)
def load_spese_missione():
    return _mart("bdap_spese_stato", "mart_spese_missione_anno", 2025)


@st.cache_data(ttl=3600, show_spinner=False)
def load_spese_anno():
    return _mart("bdap_spese_stato", "mart_spese_anno", 2025)


# --- Pagamenti ---


@st.cache_data(ttl=3600, show_spinner=False)
def load_pagamenti_anno():
    return _mart("bdap_pagamenti_stato", "mart_pagamenti_anno")


@st.cache_data(ttl=3600, show_spinner=False)
def load_costo_debito():
    return _mart("bdap_pagamenti_stato", "mart_costo_debito_bilancio")


@st.cache_data(ttl=3600, show_spinner=False)
def load_pagamenti_missione_anno():
    """Load all per-year pagamenti missioni and concatenate."""
    frames = []
    for year in range(2014, 2026):
        try:
            df = _mart(
                "bdap_pagamenti_stato", "mart_pagamenti_missione_categoria", year
            )
            if not df.empty:
                frames.append(df)
        except Exception:
            pass
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


# --- LB (Legge di Bilancio) ---


@st.cache_data(ttl=3600, show_spinner=False)
def load_lb_spese_anno():
    return _mart("bdap_lb_spese_missione", "mart_lb_spese_anno")


@st.cache_data(ttl=3600, show_spinner=False)
def load_lb_vs_rendiconto():
    return _mart("bdap_lb_spese_missione", "mart_lb_vs_rendiconto")


# --- Serie a tre stadi (DLB -> LB -> Rendiconto) ---


@st.cache_data(ttl=3600, show_spinner=False)
def load_dlb_serie_anno():
    return _mart("bdap_dlb_spese_serie", "mart_dlb_spese_anno", 2026)


@st.cache_data(ttl=3600, show_spinner=False)
def load_lb_serie_anno():
    return _mart("bdap_lb_spese_serie", "mart_lb_spese_anno", 2026)


@st.cache_data(ttl=3600, show_spinner=False)
def load_rnd_serie_anno():
    return _mart("bdap_rnd_spese_serie", "mart_rnd_spese_anno", 2025)


@st.cache_data(ttl=3600, show_spinner=False)
def load_dlb_serie_missione():
    return _mart("bdap_dlb_spese_serie", "mart_dlb_spese_missione", 2026)


@st.cache_data(ttl=3600, show_spinner=False)
def load_lb_serie_missione():
    return _mart("bdap_lb_spese_serie", "mart_lb_spese_missione", 2026)


@st.cache_data(ttl=3600, show_spinner=False)
def load_rnd_serie_missione():
    return _mart("bdap_rnd_spese_serie", "mart_rnd_spese_missione", 2025)


# --- Consuntivo (spese per capitolo, entrate per articolo) ---


def _concat_years(slug: str, table: str, years: range) -> pd.DataFrame:
    """Concatena una mart per anno (i consuntivi sono pubblicati un anno per volta)."""
    frames = []
    for year in years:
        try:
            df = _mart(slug, table, year)
            if not df.empty:
                frames.append(df)
        except Exception:
            pass
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_spese_anno():
    return _concat_years("bdap_rnd_spese_capitolo", "mart_anno", range(2011, 2026))


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_spese_missione():
    return _concat_years("bdap_rnd_spese_capitolo", "mart_missione", range(2011, 2026))


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_entrate_anno():
    return _concat_years("bdap_rnd_entrate_articolo", "mart_anno", range(2011, 2026))


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_entrate_titolo():
    return _concat_years("bdap_rnd_entrate_articolo", "mart_titolo", range(2011, 2026))
