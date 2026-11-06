"""Data sources for the Bilancio Pubblico Intelligence dashboard.

Uses lab_connectors to read from GCS in production, local files in dev.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st
from lab_connectors.duckdb.queries import load_mart_flat, load_mart_table
from lab_connectors.registry import Registry, latest_published_year, load_registry

PREFIX = "bilancio-pubblico/"
_REGISTRY_PATH = Path(__file__).resolve().parents[1] / "registry" / "registry.json"


def _get_registry():
    """Registry committato (aggiornato dalla pipeline), o None se assente."""
    try:
        return load_registry(_REGISTRY_PATH)
    except (FileNotFoundError, ValueError):
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def published_year(slug: str) -> int:
    """Anno della partizione pubblicata per ``slug``.

    Ordine di risoluzione (in ``lab_connectors.registry``): registry → HEAD su
    GCS. Se non esiste ancora nessuna partizione si usa l'anno corrente (la
    pipeline pubblica sotto l'anno di esecuzione): hardcodarlo fa 404 al primo
    bump.
    """
    year = latest_published_year(_get_registry() or Registry(), slug, prefix=PREFIX)
    return year or date.today().year


def _mart(slug: str, table: str, year: int | None = None) -> pd.DataFrame:
    """Load a single mart table via lab_connectors.

    Prova prima il filesystem locale (``out/data`` rilevato da lab_connectors),
    poi ricade su GCS: in sviluppo l'output locale può essere parziale, mentre
    in cloud il locale non esiste e si legge direttamente dal bucket.
    ``fallback_remote`` gestisce il primo caso senza duplicare la query.
    """
    if year is None:
        return load_mart_flat(slug, table, prefix=PREFIX, fallback_remote=True)
    return load_mart_table(slug, table, year, prefix=PREFIX, fallback_remote=True)


@st.cache_data(ttl=3600, show_spinner=False)
def get_last_updated() -> str:
    """Ultimo anno pubblicato del consuntivo spese (dal registry)."""
    try:
        return str(published_year("bdap_rnd_spese_capitolo"))
    except Exception:
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
    return _mart("bdap_dlb_spese_serie", "mart_dlb_spese_anno", published_year("bdap_dlb_spese_serie"))


@st.cache_data(ttl=3600, show_spinner=False)
def load_lb_serie_anno():
    return _mart("bdap_lb_spese_serie", "mart_lb_spese_anno", published_year("bdap_lb_spese_serie"))


@st.cache_data(ttl=3600, show_spinner=False)
def load_rnd_serie_anno():
    return _mart("bdap_rnd_spese_serie", "mart_rnd_spese_anno", published_year("bdap_rnd_spese_serie"))


@st.cache_data(ttl=3600, show_spinner=False)
def load_dlb_serie_missione():
    return _mart("bdap_dlb_spese_serie", "mart_dlb_spese_missione", published_year("bdap_dlb_spese_serie"))


@st.cache_data(ttl=3600, show_spinner=False)
def load_lb_serie_missione():
    return _mart("bdap_lb_spese_serie", "mart_lb_spese_missione", published_year("bdap_lb_spese_serie"))


@st.cache_data(ttl=3600, show_spinner=False)
def load_rnd_serie_missione():
    return _mart("bdap_rnd_spese_serie", "mart_rnd_spese_missione", published_year("bdap_rnd_spese_serie"))


# --- Note Integrative (programmazione per obiettivi) ---


@st.cache_data(ttl=3600, show_spinner=False)
def load_ni_azioni():
    """Azioni di bilancio con stanziamento triennale e gestione (DLB/LB/RND)."""
    return _mart("bdap_ni_azioni", "mart_azioni_anno")


@st.cache_data(ttl=3600, show_spinner=False)
def load_ni_obiettivi():
    """Obiettivi strategici e strutturali delle amministrazioni (DLB/LB)."""
    return _mart("bdap_ni_obiettivi", "mart_obiettivi_anno")


@st.cache_data(ttl=3600, show_spinner=False)
def load_ni_indicatori():
    """Indicatori con target numerico e valore a rendiconto (DLB/LB/RND)."""
    return _mart("bdap_ni_indicatori", "mart_indicatori_anno")


@st.cache_data(ttl=3600, show_spinner=False)
def load_ni_priorita():
    """Priorità politiche dichiarate, con conteggio dei riferimenti al PNRR."""
    return _mart("bdap_ni_priorita", "mart_priorita_anno")


# --- Consuntivo (spese per capitolo, entrate per articolo) ---


def _concat_years(slug: str, table: str, first_year: int = 2011) -> pd.DataFrame:
    """Concatena una mart per anno (i consuntivi sono pubblicati un anno per volta)."""
    frames = []
    for year in range(first_year, published_year(slug) + 1):
        try:
            df = _mart(slug, table, year)
            if not df.empty:
                frames.append(df)
        except Exception:
            pass
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_spese_anno():
    return _concat_years("bdap_rnd_spese_capitolo", "mart_anno")


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_spese_missione():
    return _concat_years("bdap_rnd_spese_capitolo", "mart_missione")


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_entrate_anno():
    return _concat_years("bdap_rnd_entrate_articolo", "mart_anno")


@st.cache_data(ttl=3600, show_spinner=False)
def load_consuntivo_entrate_titolo():
    return _concat_years("bdap_rnd_entrate_articolo", "mart_titolo")
