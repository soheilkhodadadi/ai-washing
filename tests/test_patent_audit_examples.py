from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_patent_audit_examples.py"
_spec = importlib.util.spec_from_file_location("build_patent_audit_examples", SCRIPT_PATH)
assert _spec is not None and _spec.loader is not None
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)


def test_build_patent_audit_examples_flags_short_acronyms(tmp_path: Path) -> None:
    grant = tmp_path / "grant.csv"
    pregrant = tmp_path / "pregrant.csv"
    output = tmp_path / "audit.csv"

    pd.DataFrame(
        [
            {
                "cik": "1",
                "name": "TEST GRANT INC",
                "year": 2014,
                "patent_id": "G1",
                "patent_title": "Dosage in ML",
                "patent_abstract": "A pharmaceutical dosage measured in ML.",
                "matched_keywords": "ml",
            },
            {
                "cik": "2",
                "name": "MODEL GRANT INC",
                "year": 2024,
                "patent_id": "G2",
                "patent_title": "Machine learning controller",
                "patent_abstract": "A machine learning controller uses a neural network.",
                "matched_keywords": "machine learning | neural network",
            },
        ]
    ).to_csv(grant, index=False)

    pd.DataFrame(
        [
            {
                "cik": "3",
                "name": "TEST PREGRANT INC",
                "year": 2015,
                "application_id": "A1",
                "pgpub_id": "P1",
                "patent_id": "",
                "application_title": "AI enabled forecast",
                "application_abstract": "An AI enabled forecast with artificial intelligence.",
                "matched_keywords": "ai | artificial intelligence",
            },
            {
                "cik": "4",
                "name": "MODEL PREGRANT INC",
                "year": 2025,
                "application_id": "A2",
                "pgpub_id": "P2",
                "patent_id": "",
                "application_title": "Computer vision detector",
                "application_abstract": "A computer vision detector.",
                "matched_keywords": "computer vision",
            },
        ]
    ).to_csv(pregrant, index=False)

    frame = _module.build_audit_examples(
        grant_examples=grant,
        pregrant_examples=pregrant,
        output=output,
        per_lane=2,
    )

    assert output.exists()
    assert len(frame) == 4
    assert set(frame["source_lane"]) == {"grant", "pregrant"}
    flags = dict(zip(frame["record_id"], frame["keyword_review_flag"]))
    assert flags["G1"] == "short_acronym_only"
    assert flags["A1"] == "contains_short_acronym"
    assert "Short-acronym-only" in frame.loc[frame["record_id"] == "G1", "audit_note"].iloc[0]
