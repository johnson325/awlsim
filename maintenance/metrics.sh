#!/bin/sh

basedir="$(dirname "$0")"
[ "$(echo "$basedir" | cut -c1)" = '/' ] || basedir="$PWD/$basedir"

[ $# -ge 1 ] || {
	echo "Usage: $0 [CLOC-OPTS] DIRECTORY" >&2
	exit 1
}

set -e

cd "$basedir/.."
submodpaths="$(git submodule status | awk '{print $2;}' | tr "[:space:]" ",")"

cloc --exclude-dir="build,dist,.pybuild,release-archives,icons,__pycache__,${submodpaths},awlsim_cython,pyprofibus,libpilc" \
	--read-lang-def="${basedir}/cloc-lang-awl.txt" \
	--exclude-lang='ASP.Net,IDL,D' \
	--quiet --progress-rate=0 \
	"$@"
