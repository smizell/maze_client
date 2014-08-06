import xml.etree.ElementTree as ET
import unittest
import json

from adapters import hal_json, maze_xml
import translator
import hypermedia_client

import representer as representer

cell_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<maze version="1.0">
    <cell>
        <link href="http://amundsen.com/examples/mazes/2d/five-by-five/0:north" rel="current" debug="0:1,1,1,0" total="25" side="5" />
        <link href="http://amundsen.com/examples/mazes/2d/five-by-five/5:east" rel="east" />
    </cell>
</maze>
"""

cell_hal_json = """{
    "_links": {
        "north": { "href": "/cell/1" },
        "south": { "href": "/cell/1" }
    }
}"""

class TestMazeXMLFunctions(unittest.TestCase):

    def setUp(self):
        self.root = ET.fromstring(cell_xml)

    def test_get_type_of(self):
        resource_type = maze_xml.get_type_of(self.root)
        self.assertEqual(resource_type, 'cell')

    def test_parse_links(self):
        links = self.root[0].findall('link')
        parsed_links = maze_xml.parse_links(links)
        self.assertEqual(len(parsed_links.items), 2)
        self.assertEqual(parsed_links.items[0].rel, 'current')

class TestMazeXMLClass(unittest.TestCase):

    def setUp(self):
        self.adapter = maze_xml.MazeXMLAdapter()

    def test_parse(self):
        representer = self.adapter.parse(cell_xml)
        self.assertEqual(representer.type_of, 'cell')
        self.assertEqual(len(representer.links.items), 2)

class TestTranslatorClass(unittest.TestCase):

    def setUp(self):
        self.translate = translator.Translator()
        self.media_type = 'application/vnd.amundsen.maze+xml'

    def test_register(self):
        self.translate = translator.Translator()
        self.translate.register(maze_xml.MazeXMLAdapter)
        self.assertTrue(self.translate.adapters.has_key(self.media_type))

    def test_translate_from(self):
        rep = self.translate.translate_from(self.media_type, cell_xml)
        self.assertEqual(rep.type_of, 'cell')
        self.assertEqual(len(rep.links.items), 2)

class TestRepresenterClass(unittest.TestCase):

    def setUp(self):
        translate = translator.Translator()
        translate.register(maze_xml.MazeXMLAdapter)
        self.media_type = 'application/vnd.amundsen.maze+xml'
        self.representer = translate.translate_from(self.media_type, cell_xml)

    def test_filter_by_rel(self):
        filtered = self.representer.links.filter_by_rel('east')
        self.assertEqual(len(filtered), 1)

    def test_has_rel(self):
        self.assertTrue(self.representer.links.has_rel('east'))
        self.assertFalse(self.representer.links.has_rel('dne'))

    def test_get_by_rel(self):
        first = self.representer.links.get_by_rel('east')
        self.assertEqual(first.rel, 'east')

    def test_translate_to(self):
        new_xml = str(self.representer.translate_to(self.media_type))
        root = ET.fromstring(new_xml)
        self.assertEqual(root[0].tag, 'cell')
        self.assertEqual(len(root[0].findall('link')), 2)

class TestHypermediaClient(unittest.TestCase):

    def setUp(self):
        self.translate = translator.Translator()
        self.translate.register(maze_xml.MazeXMLAdapter)

    def test_get_headers(self):
        headers = hypermedia_client.get_accept_header(self.translate)
        self.assertEqual(headers, 'application/vnd.amundsen.maze+xml')

    def test_headers(self):
        client = hypermedia_client.HypermediaClient(self.translate)
        self.assertEqual(client.headers()['Accept'], 'application/vnd.amundsen.maze+xml')

class TestHalJSONFunctions(unittest.TestCase):

    def setUp(self):
        self.hal_json = json.loads(cell_hal_json)

    def test_parse_links(self):
        links = hal_json.parse_links(self.hal_json)
        self.assertEqual(len(links.items), 2)

    def test_build_link(self):
        link = hal_json.build_link(representer.Link(rel="north", href="/test"))
        expected_link = ("north", { 'href': "/test" })
        self.assertEqual(link, expected_link)

class TestHalJSONClass(unittest.TestCase):

    def setUp(self):
        self.adapter = hal_json.HalJSONAdapter()

    def test_parse(self):
        rep = self.adapter.parse(cell_hal_json)
        self.assertTrue(rep.links.has_rel('north'))

    def test_build(self):
        rep = representer.Representer(type_of="", adapters={})
        rep.register(hal_json.HalJSONAdapter)
        rep.links.add(rel='north', href='/test')
        raw_hal = json.loads(rep.translate_to('application/hal+json'))
        self.assertTrue(raw_hal.has_key('_links'))

if __name__ == '__main__':
    unittest.main()

