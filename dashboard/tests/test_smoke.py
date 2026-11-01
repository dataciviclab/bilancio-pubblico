"""Smoke test — verifica che tutte le pagine siano importabili ed eseguibili."""

from __future__ import annotations

import py_compile
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

DASHBOARD_DIR = Path(__file__).resolve().parents[1]
PAGES = sorted(DASHBOARD_DIR.glob("pages/*.py"))
ROOT_FILES = [DASHBOARD_DIR / "app.py", DASHBOARD_DIR / "sources.py"]

sys.path.insert(0, str(DASHBOARD_DIR))


@pytest.mark.smoke
@pytest.mark.parametrize("page", PAGES, ids=[p.name for p in PAGES])
def test_page_importable(page: Path) -> None:
    """Ogni pagina deve essere syntatticamente valida."""
    py_compile.compile(str(page), doraise=True)


@pytest.mark.smoke
@pytest.mark.parametrize("page", PAGES, ids=[p.name for p in PAGES])
def test_page_runs(page: Path) -> None:
    """Ogni pagina deve eseguire senza eccezioni sui dati reali."""
    at = AppTest.from_file(str(page), default_timeout=180)
    at.run()
    assert not at.exception, [str(e.value) for e in at.exception]


@pytest.mark.smoke
@pytest.mark.parametrize("root_file", ROOT_FILES, ids=[f.name for f in ROOT_FILES])
def test_root_file_importable(root_file: Path) -> None:
    """app.py e sources.py devono essere syntatticamente validi."""
    py_compile.compile(str(root_file), doraise=True)


@pytest.mark.smoke
def test_sources_data_loads() -> None:
    """Le funzioni dati devono restituire DataFrame non vuoti."""
    import sys
    sys.path.insert(0, str(DASHBOARD_DIR))
    from sources import (
        load_saldi_anno,
        load_composizione_spesa,
        load_entrate_anno,
        load_spese_missione,
        load_pagamenti_anno,
        load_costo_debito,
        load_lb_serie_anno,
        load_consuntivo_spese_anno,
        load_consuntivo_entrate_titolo,
    )
    assert not load_saldi_anno().empty, "saldi_anno vuoto"
    assert not load_composizione_spesa().empty, "composizione_spesa vuoto"
    assert not load_entrate_anno().empty, "entrate_anno vuoto"
    assert not load_spese_missione().empty, "spese_missione vuoto"
    assert not load_pagamenti_anno().empty, "pagamenti_anno vuoto"
    assert not load_costo_debito().empty, "costo_debito vuoto"
    assert not load_lb_serie_anno().empty, "lb_serie_anno vuoto"
    assert not load_consuntivo_spese_anno().empty, "consuntivo_spese_anno vuoto"
    assert not load_consuntivo_entrate_titolo().empty, "consuntivo_entrate_titolo vuoto"
