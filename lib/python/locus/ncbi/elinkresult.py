from lxml.etree import XML

class ELinkResult(object):
    def __init__(self,xml):
        self._root = XML(xml)

    def results(self):
        return [ { 'to':n.find('DbTo').text,
                   'link_name':n.find('LinkName').text,
                   'ids': n.find('Link/Id').text } 
                 for n in self._root.xpath('/eLinkResult/LinkSet/LinkSetDb') ]
