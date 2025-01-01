if (-Not (Test-Path "tmp/diff_cache.json")) {
  Write-Host "tmp/diff_cache.json not found"
  exit 1
}
if (-Not (Test-Path "tmp/followers_cache.json")) {
  Write-Host "tmp/followers_cache.json not found"
  exit 1
}

Copy-Item "tmp/diff_cache.json" "who_sc_follower_timeline/public/diff_cache.json"
Copy-Item "tmp/followers_cache.json" "who_sc_follower_timeline/public/followers_cache.json"
