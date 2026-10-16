"""Draw a price-by-size bar chart for any sneaker.

Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data
Support (fastest): Telegram @pintoflow

    pip install requests matplotlib
    RAPIDAPI_KEY=xxx python price_by_size_chart.py air-jordan-1-low-se-concord-dv1309-100
"""
import os
import re
import sys

import matplotlib.pyplot as plt
import requests

HOST = "kickscrew-sneakers-data.p.rapidapi.com"
HEADERS = {"x-rapidapi-key": os.environ["RAPIDAPI_KEY"], "x-rapidapi-host": HOST}

handle = sys.argv[1] if len(sys.argv) > 1 else "air-jordan-1-low-se-concord-dv1309-100"
d = requests.get(f"https://{HOST}/product/description/byslugs", headers=HEADERS,
                 params={"handle": handle, "country": "US"}, timeout=60).json()["data"]

sizes, prices, colors = [], [], []
for e in d["variants"]["edges"]:
    n = e["node"]
    price = float(n["price"]["amount"])
    if price <= 0:
        continue
    label = next(o["value"] for o in n["selectedOptions"] if o["name"] == "Size")
    m = re.search(r"US\s*([\d.]+[YCK]?)", label)
    sizes.append(m.group(1) if m else label)
    prices.append(price)
    colors.append("#16a34a" if n["availableForSale"] else "#cbd5e1")

plt.figure(figsize=(12, 5))
plt.bar(sizes, prices, color=colors)
plt.title(d["title"])
plt.xlabel("US size")
plt.ylabel("Price (USD)")
plt.ylim(0, sorted(prices)[int(len(prices) * 0.9)] * 1.3)  # hide extreme outliers
plt.tight_layout()
out = f"{handle}.png"
plt.savefig(out, dpi=150)
print("Saved", out, "(green = in stock)")
