.PHONY: FORCE
.SUFFIXES:
.DELETE_ON_ERROR:
SHELL:=/bin/bash

VIRTUALENV_DIR:=ve
export PYTHONUNBUFFERED:=1
export PYTHONPATH:=${HOME}/projects/locus-python/lib

setup: ${VIRTUALENV_DIR} install-reqs

${VIRTUALENV_DIR}:
	virtualenv $@
install-reqs: etc/reqs.pip ${VIRTUALENV_DIR}
	${VIRTUALENV_DIR}/bin/pip install -r $<


human.rna.fna.gz:
	curl ftp://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/mRNA_Prot/human.rna.fna.gz >'$@.tmp' \
	&& mv -fv '$@.tmp' '$@'

all: human.rna.fna.gz
	gzip -cd <$< | perl -lne 'print $$& if m/NM_\d+\.\d+/' | sort >$@

%.dup: %
	unset LANG LC_COLLATE; join <(tail -n+2 $< | cut -f1 | sort -t\t | uniq -d) <(tail -n+2 $< | sort -t\t) >$@

%.d: %
	mkdir $@
	split -l 100 $< $@/

%.d/log: %.d
	make -j4 $(addsuffix .cmp,$(wildcard $</??))

.SECONDARY: %.cmp
%.cmp: %
	xargs <$< ./bin/ncbi-compare-refseq-to-genome >$@ 2>$@.log

all.cmp: all.d/log
	sort $(addsuffix .cmp,$(wildcard ${<D}/??.cmp)) -o $@


transcripts.tsv: all.cmp
	./bin/post-proc <$< ens >$@



# Q: How many ensembl CDSs are represented in RefSeq?
# Instead of directly comparing exon structures, just assume that
# equivalent sequences implies same CDS.  Equivalency is by md5 checksum.
# We'll look in both cdna and peptide space.
md5s: refseq-pep.md5s refseq-cdna.md5s ensembl-pep.md5s ensembl-cdna.md5s

refseq-pep.md5s refseq-cdna.md5s:
	gzip -cqd <$< \
	| ./bin/fasta-checksum \
	| perl -aF'\t' -wlne 'print "$$F[0]\t$$1" if $$F[1]=~m/ref\|([^\|]+)/;' \
	| sort >$@
refseq-pep.md5s: /locus/data/mirrors/ftp.ncbi.nih.gov/refseq/H_sapiens/mRNA_Prot/human.protein.faa.gz
refseq-cdna.md5s: /locus/data/mirrors/ftp.ncbi.nih.gov/refseq/H_sapiens/mRNA_Prot/human.rna.fna.gz

ensembl-pep.md5s ensembl-cdna.md5s:
	gzip -cqd <$< \
	| ./bin/fasta-checksum \
	| perl -pe 's/(ENS[PT]\d+).+/$$1/' \
	| sort >$@
ensembl-pep.md5s: /locus/data/mirrors/ftp.ensembl.org/pub/release-65/fasta/homo_sapiens/pep/Homo_sapiens.GRCh37.65.pep.all.fa.gz
ensembl-cdna.md5s: /locus/data/mirrors/ftp.ensembl.org/pub/release-65/fasta/homo_sapiens/cdna/Homo_sapiens.GRCh37.65.cdna.all.fa.gz

%.ua-md5s: %.md5s
	cut -f1 $< | sort -u >$@

common-%: refseq-%.ua-md5s ensembl-%.ua-md5s
	comm -12 <(cut -f1 <$(word 1,$^)|sort -u) <(cut -f1 <$(word 2,$^)|sort -u) >$@
refseq-only-%: refseq-%.ua-md5s ensembl-%.ua-md5s
	comm -23 <(cut -f1 <$(word 1,$^)|sort -u) <(cut -f1 <$(word 2,$^)|sort -u) >$@
ensembl-only-%: refseq-%.ua-md5s ensembl-%.ua-md5s
	comm -13 <(cut -f1 <$(word 1,$^)|sort -u) <(cut -f1 <$(word 2,$^)|sort -u) >$@



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

