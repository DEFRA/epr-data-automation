# utils/create_pom_file.py
from __future__ import annotations
import argparse
from pathlib import Path

from eprda.utils.csv_factory import create_csv_from_template, TEMPLATES_DIR, OUTPUT_DIR


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a POM CSV from the template.")
    parser.add_argument(
        "--org-id",
        required=True,
        help="Organisation ID to populate (e.g., ORG-1001)",
    )
    args = parser.parse_args()

    template = TEMPLATES_DIR / "pom-file-template.csv"   # keep your template here
    output = OUTPUT_DIR / f"pom_{args.org_id}.csv"      # generated file

    rows = [
        {
            "organisation_id": args.org_id,  # only org_id for now (extend later)
        }
    ]

    written = create_csv_from_template(template_csv=template, output_csv=output, rows=rows)
    print(f"✅ POM CSV created: {written.resolve()}")


if __name__ == "__main__":
    main()
