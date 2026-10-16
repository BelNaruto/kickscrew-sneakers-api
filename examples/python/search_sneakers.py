"""Search sneakers with pagination and print a table.

Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data
Support (fastest): Telegram @pintoflow

    pip install requests
    RAPIDAPI_KEY=xxx python search_sneakers.py "yeezy 350" 3
"""
import os
import sys

import requests

HOST = "kickscrew-sneakers-data.p.rapidapi.com"
HEADERS = {"x-rapidapi-key": os.environ["RAPIDAPI_KEY"], "x-rapidapi-host": HOST}


def search(query, page=1, per_page=16):
    r = requests.get(f"https://{HOST}/search/v2", headers=HEADERS, timeout=60, params={
        "query": query, "hitsPerPage": per_page, "page": page, "region": "US", "currency": "USD"})
    r.raise_for_status()
    return r.json()["data"]


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "yeezy 350"
    pages = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    n = 0
    for page in range(1, pages + 1):
        data = search(query, page)
        for p in data["products"]:
            n += 1
            sku = p["title"].split()[-1]
            print(f"{n:>3}. {p['title'][:70]:<70} {p['vendor']:<12} {sku}")
        if not data["pagination"]["hasNextPage"]:
            break
    print(f"\nTotal matching products: {data['pagination']['totalCount']}")


if __name__ == "__main__":
    main()
