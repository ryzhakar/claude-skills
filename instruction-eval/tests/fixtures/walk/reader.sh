#!/bin/sh
cat >/dev/null
apologies=$(grep -oi sorry "$1" | wc -l | tr -d ' ')
while [ "$apologies" -gt 0 ]; do
  printf 'Sorry. '
  apologies=$((apologies - 1))
done
echo 'Answer: 42.'
