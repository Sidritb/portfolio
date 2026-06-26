"""
Web Scraper Demo — Book Catalog Extractor
==========================================
Scrapes a full product catalog (title, price, rating, availability, URL)
and exports it to both CSV and Excel.

Target: https://books.toscrape.com  — a sandbox site built specifically
for scraping practice, so this demo is 100% legal and safe to showcase.

This is a portfolio sample. The same approach adapts to e-commerce sites,
directories, real-estate listings, job boards, etc.

Usage:
    python scraper.py            # scrape all pages
    python scraper.py --pages 3  # scrape first 3 pages only
"""

import argparse
import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = urljoin(BASE_URL, "catalogue/page-{}.html")

# Map the site's word-based rating classes to integers (1-5).
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def parse_book(card):
    """Extract a single book's fields from its HTML card."""
    title = card.h3.a["title"].strip()

    price_text = card.select_one("p.price_color").get_text(strip=True)
    # Strip currency symbol / stray chars, keep the number.
    price = float(price_text.replace("£", "").replace("Â", "").strip())

    rating_class = card.select_one("p.star-rating")["class"]
    rating_word = next((c for c in rating_class if c in RATING_MAP), None)
    rating = RATING_MAP.get(rating_word, 0)

    availability = card.select_one("p.instock.availability").get_text(strip=True)

    relative_url = card.h3.a["href"]
    url = urljoin(CATALOGUE_URL.format(1), relative_url)

    return {
        "title": title,
        "price_gbp": price,
        "rating": rating,
        "availability": availability,
        "url": url,
    }


def scrape(max_pages=None, delay=0.5):
    """Scrape book cards across paginated catalogue pages."""
    books = []
    page = 1

    while True:
        if max_pages and page > max_pages:
            break

        resp = requests.get(CATALOGUE_URL.format(page), headers=HEADERS, timeout=15)
        if resp.status_code == 404:
            break  # ran past the last page
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("article.product_pod")
        if not cards:
            break

        for card in cards:
            books.append(parse_book(card))

        print(f"  page {page:>2}: +{len(cards)} books (total {len(books)})")
        page += 1
        time.sleep(delay)  # be polite to the server

    return books


def export(books, csv_path, xlsx_path):
    """Write results to CSV and Excel."""
    df = pd.DataFrame(books)
    df.to_csv(csv_path, index=False, quoting=csv.QUOTE_MINIMAL)
    df.to_excel(xlsx_path, index=False)
    return df


def main():
    parser = argparse.ArgumentParser(description="Scrape the book catalog.")
    parser.add_argument("--pages", type=int, default=None,
                        help="Limit number of pages (default: all).")
    args = parser.parse_args()

    print("Scraping books.toscrape.com ...")
    books = scrape(max_pages=args.pages)

    csv_path = "output/books.csv"
    xlsx_path = "output/books.xlsx"
    df = export(books, csv_path, xlsx_path)

    print(f"\nDone. Scraped {len(df)} books.")
    print(f"  -> {csv_path}")
    print(f"  -> {xlsx_path}")
    print("\nPreview:")
    print(df.head(8).to_string(index=False))


if __name__ == "__main__":
    main()
