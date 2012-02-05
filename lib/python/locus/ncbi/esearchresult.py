from lxml.etree import XML

class ESearchResult(object):
    def __init__(self,xml):
        self._root = XML(xml)
    def count(self):
        return int(self._root.xpath('/eSearchResult/Count')[0].text)
    def retmax(self):
        return int(self._root.xpath('/eSearchResult/RetMax')[0].text)
    def retstart(self):
        return int(self._root.xpath('/eSearchResult/RetStart')[0].text)
    def uilist(self):
        return [ n.text for n in self._root.xpath('/eSearchResult/IdList/Id') ]

