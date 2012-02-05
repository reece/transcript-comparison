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






.PHONY: clean cleaner cleanest
clean:
	find . \( -name \*~ -o -name \*.pyc \) -print0 | xargs -0r /bin/rm
cleaner: clean
	find . \( -name \*bak -o -name \*.orig \) -print0 | xargs -0r /bin/rm
cleanest: cleaner
	/bin/rm -fr ${VIRTUALENV_DIR}
