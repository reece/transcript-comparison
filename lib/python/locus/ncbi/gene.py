from lxml.etree import XML

class Gene(object):
    def __init__(self,xml):
        self._root = XML(xml)

    # TODO: rename hgnc or somesuch
    def locus(self):
        return self._root.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_locus/text()')[0]

    def desc(self):
        return self._root.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_desc/text()')[0]

    def maploc(self):
        return self._root.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_maploc/text()')[0]

    def summary(self):
        return self._root.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_summary/text()')[0]

    def grch37p5_product_exons(self,acv):
        gc = self._grch37p5_product_gc(acv)
        i = gc.iterfind('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_mix/Seq-loc-mix/Seq-loc/Seq-loc_int/Seq-interval')
        return [ (int(n.find('Seq-interval_from').text),int(n.find('Seq-interval_to').text)) for n in i ]

    def grch37p5_product_strand(self,acv):
        gc = self._grch37p5_product_gc(acv)
        n = gc.find('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_mix/Seq-loc-mix/Seq-loc/Seq-loc_int/Seq-interval')
        return n.find('Seq-interval_strand/Na-strand').get('value')

    ######################################################################
    ## Internal functions

    def _grch37p5_product_gc(self,acv):
        ac,v = acv.split('.')
        gc = self._grch37p5_gene_commentary()
        pred = ' and '.join(['Gene-commentary_accession/text()="{ac}"',
                             'Gene-commentary_version/text()="{v}"'])
        pred = pred.format(ac=ac, v=v)
        xpath = 'Gene-commentary_products/Gene-commentary[%s]' % (pred)
        nodes = gc.xpath(xpath)
        assert len(nodes) == 1, "Expected only one matching Gene-commentary_products for %s"%(acv)
        return nodes[0]

    def _grch37p5_gene_commentary(self):
        return self._gene_commentary(heading='Reference GRCh37.p5 Primary Assembly')

    def _gene_commentary(self,heading):
        xpath = '/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary[Gene-commentary_heading[text()="%s"]]' % (heading)
        return self._root.xpath(xpath)[0]


def _feature_se(gbf):
    s,e = gbf.find('GBFeature_location').text.split('..')
    return int(s),int(e)

