"""
Data Cleaning Demo — Contact List Cleaner
=========================================
Takes a messy contact export and produces a clean, deduplicated,
standardized spreadsheet. This is the kind of task buyers pay $50-150
for and that would take them hours by hand.

What it fixes:
  - Trims/normalizes whitespace and casing (names Title Case, emails lower)
  - Standardizes US phone numbers to (XXX) XXX-XXXX
  - Flags invalid emails and invalid/short phone numbers
  - Parses messy dates into a single ISO format (YYYY-MM-DD)
  - Removes duplicate people (same email OR same name+phone)
  - Drops rows with no usable contact info
  - Produces a short cleaning report

Usage:
    python clean_data.py
"""

import re
import pandas as pd

INPUT = "messy_contacts.csv"
OUTPUT_CSV = "output/clean_contacts.csv"
OUTPUT_XLSX = "output/clean_contacts.xlsx"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_name(value):
    if pd.isna(value):
        return ""
    # collapse internal whitespace, trim, title-case
    return re.sub(r"\s+", " ", str(value)).strip().title()


def clean_email(value):
    if pd.isna(value):
        return "", False
    email = str(value).strip().lower()
    return email, bool(EMAIL_RE.match(email))


def clean_phone(value):
    if pd.isna(value):
        return "", False
    digits = re.sub(r"\D", "", str(value))
    # strip leading US country code
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}", True
    return str(value).strip(), False  # keep original, flag invalid


def clean_date(value):
    if pd.isna(value):
        return ""
    parsed = pd.to_datetime(str(value).strip(), errors="coerce")
    return parsed.strftime("%Y-%m-%d") if pd.notna(parsed) else ""


def main():
    df = pd.read_csv(INPUT, dtype=str)
    rows_in = len(df)

    df["Full Name"] = df["Full Name"].apply(clean_name)

    emails = df["Email"].apply(clean_email)
    df["Email"] = [e for e, _ in emails]
    df["email_valid"] = [ok for _, ok in emails]

    phones = df["Phone"].apply(clean_phone)
    df["Phone"] = [p for p, _ in phones]
    df["phone_valid"] = [ok for _, ok in phones]

    df["Company"] = df["Company"].apply(
        lambda v: re.sub(r"\s+", " ", str(v)).strip().rstrip(".") if pd.notna(v) else ""
    )
    df["Signup Date"] = df["Signup Date"].apply(clean_date)

    # Drop rows with no name AND no valid email (junk rows)
    df = df[~((df["Full Name"] == "") & (~df["email_valid"]))]

    # Deduplicate: prefer rows with a valid email, then drop dup emails
    df = df.sort_values(by=["email_valid", "phone_valid"], ascending=False)
    df = df.drop_duplicates(subset=["Email"], keep="first")
    df = df.drop_duplicates(subset=["Full Name", "Phone"], keep="first")

    df = df.sort_values(by="Full Name").reset_index(drop=True)
    rows_out = len(df)

    df.to_csv(OUTPUT_CSV, index=False)
    df.to_excel(OUTPUT_XLSX, index=False)

    print("Cleaning report")
    print("=" * 40)
    print(f"Rows in:            {rows_in}")
    print(f"Rows out (clean):   {rows_out}")
    print(f"Removed (dupes/junk): {rows_in - rows_out}")
    print(f"Invalid emails flagged: {(~df['email_valid']).sum()}")
    print(f"Invalid phones flagged: {(~df['phone_valid']).sum()}")
    print(f"\nSaved -> {OUTPUT_CSV}")
    print(f"Saved -> {OUTPUT_XLSX}")
    print("\nCleaned data:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
