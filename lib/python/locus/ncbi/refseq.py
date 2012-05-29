from lxml.etree import XML
import IPython

class RefSeq(object):
    def __init__(self,xml):
        self._root = XML(xml)

    def cds_start_end(self):
        n = self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key/text()="CDS"]')
        assert len(n) == 1, "expected exactly one CDS GBFeature_key node"
        s,e = _feature_se(n[0])
        return s,e

    def cds_start(self):
        return self.cds_start_end()[0]

    def chr(self):
        return self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature['
                                'GBFeature_key/text()="source"]/GBFeature_quals'
                                '/GBQualifier[GBQualifier_name/text()='
                                '"chromosome"]/GBQualifier_value')[0].text

    def exons(self):
        exon_nodes = self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="exon"]')
        return [ _feature_se(n) for n in exon_nodes ]

    def seq(self):
        return self._root.xpath('/GBSet/GBSeq/GBSeq_sequence')[0].text

def _feature_se(gbf):
    loc = gbf.find('GBFeature_location').text
    if 'join' in loc:
        raise RuntimeError('discontiguous genbank feature')
    s,e = loc.split('..')
    return int(s),int(e)
