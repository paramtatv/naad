#!/bin/sh
# Did the page that is live match the page in this checkout?
# Two instruments, because one was fooled before: a content grep matched a
# substring that survived between versions and reported a deploy that had not
# happened. The build stamp is a line that changes on every revision; the byte
# count is a second reading that does not depend on the first.
set -u
URL=${1:-https://paramtatv.github.io/naad/}
HERE=$(cd "$(dirname "$0")/.." && pwd)
LIVE=$(mktemp)
curl -fsSL --max-time 20 "$URL" -o "$LIVE" || { echo "RED could not fetch $URL" >&2; exit 2; }
stamp() { grep -o '<meta name="naad-build" content="[^"]*"' "$1"; }
ls_=$(stamp "$LIVE"); lh=$(stamp "$HERE/index.html")
bs=$(wc -c < "$LIVE" | tr -d ' '); bh=$(wc -c < "$HERE/index.html" | tr -d ' ')
rm -f "$LIVE"
if [ "$ls_" = "$lh" ] && [ "$bs" = "$bh" ]; then
  echo "OK live == local: $lh, $bh bytes"; exit 0
fi
echo "RED live stamp: ${ls_:-none}" >&2
echo "RED local stamp: $lh" >&2
echo "RED bytes live $bs vs local $bh" >&2
exit 1
