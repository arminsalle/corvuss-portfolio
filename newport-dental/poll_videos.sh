#!/bin/bash
jobs=(2cd822f6-586f-40c2-831c-5d77e930d5e5 98b913ea-3c45-4d56-9f8e-c255b29b0e28 48095ff1-403a-4f5c-9a72-f1d04d84f13a)
names=(ext int op)
while true; do
  done=0; report=""
  for i in 0 1 2; do
    line=$(higgsfield generate get "${jobs[$i]}" 2>/dev/null | tail -1)
    st=$(echo "$line" | grep -oE 'completed|failed|nsfw|canceled|queued|in_progress|processing' | head -1)
    url=$(echo "$line" | grep -oE 'https://[^ ]+' | head -1)
    report="$report ${names[$i]}:$st"
    case "$st" in completed|failed|nsfw|canceled) done=$((done+1)); report="$report $url";; esac
  done
  if [ "$done" -eq 3 ]; then echo "ALL_TERMINAL$report"; exit 0; fi
  sleep 25
done
