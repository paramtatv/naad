#!/bin/sh
# The resync bound in kernel/nihshesha.t1 must compare SIGNED. Rule 6a872ccf: an ordering
# compare is unsigned when either operand is a bare name of type न८..न६४, so a कोणः or
# उच्चम् declared न६४ wraps a negative limit (सीमान्तः < १६) into a huge number and the
# scan finds a frame past the caller's bound. naad vendors sravan's kernel without its t1
# tests (sravan kernel/pariksha_punah.t1 pins the behaviour); this holds the two declarations.
# Exit status is the number of missing lines. Prints nothing on green except OK.
set -u
HERE=$(cd "$(dirname "$0")/.." && pwd)
K="$HERE/kernel/nihshesha.t1"
[ -f "$K" ] || { echo "OK kernel/ not vendored; nothing to check"; exit 0; }
bad=0
for decl in \
  'चरः कोणः ॱॱ अ६४ भवति सूचकम् अङ्कः ० अन्तः ।' \
  'चरः उच्चम् ॱॱ अ६४ भवति सीमान्तः वियोगः १६ ।'
do
  grep -qF -- "$decl" "$K" || { echo "RED kernel/nihshesha.t1 lost the signed resync declaration: $decl" >&2; bad=$((bad+1)); }
done
[ "$bad" -eq 0 ] && echo "OK the resync bound declarations are signed (अ६४)"
exit "$bad"
