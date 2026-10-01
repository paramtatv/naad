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
# figures.json ships beside the page and a push can change it alone, which
# the page's stamp cannot see: compare it by checksum too.
FJ=$(mktemp); curl -fsSL --max-time 20 "${URL%/}/figures.json" -o "$FJ" || { echo "RED could not fetch figures.json" >&2; exit 2; }
fl=$(md5 -q "$FJ" 2>/dev/null || md5sum "$FJ" | cut -c1-32); fh=$(md5 -q "$HERE/figures.json" 2>/dev/null || md5sum "$HERE/figures.json" | cut -c1-32)
rm -f "$FJ"
if [ "$ls_" = "$lh" ] && [ "$bs" = "$bh" ] && [ "$fl" = "$fh" ]; then
  echo "OK live == local: $lh, $bh bytes; figures.json md5 $fh"; exit 0
fi
[ "$fl" = "$fh" ] || echo "RED figures.json live md5 $fl vs local $fh" >&2
echo "RED live stamp: ${ls_:-none}" >&2
echo "RED local stamp: $lh" >&2
echo "RED bytes live $bs vs local $bh" >&2
exit 1
