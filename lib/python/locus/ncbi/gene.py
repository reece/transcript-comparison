import logging
from lxml.etree import XML

from locus.core.exceptions import LocusError

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

    def grch37p5_mapping(self):
        gc = self._grch37p5_gc()
        si = gc.find('Gene-commentary_seqs/Seq-loc/Seq-loc_int/Seq-interval')
        ac = gc.find('Gene-commentary_accession').text
        v = gc.find('Gene-commentary_version').text
        return { 
            'chr': _NC_to_chr(ac),
            'accession': ac,
            'version': v,
            'ac': ac+'.'+v,
            'start': int(si.find('Seq-interval_from').text),
            'end': int(si.find('Seq-interval_to').text),
            'strand': si.find('Seq-interval_strand/Na-strand').get('value'),
            'gi': int(si.find('Seq-interval_id/Seq-id/Seq-id_gi').text),
            }

    def grch37p5_product_exons(self,acv):
        gc = self._grch37p5_product_gc(acv)
        i = gc.iterfind('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_mix/Seq-loc-mix/Seq-loc/Seq-loc_int/Seq-interval')
        return [ (int(n.find('Seq-interval_from').text),int(n.find('Seq-interval_to').text)) for n in i ]

    def grch37p5_product_strand(self,acv):
        gc = self._grch37p5_product_gc(acv)
        n = gc.find('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_mix/Seq-loc-mix/Seq-loc/Seq-loc_int/Seq-interval')
        return n.find('Seq-interval_strand/Na-strand').get('value')

    def grch37p5_product_seq_id(self,acv):
        gc = self._grch37p5_product_gc(acv)
        n = gc.find('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_mix/Seq-loc-mix/Seq-loc/Seq-loc_int/Seq-interval')
        return n.find('Seq-interval_id/Seq-id/Seq-id_gi').text

    ######################################################################
    ## Internal functions
    # TODO: Expand to manipulate alignments to non-chromosomal reference
    # e.g., NM_000034.3, gene 226, aligns to an NG and HuRef, but not
    # to GRCh37. Should use gis for all alignment

    def _grch37p5_product_gc(self,acv):
        ac,v = acv.split('.')
        gc = self._grch37p5_gc()
        pred = ' and '.join(['Gene-commentary_accession/text()="{ac}"',
                             'Gene-commentary_version/text()="{v}"'])
        pred = pred.format(ac=ac, v=v)
        xpath = 'Gene-commentary_products/Gene-commentary[%s]' % (pred)
        nodes = gc.xpath(xpath)
        if len(nodes) != 1:
            raise LocusError("Got %d Gene-commentary_products for %s"%(len(nodes),acv))
        return nodes[0]
        
    def _grch37p5_gc(self):
        return self._gc(heading='Reference GRCh37.p5 Primary Assembly')

    def _gc(self,heading):
        xpath = '/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary[Gene-commentary_heading[text()="%s"]]' % (heading)
        return self._root.xpath(xpath)[0]


def _feature_se(gbf):
    s,e = gbf.find('GBFeature_location').text.split('..')
    return int(s),int(e)

def _NC_to_chr(ac):
    return {
        'NC_000001': '1',        'NC_000002': '2',        'NC_000003': '3',
        'NC_000004': '4',        'NC_000005': '5',        'NC_000006': '6',
        'NC_000007': '7',        'NC_000008': '8',        'NC_000009': '9',
        'NC_000010': '10',       'NC_000011': '11',       'NC_000012': '12',
        'NC_000013': '13',       'NC_000014': '14',       'NC_000015': '15',
        'NC_000016': '16',       'NC_000017': '17',       'NC_000018': '18',
        'NC_000019': '19',       'NC_000020': '20',       'NC_000021': '21',
        'NC_000022': '22',       'NC_000023': 'X',        'NC_000024': 'Y',
        }[ac]
