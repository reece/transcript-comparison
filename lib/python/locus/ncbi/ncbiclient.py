from cogent.db.ncbi import EFetch,ELink,ESearch

from locus.ncbi.esearchresult import ESearchResult
from locus.ncbi.refseq import RefSeq
from locus.ncbi.elinkresult import ELinkResult
from locus.ncbi.gene import Gene


eutils_defaults = {
    'tool': sys.argv[0],
    'email': 'reecehart@gmail.com',
    'retmax': 5,
    'retmode': 'xml'
    }


class NCBIClient(object):
    def __init__(self):
        self._es = ESearch(rettype='uilist',**eutils_defaults)
        self.ef = EFetch(**eutils_defaults)
        self.el = ELink(**eutils_defaults)

    def search_by_accession(self,term):
        return ESearchResult( es.read(term='%s[accn]'%(ac)) )

    def fetch_refseq_by_id(self,id):
        return RefSeq(ef.read(db='nuccore',id=id,retmode='xml',rettype='gb'))

    def fetch_refseq_by_ac(self,ac):
        esr = ESearchResult( es.read(term='%s[accn]'%(ac)) )
        assert len(esr.uilist()) == 1
        return RefSeq(ef.read(db='nuccore',id=esr.uilist()[0],retmode='xml',rettype='gb'))
