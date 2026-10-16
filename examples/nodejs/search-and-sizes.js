// Search a sneaker and print the price of every size (Node.js 18+, no dependencies)
// Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data
// Support (fastest): Telegram @pintoflow
//
// Usage: RAPIDAPI_KEY=xxx node search-and-sizes.js "jordan 1 low concord"

const HOST = 'kickscrew-sneakers-data.p.rapidapi.com';
const headers = { 'x-rapidapi-key': process.env.RAPIDAPI_KEY, 'x-rapidapi-host': HOST };

async function api(path, params) {
  const url = `https://${HOST}${path}?${new URLSearchParams(params)}`;
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}

// "Men's US 9.5 / Women's US 11 / UK 8.5 / EU 43 / JP 27.5" -> "US 9.5"
const usSize = (label = '') => (label.match(/US\s*([\d.]+[YCK]?)/) || [, label])[1];

(async () => {
  const query = process.argv[2] || 'jordan 1 low concord';
  const { data } = await api('/search/v2', { query, hitsPerPage: 5, page: 1, region: 'US', currency: 'USD' });
  if (!data.products.length) return console.log('No results');

  data.products.forEach((p, i) => console.log(`${i + 1}. ${p.title}  (${p.vendor})`));

  const top = data.products[0];
  const details = await api('/product/description/byslugs', { handle: top.handle, country: 'US' });
  const sizes = details.data.variants.edges
    .map(({ node }) => ({
      gender: node.selectedOptions.find((o) => o.name === 'Gender')?.value,
      size: usSize(node.selectedOptions.find((o) => o.name === 'Size')?.value),
      price: Number(node.price.amount),
      inStock: node.availableForSale,
    }))
    .filter((s) => s.price > 0);

  console.log(`\n${details.data.title}\n${top.url}\n`);
  console.table(sizes.map((s) => ({ size: s.size, gender: s.gender, price: `$${s.price.toFixed(2)}`, inStock: s.inStock ? '✅' : '—' })));

  const cheapest = sizes.filter((s) => s.inStock).sort((a, b) => a.price - b.price)[0];
  if (cheapest) console.log(`Cheapest in-stock size: US ${cheapest.size} at $${cheapest.price.toFixed(2)}`);
})().catch((e) => { console.error(e.message); process.exit(1); });
