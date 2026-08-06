"""Create lei_switzerland.csv from the GLEIF Golden Copy file.

The raw file is very big (about 5 GB unpacked), so it is read in chunks.
Only entities with legal address in Switzerland (country "CH") are kept.

Usage: python prepare_dataset.py --source <golden-copy-csv-zip>
"""

import argparse
import csv
import glob
import sys

import pandas as pd

# GLEIF column names -> short names used in the notebook
COLUMN_MAP = {
    "LEI": "lei",
    "Entity.LegalName": "legal_name",
    "Entity.LegalForm.EntityLegalFormCode": "legal_form_code",
    "Entity.EntityCategory": "entity_category",
    "Entity.EntityStatus": "entity_status",
    "Entity.LegalAddress.City": "city",
    "Entity.LegalAddress.PostalCode": "postal_code",
    "Registration.RegistrationStatus": "registration_status",
    "Registration.InitialRegistrationDate": "initial_registration_date",
    "Registration.LastUpdateDate": "last_update_date",
    "Registration.NextRenewalDate": "next_renewal_date",
    "Registration.ManagingLOU": "managing_lou",
}

COUNTRY_COLUMN = "Entity.LegalAddress.Country"
CHUNK_SIZE = 200_000


def find_default_source():
    """Look for the Golden Copy zip in the current directory.

    Stops the script with an error message if no file is found.
    """
    matches = glob.glob("*gleif-goldencopy-lei2-golden-copy.csv.zip")
    if not matches:
        sys.exit(
            "No GLEIF Golden Copy zip found. Download it from "
            "https://www.gleif.org/en/lei-data/gleif-golden-copy/"
            "download-the-golden-copy and pass the path with --source."
        )
    return matches[0]


def extract_swiss_entities(source_path):
    """Read the Golden Copy in chunks and return the Swiss entities.

    Keeps only the rows with country "CH" and the columns from
    COLUMN_MAP, renamed to the short names.
    """
    needed_columns = list(COLUMN_MAP) + [COUNTRY_COLUMN]
    chunks = []
    total_rows = 0
    kept_rows = 0

    reader = pd.read_csv(
        source_path,
        usecols=needed_columns,
        dtype=str,
        chunksize=CHUNK_SIZE,
    )
    for chunk in reader:
        total_rows += len(chunk)
        swiss = chunk[chunk[COUNTRY_COLUMN] == "CH"]
        if not swiss.empty:
            kept_rows += len(swiss)
            chunks.append(swiss[list(COLUMN_MAP)])
        print(f"processed {total_rows:,} rows, kept {kept_rows:,}")

    result = pd.concat(chunks, ignore_index=True)
    return result.rename(columns=COLUMN_MAP)


def main():
    """Run the extraction and write the output CSV."""
    parser = argparse.ArgumentParser(
        description="Filter the GLEIF Golden Copy to Swiss entities."
    )
    parser.add_argument(
        "--source",
        help="path to the GLEIF Golden Copy CSV zip",
    )
    parser.add_argument(
        "--output",
        default="lei_switzerland.csv",
        help="output CSV path (default: lei_switzerland.csv)",
    )
    args = parser.parse_args()

    source = args.source or find_default_source()
    print(f"Reading from: {source}")

    swiss = extract_swiss_entities(source)
    # legal names contain commas and quotes, so better quote all fields
    swiss.to_csv(
        args.output,
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL,
    )
    print(f"Wrote {len(swiss):,} rows and {swiss.shape[1]} columns "
          f"to {args.output}")


if __name__ == "__main__":
    main()
