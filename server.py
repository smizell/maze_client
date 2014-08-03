from flask import Flask, Response

from representer import Representer
from adapters.maze_xml import MazeXMLAdapter

app = Flask(__name__)

# Rels for links below
rels = ['north', 'east', 'south', 'west', 'exit']

# Each cell and it's links to the other cells
# Each item in these lists corresponds to the rels above
cells = [
    [None, 5, None, None, None],
    [None, 6, None, None, None],
    [None, 7, 3, None, None],
    [2, None, 4, None, None],
    [3, 9, None, None, None],
    [None, 10, None, 0, None],
    [None, None, 7, 1, None],
    [6, 12, None, 2, None],
    [None, 13, 9, None, None],
    [8, None, None, 4, None],
    [None, None, 11, 5, None],
    [10, 16, None, None, None],
    [None, None, None, 7, None],
    [None, None, 14, 8, None],
    [13, 19, None, None, None],
    [None, 20, None, None, None],
    [None, 21, None, 11, None],
    [None, 22, 18, None, None],
    [17, None, 19, None, None],
    [18, 24, None, 14, None],
    [None, None, 21, 15, None],
    [20, None, 22, 16, None],
    [21, None, None, 17, None],
    [None, None, 24, None, None],
    [None, None, None, None, 999]
]

def maze_rep(type_of):
    rep = Representer(type_of=type_of, adapters={})
    rep.register(MazeXMLAdapter)
    return rep

def link_to_cell(cell_num):
    return 'http://127.0.0.1:5000/cells/'+str(cell_num)

def get_links(cell_num):
    cell = cells[cell_num]
    cell_with_rels = dict(zip(rels, cell))
    links = dict((k, link_to_cell(v)) for k, v in cell_with_rels.iteritems() if v)
    return links

@app.route('/')
def root():
    rep = maze_rep('item')
    rep.links.add(rel='start', href=link_to_cell(0))
    media_type = MazeXMLAdapter.media_type
    maze_xml = rep.translate_to(media_type)
    return Response(maze_xml, mimetype=media_type)

@app.route('/cells/999')
def exit():
    rep = maze_rep('completed')
    rep.links.add(rel='start', href=link_to_cell(0))
    media_type = MazeXMLAdapter.media_type
    maze_xml = rep.translate_to(media_type)
    return Response(maze_xml, mimetype=media_type)

@app.route('/cells/<cell_num>')
def cell(cell_num):
    rep = maze_rep('cell')
    links = get_links(int(cell_num))
    for rel, link in links.iteritems():
        rep.links.add(rel=rel, href=link)
    media_type = MazeXMLAdapter.media_type
    maze_xml = rep.translate_to(media_type)
    return Response(maze_xml, mimetype=media_type)

if __name__ == "__main__":
    app.debug = True
    app.run()

