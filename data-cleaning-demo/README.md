# 🧹 Data Cleaning — Contact List Cleaner

Turns a **messy contact export** into a clean, deduplicated, standardized
spreadsheet — the kind of task that takes a human hours and that clients
happily pay $50–150 to make disappear.

> **What this demonstrates:** real-world data wrangling — normalization,
> validation, fuzzy deduplication, and date parsing — with a clear before/after
> and a cleaning report. Adapts to product lists, leads, survey data, exports
> from any CRM, etc.

---

## 📊 Before → After

**Before** ([`messy_contacts.csv`](messy_contacts.csv)) — 10 rows of chaos:
inconsistent casing, extra spaces, duplicate people, broken emails, phone
numbers in 5 different formats, dates in 4 different formats, empty junk rows.

**After** ([`output/clean_contacts.csv`](output/clean_contacts.csv)) — 6 clean rows:

| Full Name | Email | Phone | Company | Signup Date |
|-----------|-------|-------|---------|-------------|
| Alice Wong | alice.wong@gmail.com | (555) 666-7777 | Stark Industries | 2023-03-20 |
| Bob Brown | bob@company.io | (555) 444-5555 | Hooli | 2023-03-03 |
| Jane Doe | jane.doe@yahoo.com | (555) 987-6543 | Globex | 2023-01-06 |
| John Smith | john.smith@gmail.com | (555) 123-4567 | Acme Inc | 2023-01-05 |
| Mary Johnson | mary@example.com | (555) 222-3333 | Initech | 2023-02-14 |

```
Cleaning report
========================================
Rows in:              10
Rows out (clean):     6
Removed (dupes/junk): 4
Invalid emails flagged: 1
Invalid phones flagged: 1
```

---

## ⚙️ How to run

```bash
pip install -r requirements.txt
python clean_data.py
```

---

## 🔧 What it fixes

- **Whitespace & casing** — names → Title Case, emails → lowercase, trimmed.
- **Phone standardization** — any format → `(XXX) XXX-XXXX`, strips country codes.
- **Email validation** — flags malformed addresses instead of silently keeping them.
- **Date parsing** — `01/06/2023`, `2023/02/14`, `March 3 2023` → unified `YYYY-MM-DD`.
- **Deduplication** — removes duplicate people by email and by name+phone.
- **Junk removal** — drops rows with no usable contact info.
- **Cleaning report** — transparent summary of what changed.

---

*Got a messy spreadsheet? Send it over — I'll return it clean within 24h.*
