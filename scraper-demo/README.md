# 🕸️ Web Scraper — Book Catalog Extractor

A clean, production-style Python scraper that extracts a **full product catalog**
(1,000 items) from a website and delivers it as ready-to-use **CSV and Excel** files.

> **What this demonstrates:** the exact workflow I use for client scraping jobs —
> reliable pagination, structured field extraction, polite request handling, and
> clean spreadsheet output. The same approach adapts to e-commerce stores,
> directories, real-estate and job listings, marketplaces, and more.

---

## 📊 Sample Output

| title | price_gbp | rating | availability | url |
|-------|-----------|--------|--------------|-----|
| A Light in the Attic | 51.77 | 3 | In stock | https://books.toscrape.com/... |
| Sapiens: A Brief History of Humankind | 54.23 | 5 | In stock | https://books.toscrape.com/... |
| Sharp Objects | 47.82 | 4 | In stock | https://books.toscrape.com/... |

✅ **1,000 rows** scraped across 50 pages in seconds.
Full results: [`output/books.csv`](output/books.csv) · [`output/books.xlsx`](output/books.xlsx)

---

## ⚙️ How to run

```bash
pip install -r requirements.txt
python scraper.py            # scrape everything
python scraper.py --pages 3  # quick test: first 3 pages
```

---

## 🔧 Features

- **Pagination handling** — automatically walks every page until the catalog ends.
- **Structured extraction** — title, price, star rating (converted to 1–5), stock status, and product URL.
- **Polite scraping** — realistic User-Agent + request delays to avoid hammering servers.
- **Dual export** — CSV *and* Excel, ready for non-technical clients.
- **Robust parsing** — handles currency symbols and encoding quirks.

---

## 🛡️ Legal note

This demo targets [books.toscrape.com](https://books.toscrape.com), a sandbox
site **built specifically for scraping practice**. For client work I always
respect each site's Terms of Service and `robots.txt`.

---

*Want a scraper for your target site? I deliver clean data in 24–48h.*
