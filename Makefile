.PHONY: FORCE
.SUFFIXES:
.DELETE_ON_ERROR:
SHELL:=/bin/bash

VIRTUALENV_DIR:=ve

setup: ${VIRTUALENV_DIR} install-reqs

${VIRTUALENV_DIR}:
	virtualenv $@
install-reqs: etc/reqs.pip ${VIRTUALENV_DIR}
	${VIRTUALENV_DIR}/bin/pip install -r $<





############################################################################
## miscellaneous utilities
BLOCK:=The following items are updated automatically by make TODO
TODO: FORCE
	# updating $@
	@( \
	set -e; \
	[ -s "$@" ] && perl -lpe 'last if $$_ eq "${BLOCK}"' <"$@"; \
	echo "${BLOCK}"; \
	find bin lib/python/locus \( -name \*.py \) -print0 \
	| xargs -0r perl -ne 'if (s/^\s*#\s*(?=TODO:|FIXME:)//) {' \
	-e 'print("\n$$ARGV:\n","="x76,"\n") unless $$p{$$ARGV}++; print;}' \
	) >"$@.tmp" && /bin/mv "$@.tmp" "$@"


.PHONY: clean cleaner cleanest
clean:
	find . \( -name \*~ -o -name \*.pyc \) -print0 | xargs -0r /bin/rm
cleaner: clean
	find . \( -name \*bak -o -name \*.orig \) -print0 | xargs -0r /bin/rm
cleanest: cleaner
	/bin/rm -fr ${VIRTUALENV_DIR}

