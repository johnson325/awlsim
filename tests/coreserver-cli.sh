# awlsimcli with coreserver tests

sh_test()
{
	local interpreter="$1"

	echo
	echo "--- Running coreserver tests"
	for testfile in shutdown.awl; do
		run_test "$interpreter" "$basedir/$testfile" \
			--spawn-backend --interpreter "$interpreter"
	done
	echo -n "--- Finished coreserver tests "
}
