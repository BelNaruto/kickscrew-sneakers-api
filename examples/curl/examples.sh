#!/usr/bin/env bash
# KicksCrew Sneakers Data API – cURL examples for every endpoint
# Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data
# Support (fastest): Telegram @pintoflow
set -euo pipefail
: "${RAPIDAPI_KEY:?Set RAPIDAPI_KEY first: export RAPIDAPI_KEY=your-key}"
HOST="kickscrew-sneakers-data.p.rapidapi.com"
H=(-H "x-rapidapi-key: $RAPIDAPI_KEY" -H "x-rapidapi-host: $HOST")
get() { echo "== $1"; curl -s "${H[@]}" "https://$HOST$2"; echo; echo; }

get "Search v2"                    "/search/v2?query=jordan%201&hitsPerPage=16&page=1&region=US&currency=USD"
get "Search v1"                    "/search?query=yeezy"
get "Details by handle (all sizes)" "/product/description/byslugs?handle=air-jordan-1-low-se-concord-dv1309-100&country=US"
get "Details by URL (all sizes)"   "/product/description?productUrl=https%3A%2F%2Fwww.kickscrew.com%2Fproducts%2Fair-jordan-1-low-se-concord-dv1309-100&country=US"
get "Details by model number"      "/description?modelNumber=DD9315-112"
get "Description by URL (v1)"      "/description/byurl?productUrl=https%3A%2F%2Fwww.kickscrew.com%2Fproducts%2Fair-jordan-1-low-se-concord-dv1309-100"
get "Recommendations"              "/product/recomendation?productId=7265091813571&currency=USD"
get "Review summary"               "/product/review/summary?productId=6997815525571"
get "Products by collection"       "/product/bycollection/v2?collection=nike&page=1&perPage=24&currency=USD"
get "Collection filters"           "/product/bycollection/v2/filters?collection=nike"
get "Brand collection"             "/brand-collection?brand=nike"
get "All collections (v4)"         "/api/v4/collections?page=1&perPage=35&country=US"
get "Search collections (v4)"      "/api/v4/collections/search?query=nike&perPage=45&page=1&country=US"
get "Collection product URLs (v4)" "/api/v4/collections/urls?collection=nike&page=1&perPage=24"
