import representer as representer
import xml.etree.ElementTree as ET

def get_type_of(root):
    """
    The first child element of the response should tell us what
    type of response this is
    """
    return root[0].tag

def parse_links(links):
    links_rep = representer.Links()
    for link in links:
        links_rep.add(rel=link.get('rel'), href=link.get('href'))
    return links_rep

class MazeXMLAdapter:
    """
    This adapter understands how to parse a Maze+XML response and
    create a representer object from it. The `build` method can
    be finisehd to allow this object to also know how to build
    a Maze+XML representation from a representer object, which
    could be used on the server.
    """

    # Used by the translator to know how to register this adapter
    media_type = 'application/vnd.amundsen.maze+xml'

    def __init__(self, adapters=None):
        self.adapters = adapters

    def parse(self, raw_representation):
        root = ET.fromstring(raw_representation)
        type_of = get_type_of(root)
        links = parse_links(root[0].findall('link'))
        return representer.Representer(type_of=type_of, links=links,
                                       adapters=self.adapters)

    def build(self, representer):
        root = ET.Element('maze')
        root.set('version', '1.0')
        type_of = ET.SubElement(root, representer.type_of)
        for link in representer.links.items:
            new_link = ET.SubElement(type_of, 'link')
            new_link.set('rel', link.rel)
            new_link.set('href', link.href)
        return ET.tostring(root, encoding='utf8', method='xml')
