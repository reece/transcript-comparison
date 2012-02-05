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

    def grch37p5_exons(self,acv):
        gc = self._grch37p5_product_commentary(acv)
        assert len(gc.findall('Gene-commentary_products/Gene-commentary')) == 1, 'Found more than one gene product commentary'
        i = gc.iterfind('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_mix/Seq-loc-mix/Seq-loc/Seq-loc_int')
        return [ (int(n[0].find('Seq-interval_from').text),int(n[0].find('Seq-interval_to').text)) for n in i ]

    def grch37p5_exon_starts_ends_lengths(self):
        exons = self.grch37p5_exons()
        starts = [ e[0] for e in exons ]
        ends = [ e[1] for e in exons ]
        lengths = [ e[1]-e[0]+1 for e in exons ]
        return starts,ends,lengths

    def grch37p5_strand(self):
        gc = self._grch37p5_gene_commentary()
        return gc.find('Gene-commentary_seqs/Seq-loc/Seq-loc_int/Seq-interval/Seq-interval_strand/Na-strand').get('value')

    ######################################################################
    ## Internal functions

    def _grch37p5_product_commentary(self,acv):
        ac,v = acv.split('.')
        gc = _grch37p5_gene_commentary()
        pred = ' and '.join(['Gene-commentary_heading[text()="{heading}"]',
                             'Gene-commentary_accession[text()="{ac}"]',
                             'Gene-commentary_version[text()="{v}"'])
        pred = pred.format(heading=heading, ac=ac, v=v)
        xpath = 'Gene-commentary-products/Gene-commentary[%s]' % (pred)
        return gc.xpath(xpath)

    def _grch37p5_gene_commentary(self):
        return self._gene_commentary(self,heading='Reference GRCh37.p5 Primary Assembly')

    def _gene_commentary(self,heading):
        xpath = '/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary[%s]' % (pred)
        return self._root.xpath(xpath)[0]


def _feature_se(gbf):
    s,e = gbf.find('GBFeature_location').text.split('..')
    return int(s),int(e)

