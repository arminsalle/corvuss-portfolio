#!/bin/bash
names=(botox cosmetic implants dentures emergency ortho perio sleep)
jobs=(681985aa-1b04-4093-9cfc-92c8497fa55d 4ee0502d-e655-4e62-829e-396cf41d18c0 ebdc9aad-ba77-4fcf-8d9c-a1e8579f1b4d e624a7d8-07c6-45aa-9ffd-71b21046ed8a bd4fddb3-ceac-4ff7-8150-7ac43ae95caf 86aca846-e242-446c-af30-5d43e3dc6a90 66021f88-6efc-4eeb-bc57-f39b3cfb8a08 1d6695e6-cd36-403c-810e-5e55368690c3)
while true; do
  done=0; report=""
  for i in 0 1 2 3 4 5 6 7; do
    line=$(higgsfield generate get "${jobs[$i]}" 2>/dev/null | tail -1)
    st=$(echo "$line" | grep -oE 'completed|failed|nsfw|canceled' | head -1)
    url=$(echo "$line" | grep -oE 'https://[^ ]+' | head -1)
    if [ -n "$st" ]; then done=$((done+1)); report="$report ${names[$i]}:$st:$url"; fi
  done
  if [ "$done" -eq 8 ]; then echo "ALL_TERMINAL$report"; exit 0; fi
  sleep 30
done
