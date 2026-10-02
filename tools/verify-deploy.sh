#!/bin/sh
# Did the page that is live match the page in this checkout?
# Two instruments, because one was fooled before: a content grep matched a
# substring that survived between versions and reported a deploy that had not
# happened. The build stamp is a line that changes on every revision; the byte
# count is a second reading that does not depend on the first.
# Since r45 a third: every tracked file is compared with what the site serves.
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
  # Third instrument, only once the stamp agrees: EVERY tracked file, because a push can
  # change kernel/, an image or a font alone and neither the stamp nor figures.json sees
  # it. Files up to 2 MB are compared by checksum; larger ones (the audio) by the length
  # the server reports, or by checksum too when FULL=1. A file the site does not serve
  # is RED: the page's own check already refuses a reference to a file not in the tree.
  sum() { md5 -q "$1" 2>/dev/null || md5sum "$1" | cut -c1-32; }
  bad=0; n=0; big=0
  LIST=$(mktemp); git -C "$HERE" ls-files > "$LIST"
  while IFS= read -r f; do
    n=$((n+1)); size=$(wc -c < "$HERE/$f" | tr -d ' ')
    if [ "$size" -gt 2000000 ] && [ "${FULL:-0}" != 1 ]; then
      big=$((big+1))
      len=$(curl -fsSIL --max-time 20 "${URL%/}/$f" | tr -d '\r' | awk 'tolower($1)=="content-length:"{l=$2} END{print l}')
      [ "$len" = "$size" ] || { echo "RED $f: live length ${len:-none} vs local $size" >&2; bad=$((bad+1)); }
    else
      T=$(mktemp)
      if curl -fsSL --max-time 120 "${URL%/}/$f" -o "$T"; then
        [ "$(sum "$T")" = "$(sum "$HERE/$f")" ] || { echo "RED $f: live content differs from local" >&2; bad=$((bad+1)); }
      else
        echo "RED $f: not served" >&2; bad=$((bad+1))
      fi
      rm -f "$T"
    fi
  done < "$LIST"
  rm -f "$LIST"
  [ "$bad" = 0 ] || exit 1
  echo "OK live == local: $lh, $bh bytes; figures.json md5 $fh; all $n tracked files match ($big by length)"; exit 0
fi
[ "$fl" = "$fh" ] || echo "RED figures.json live md5 $fl vs local $fh" >&2
echo "RED live stamp: ${ls_:-none}" >&2
echo "RED local stamp: $lh" >&2
echo "RED bytes live $bs vs local $bh" >&2
exit 1
