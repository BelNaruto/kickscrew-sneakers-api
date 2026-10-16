"""Export a brand collection (every product, every size, every price) to CSV.

Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data
Support (fastest): Telegram @pintoflow

    pip install requests
    RAPIDAPI_KEY=xxx python export_collection_csv.py nike 5   # first 5 pages
"""
import csv
import os
import re
import sys

import requests

HOST = "kickscrew-sneakers-data.p.rapidapi.com"
HEADERS = {"x-rapidapi-key": os.environ["RAPIDAPI_KEY"], "x-rapidapi-host": HOST}


def us_size(label):
    m = re.search(r"US\s*([\d.]+[YCK]?)", label or "")
    return m.group(1) if m else label


def main():
    collection = sys.argv[1] if len(sys.argv) > 1 else "nike"
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    out = f"{collection}_sizes_prices.csv"
    rows = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["product_id", "title", "vendor", "sku", "gender", "us_size", "price_usd", "available", "image", "url"])
        for page in range(1, max_pages + 1):
            r = requests.get(f"https://{HOST}/product/bycollection/v2", headers=HEADERS, timeout=90,
                             params={"collection": collection, "page": page, "perPage": 24, "currency": "USD"})
            r.raise_for_status()
            products = r.json()["data"]["products"]
            if not products:
                break
            for p in products:
                img = p["images"][0]["src"] if p.get("images") else ""
                url = f"https://www.kickscrew.com/products/{p['handle']}"
                for v in p["variants"]:
                    w.writerow([p["id"], p["title"], p["vendor"], v["sku"], v["option1"], us_size(v["option2"]),
                                v["price"], v["available"], img, url])
                    rows += 1
            print(f"page {page}: {len(products)} products")
    print(f"Saved {rows} size rows to {out}")


if __name__ == "__main__":
    main()
