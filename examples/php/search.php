<?php
// Search sneakers with the KicksCrew Sneakers Data API (PHP + cURL)
// Get your key: https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data
// Support (fastest): Telegram @pintoflow
//
// RAPIDAPI_KEY=xxx php search.php "new balance 550"

$host  = 'kickscrew-sneakers-data.p.rapidapi.com';
$key   = getenv('RAPIDAPI_KEY') ?: die("Set RAPIDAPI_KEY\n");
$query = $argv[1] ?? 'new balance 550';

$url = "https://$host/search/v2?" . http_build_query([
    'query' => $query, 'hitsPerPage' => 10, 'page' => 1, 'region' => 'US', 'currency' => 'USD',
]);
$ch = curl_init($url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT        => 60,
    CURLOPT_HTTPHEADER     => ["x-rapidapi-key: $key", "x-rapidapi-host: $host"],
]);
$res = json_decode(curl_exec($ch), true);
curl_close($ch);

foreach ($res['data']['products'] ?? [] as $i => $p) {
    printf("%2d. %-70s %s\n    %s\n", $i + 1, $p['title'], $p['vendor'], $p['url']);
}
