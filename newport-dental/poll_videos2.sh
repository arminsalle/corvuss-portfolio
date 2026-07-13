#!/bin/bash
jobs=(fe0a69ea-5bcf-4f71-be6b-841ff4dd4954 7be231e4-15c1-403b-8c07-948f64912423 b7d2c1a3-98ff-4adc-8d70-5a6198369e71)
names=(smile craft tech)
while true; do
  done=0; report=""
  for i in 0 1 2; do
    line=$(higgsfield generate get "${jobs[$i]}" 2>/dev/null | tail -1)
    st=$(echo "$line" | grep -oE 'completed|failed|nsfw|canceled' | head -1)
    url=$(echo "$line" | grep -oE 'https://[^ ]+' | head -1)
    if [ -n "$st" ]; then done=$((done+1)); report="$report ${names[$i]}:$st:$url"; fi
  done
  if [ "$done" -eq 3 ]; then echo "ALL_TERMINAL$report"; exit 0; fi
  sleep 25
done
