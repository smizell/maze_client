import json

import representer

def parse_links(hal_json):
    """
    Parse the hal `_links` attribute

    This currently does not take into account the following:

    1. It does not deal with link templates
    2. It does not handle curies
    3. It does not handle the differences between a link object and link dict

    This is minimal for demonstration purposes only.
    """
    links = representer.Links()

    if not hal_json.has_key('_links'):
        return links
    for rel, link in hal_json['_links'].iteritems():
        links.add(rel=rel, href=link['href'])
    return links

def build_link(link):
    return (link.rel, { 'href': link.href })

class HalJSONAdapter:

    media_type = 'application/hal+json'

    def __init__(self, adapters=None):
        self.adapters = adapters

    def parse(self, raw_representation):
        hal_json = json.loads(raw_representation)
        links = parse_links(hal_json)
        return representer.Representer(type_of="", links=links, adapters=self.adapters)

    def build(self, representer):
        links = dict(build_link(link) for link in representer.links.items)
        return json.dumps({ '_links': links })
