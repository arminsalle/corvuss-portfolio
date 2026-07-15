#!/bin/bash
cd ~/vanson-site
i=0
while IFS= read -r url; do
  i=$((i+1))
  f="assets/products/p$(printf '%04d' $i).jpg"
  [ -s "$f" ] && continue
  curl -sL --max-time 30 -A "Mozilla/5.0" "$url" -o "$f" &
  if (( i % 12 == 0 )); then wait; fi
done < scrape/img-urls.txt
wait
echo "downloaded: $(ls assets/products | wc -l)"
