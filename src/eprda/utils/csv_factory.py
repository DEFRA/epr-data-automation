# utils/csv_factory.py
from __future__ import annotations
from pathlib import Path
from typing import Iterable, Mapping, Tuple, Dict, List
import pandas as pd


# ---------- path helpers (works no matter where you run from) ----------
def _find_project_root(start: Path | None = None) -> Path:
    """
    Walk up from 'start' (or this file) until we find a directory that contains
    either 'templates' or 'pyproject.toml' or '.git'. Fallback to 3 parents up.
    """
    here = (start or Path(__file__).resolve()).parent
    for p in [here, *here.parents]:
        if (p / "templates").exists() or (p / "pyproject.toml").exists() or (p / ".git").exists():
            return p
    return here.parents[2]  # sensible fallback


PROJECT_ROOT = _find_project_root()
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "output"


# ---------- core factory ----------
def _load_template(template_csv: str | Path) -> Tuple[List[str], Dict[str, str]]:
    """
    Load CSV template header (column order) and first-row defaults (if present).
    All values are handled as strings; empty defaults become "".
    """
    tpl_path = Path(template_csv)
    if not tpl_path.exists():
        raise FileNotFoundError(f"Template not found: {tpl_path}")

    df = pd.read_csv(tpl_path, dtype=str, keep_default_na=False, nrows=1)
    columns = list(df.columns)

    if df.empty:
        base_row = {c: "" for c in columns}
    else:
        first = df.iloc[0].fillna("")
        base_row = {c: str(first[c]) for c in columns}

    return columns, base_row


def _build_dataframe(
    columns: List[str],
    base_row: Mapping[str, str],
    overrides_list: Iterable[Mapping[str, object]],
) -> pd.DataFrame:
    """
    Strictly build a DataFrame based on the template:
      - Only template columns allowed (raise on unknown keys)
      - Merge base_row with per-row overrides
      - Preserve exact template column order
      - Coerce all values to strings (None -> "")
    """
    colset = set(columns)
    rows: List[Dict[str, str]] = []

    for i, overrides in enumerate(overrides_list, start=1):
        unknown = set(overrides.keys()) - colset
        if unknown:
            raise ValueError(
                f"Row {i} contains unknown fields: {sorted(unknown)}. "
                f"Allowed fields: {columns}"
            )

        row = {c: "" if base_row.get(c) is None else str(base_row.get(c, "")) for c in columns}
        for k, v in overrides.items():
            row[k] = "" if v is None else str(v)
        rows.append(row)

    df = pd.DataFrame(rows, columns=columns).fillna("")
    # ensure dtype=str for all columns
    for c in columns:
        df[c] = df[c].astype(str)
    return df


def create_csv_from_template(
    template_csv: str | Path,
    output_csv: str | Path,
    rows: Iterable[Mapping[str, object]],
) -> Path:
    """
    Generate a CSV by:
      - Loading the template header (column order) and default row (if any)
      - Applying per-row overrides (strict: unknown fields raise)
      - Writing CSV with preserved column order and string values
    """
    columns, base_row = _load_template(template_csv)
    df = _build_dataframe(columns, base_row, rows)

    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")
    return out_path
