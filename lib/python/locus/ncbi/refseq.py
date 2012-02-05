from lxml.etree import XML

class RefSeq(object):
    def __init__(self,xml):
        self._root = XML(xml)

    def cds_start(self):
        n = r._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="CDS"]')
        assert len(n) == 0
        s,e = _feature_se(n[0])
        return s

    def exons(self):
        exon_nodes = self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="exon"]')
        return [ _feature_se(n) for n in exon_nodes ]

    def exon_starts_ends_lengths(self):
        exons = self.exons()
        starts = [ e[0] for e in exons ]
        ends = [ e[1] for e in exons ]
        lengths = [ e[1]-e[0]+1 for e in exons ]
        return starts,ends,lengths




def _feature_se(gbf):
    s,e = gbf.find('GBFeature_location').text.split('..')
    return int(s),int(e)
