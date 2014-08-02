import representer as representer
import xml.etree.ElementTree as ET

def get_type_of(root):
    return root[0].tag

def parse_links(links):
    links_rep = representer.Links()
    for link in links:
        links_rep.add(rel=link.get('rel'), href=link.get('href'))
    return links_rep

class MazeXMLAdapter:

    media_type = 'application/vnd.amundsen.maze+xml'

    def parse(self, raw_representation):
        root = ET.fromstring(raw_representation)
        type_of = get_type_of(root)
        links = parse_links(root[0].findall('link'))
        return representer.Representer(type_of=type_of, links=links)

    def build(self, representer):
        return True
