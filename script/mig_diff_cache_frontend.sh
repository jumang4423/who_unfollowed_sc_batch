if [ ! -f tmp/diff_cache.json ]; then
  echo "tmp/diff_cache.json not found"
  exit 1
fi
if [ ! -f tmp/followers_cache.json ]; then
  echo "tmp/followers_cache.json not found"
  exit 1
fi

cp tmp/diff_cache.json who_sc_follower_timeline/public/diff_cache.json
cp tmp/followers_cache.json who_sc_follower_timeline/public/followers_cache.json
