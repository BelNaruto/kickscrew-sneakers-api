# Sneaker API: KicksCrew Sneakers Data (Prices by Size, Search, Collections, Product Details)

[![RapidAPI](https://img.shields.io/badge/RapidAPI-Subscribe-0055DA?logo=rapid&logoColor=white)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data)
[![Telegram](https://img.shields.io/badge/Support-@pintoflow-26A5E4?logo=telegram&logoColor=white)](https://t.me/pintoflow)
![Endpoints](https://img.shields.io/badge/endpoints-16-success)
![License](https://img.shields.io/badge/license-MIT-blue)

> 👟 **Get your API key:** **[KicksCrew Sneakers Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data)**
>
> 💬 **Support on Telegram: [@pintoflow](https://t.me/pintoflow)** — message us for the fastest response (questions, bugs, custom plans or new features).

A **sneaker API** for developers. Search sneakers from **KicksCrew** (Nike, Jordan, Adidas, Yeezy, New Balance, ASICS…) and get **titles, SKUs / style codes, images, availability and the price of every size**, browse **brand collections**, look up **product details by URL, handle or model number**, and get **product recommendations** — all as clean JSON.

Use it to build **sneaker price trackers, restock monitors, Discord / Telegram bots, resell price comparison tools, sneaker stores and dashboards**.

## Table of contents

- [Projects built with this API](#projects-built-with-this-api)
- [Use cases](#use-cases)
- [Examples in this repo](#examples-in-this-repo)
- [Quick start](#quick-start)
- [Endpoints](#endpoints)
- [Response examples](#response-examples)
- [Tips](#tips)
- [FAQ](#faq)
- [Support](#support)

## Projects built with this API

| Project | What it is |
|---|---|
| [**sneaker-price-tracker**](https://github.com/BelNaruto/sneaker-price-tracker) | Web app: search sneakers, price-by-size chart, watchlist with price history |
| [**sneaker-restock-monitor**](https://github.com/BelNaruto/sneaker-restock-monitor) | Python monitor that posts new drops, restocks and price drops to Discord |
| [**sneaker-price-telegram-bot**](https://github.com/BelNaruto/sneaker-price-telegram-bot) | Telegram bot: search a sneaker and get photos + the price of every size |

## Use cases

- **Sneaker price tracker** — record the price of each size over time and alert on drops.
- **Restock monitor** — detect new products and sizes coming back in stock, notify Discord / Telegram / Slack.
- **Resell & price comparison** — compare KicksCrew prices with StockX / GOAT / your own store.
- **Sneaker store / catalog** — import products, images and sizes into Shopify, WooCommerce or your own site.
- **Market research** — export whole brand collections (e.g. all `nike` or `jordan` products) to CSV.

## Examples in this repo

| Language | File | What it does |
|---|---|---|
| cURL | [`examples/curl/examples.sh`](examples/curl/examples.sh) | Every endpoint in one script |
| Node.js | [`examples/nodejs/search-and-sizes.js`](examples/nodejs/search-and-sizes.js) | Search a sneaker, then print the price of every size |
| Node.js | [`examples/nodejs/cheapest-in-my-size.js`](examples/nodejs/cheapest-in-my-size.js) | Find the cheapest in-stock pairs in **your** size |
| Python | [`examples/python/search_sneakers.py`](examples/python/search_sneakers.py) | Search with pagination and print a table |
| Python | [`examples/python/export_collection_csv.py`](examples/python/export_collection_csv.py) | Export a full brand collection (all sizes & prices) to CSV |
| Python | [`examples/python/price_by_size_chart.py`](examples/python/price_by_size_chart.py) | Draw a price-by-size bar chart (matplotlib) |
| PHP | [`examples/php/search.php`](examples/php/search.php) | Search sneakers with PHP cURL |

```bash
export RAPIDAPI_KEY="your-key-from-rapidapi"
```

## Quick start

```bash
curl --request GET \
  --url 'https://kickscrew-sneakers-data.p.rapidapi.com/search/v2?query=jordan%201&hitsPerPage=16&page=1&region=US&currency=USD' \
  --header 'x-rapidapi-host: kickscrew-sneakers-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: <YOUR_KEY>'
```

```js
const res = await fetch(
  'https://kickscrew-sneakers-data.p.rapidapi.com/search/v2?query=jordan%201&hitsPerPage=16&page=1&region=US&currency=USD',
  { headers: { 'x-rapidapi-key': process.env.RAPIDAPI_KEY, 'x-rapidapi-host': 'kickscrew-sneakers-data.p.rapidapi.com' } }
);
const { data } = await res.json();
data.products.forEach((p) => console.log(p.title, p.url));
```

## Endpoints

Base URL: `https://kickscrew-sneakers-data.p.rapidapi.com`

### Search

| Endpoint | Parameters | Returns |
|---|---|---|
| `GET /search/v2` | `query`*, `hitsPerPage` (16), `page` (1), `sortBy`, `region` (US), `currency` (USD) | `data.products[]` (id, title, vendor, handle, url, image_url, images, priceRange, variants, tags) + `data.pagination { totalCount, page, hasNextPage }` |
| `GET /search` | `query`* | Search results (v1) |

### Product details

| Endpoint | Parameters | Returns |
|---|---|---|
| `GET /product/description` | `productUrl`*, `country` (US) | Full product: title, description, vendor, images, **every size with its price and availability** (`variants.edges[].node`) |
| `GET /product/description/byslugs` | `handle`*, `country` | Same as above, using the product `handle` from search results |
| `GET /description/byurl` | `productUrl`* | Product description by URL (v1) |
| `GET /description` | `modelNumber`* (e.g. `DD9315-112`) | Product by style code / model number |
| `GET /product/recomendation` | `productId`*, `currency` | Similar / recommended sneakers (prices in **cents**) |
| `GET /product/review/summary` | `productId`* | Review summary |

### Collections & brands

| Endpoint | Parameters | Returns |
|---|---|---|
| `GET /product/bycollection/v2` | `collection`* (e.g. `nike`), `page`*, `perPage`*, `currency` | `data.products[]` with all variants (size, price, available) + `currentPage` (request the next `page` until `products` is empty) |
| `GET /product/bycollection/v2/filters` | `collection`* | Available filters for a collection |
| `GET /brand-collection` | `brand`* | Products of a brand |
| `GET /api/v4/collections` | `page`, `perPage`, `country` | All collections |
| `GET /api/v4/collections/search` | `query`*, `page`, `perPage`, `country` | Search collections by name |
| `GET /api/v4/collections/urls` | `collection`*, `page`, `perPage` | Product URLs of a collection |
| `GET /api/v3/collections`, `GET /api/collections/v3/search` | `page`, `perPage`, `query`, `refresh` | Collections (v3, kept for older integrations) |

\* required

## Response examples

Real (trimmed) responses.

**`GET /search/v2?query=jordan 1`**

```json
{
  "success": true,
  "data": {
    "products": [
      {
        "id": "7513870336195",
        "title": "Air Jordan 1 Low SE 'Concord' DV1309-100",
        "vendor": "Jordan",
        "availableForSale": true,
        "productType": "Sneakers",
        "handle": "air-jordan-1-low-se-concord-dv1309-100",
        "priceRange": {
          "minVariantPrice": { "amount": "0.0", "currencyCode": "USD" },
          "maxVariantPrice": { "amount": "2771.73", "currencyCode": "USD" }
        },
        "currency": "USD",
        "image_url": "https://cdn.shopify.com/s/files/1/0603/3031/1875/files/main-square_59eff6ce-58b6-415f-a737-e16fa518ec60.jpg",
        "url": "https://www.kickscrew.com/products/air-jordan-1-low-se-concord-dv1309-100"
      }
    ],
    "pagination": { "totalCount": 1000, "page": 1, "hasNextPage": true }
  },
  "message": null
}
```

**`GET /product/description/byslugs?handle=air-jordan-1-low-se-concord-dv1309-100`** — one entry per size:

```json
{
  "data": {
    "title": "Air Jordan 1 Low SE 'Concord' DV1309-100",
    "vendor": "Jordan",
    "variants": {
      "edges": [
        {
          "node": {
            "sku": "DV1309-100-95",
            "availableForSale": true,
            "selectedOptions": [
              { "name": "Gender", "value": "MENS" },
              { "name": "Size", "value": "Men's US 9.5 / Women's US 11 / UK 8.5 / EU 43 / JP 27.5" }
            ],
            "price": { "amount": "115.83", "currencyCode": "USD" }
          }
        }
      ]
    },
    "images": { "edges": [ { "node": { "url": "https://cdn.shopify.com/s/files/1/0603/3031/1875/files/main-square_59eff6ce-58b6-415f-a737-e16fa518ec60.jpg" } } ] }
  }
}
```

**`GET /product/bycollection/v2?collection=nike&page=1&perPage=24`**

```json
{
  "status": "success",
  "data": {
    "products": [
      {
        "id": 8050079039683,
        "title": "Nike Zoom Kobe 5 Protro 'X-Ray' HJ4303-400",
        "vendor": "Nike",
        "variants": [
          { "option1": "MENS", "option2": "Men's US 3.5 / Women's US 5 / UK 3 / EU 35.5 / JP 22.5", "sku": "HJ4303-400-35", "available": true, "price": "366.21" }
        ],
        "images": [ { "src": "https://cdn.shopify.com/s/files/1/0603/3031/1875/files/..." } ]
      }
    ],
    "currentPage": 1
  }
}
```

## Tips

- **Search gives the list, details give the sizes.** `/search/v2` returns one variant per product; call `/product/description/byslugs?handle=…` to get every size and its price.
- **A price of `0.0` means "no offer"** for that size. Filter `price > 0` and `availableForSale === true` to get buyable sizes.
- **`priceRange.minVariantPrice` can be `0.0`** for the same reason — compute the "from" price from the sizes instead.
- **Recommendations return prices in cents** (`38493` = `$384.93`).
- **Size labels contain all systems** (`Men's US 9.5 / Women's US 11 / UK 8.5 / EU 43 / JP 27.5`) — parse the part you need.
- **Cache product details** for a few minutes; prices change, but not every second.
- **Keep your key on the server.** Don't embed your RapidAPI key in a public website or app.

## FAQ

**Which brands are covered?** Everything sold on KicksCrew — Nike, Jordan, Adidas, Yeezy, New Balance, ASICS, Converse, Vans, Puma, Salomon and more. Use `/api/v4/collections/search?query=…` to find a collection slug.

**Which currency / country?** Pass `currency=USD` (and `region` / `country=US`). Other currencies are supported via the same parameters.

**How do I get the price for my size?** See [`examples/nodejs/cheapest-in-my-size.js`](examples/nodejs/cheapest-in-my-size.js).

---

## Support

💬 **Need help? Contact us on Telegram: [@pintoflow](https://t.me/pintoflow)** for the fastest response.

**Subscribe / get your key:** [https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data)

## Keywords

sneaker API, sneakers API, KicksCrew API, sneaker price API, sneaker price tracker, sneaker restock monitor, Nike API, Jordan API, Yeezy API, Adidas API, shoe price API, sneaker size price, sneaker database, sneaker scraper alternative, StockX API alternative, GOAT API alternative.

## License

Example code: MIT. Use of the API is subject to the [RapidAPI terms](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data). Not affiliated with KicksCrew.
