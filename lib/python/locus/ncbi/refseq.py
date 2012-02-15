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

    def seq(self):
        return self._root.xpath('/GBSet/GBSeq/GBSeq_sequence')[0].text

def _feature_se(gbf):
    s,e = gbf.find('GBFeature_location').text.split('..')
    return int(s),int(e)
