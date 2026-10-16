// Find the cheapest in-stock sneakers in YOUR size (Node.js 18+, no dependencies)
// Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data
// Support (fastest): Telegram @pintoflow
//
// Usage: RAPIDAPI_KEY=xxx node cheapest-in-my-size.js "dunk low" 10

const HOST = 'kickscrew-sneakers-data.p.rapidapi.com';
const headers = { 'x-rapidapi-key': process.env.RAPIDAPI_KEY, 'x-rapidapi-host': HOST };
const api = async (path, params) =>
  (await fetch(`https://${HOST}${path}?${new URLSearchParams(params)}`, { headers })).json();

const query = process.argv[2] || 'dunk low';
const mySize = process.argv[3] || '10';

(async () => {
  const { data } = await api('/search/v2', { query, hitsPerPage: 16, page: 1, region: 'US', currency: 'USD' });

  // Fetch details for each result in parallel (small batches are friendlier to your quota)
  const results = await Promise.all(
    data.products.map(async (p) => {
      const d = await api('/product/description/byslugs', { handle: p.handle, country: 'US' });
      const match = (d.data?.variants?.edges || [])
        .map((e) => e.node)
        .find((n) => {
          const size = n.selectedOptions.find((o) => o.name === 'Size')?.value || '';
          return new RegExp(`(^|Men's )US ${mySize.replace('.', '\\.')}( |$)`).test(size) && n.availableForSale && Number(n.price.amount) > 0;
        });
      return match && { title: p.title, price: Number(match.price.amount), url: p.url };
    })
  );

  const found = results.filter(Boolean).sort((a, b) => a.price - b.price);
  console.log(`Cheapest "${query}" in US ${mySize}:\n`);
  found.forEach((r, i) => console.log(`${String(i + 1).padStart(2)}. $${r.price.toFixed(2).padStart(8)}  ${r.title}\n     ${r.url}`));
  if (!found.length) console.log('Nothing in stock in that size — try another query.');
})();
