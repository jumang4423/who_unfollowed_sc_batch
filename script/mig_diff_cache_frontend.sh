# check if the diff_cache.json exists
if [ ! -f tmp/diff_cache.json ]; then
  echo "tmp/diff_cache.json not found"
  exit 1
fi

cp tmp/diff_cache.json who_sc_follower_timeline/public/diff_cache.json
