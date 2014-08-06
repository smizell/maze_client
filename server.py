from flask import Flask, Response

from representer import Representer
from adapters.maze_xml import MazeXMLAdapter
from adapters.hal_json import HalJSONAdapter

app = Flask(__name__)

# Rels for links below
rels = ['north', 'east', 'south', 'west', 'exit']

# Each cell and it's links to the other cells
# The items of each cell correspond to the rel above
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

# The media type this server will send
MEDIA_TYPE = HalJSONAdapter.media_type

# Helper functions for the views

def maze_rep(type_of):
    """
    Sets up a Representer for the resource
    """
    rep = Representer(type_of=type_of, adapters={})
    rep.register(HalJSONAdapter)
    return rep

def maze_response(rep):
    """
    Translates a representer to Maze+XML and creates
    a respones with the Maze+XML media type
    """
    maze_rep = rep.translate_to(MEDIA_TYPE)
    return Response(maze_rep, mimetype=MEDIA_TYPE)

def link_to_cell(cell_num):
    """
    Helper for generating links to specific cells
    """
    return 'http://127.0.0.1:5000/cells/'+str(cell_num)

def get_links_for_cell(cell_num):
    """
    Generates link for a specific cell
    """
    cell = cells[cell_num]
    cell_with_rels = dict(zip(rels, cell))
    links = dict((k, link_to_cell(v)) for k, v in cell_with_rels.iteritems() if v)
    return links

# Route and views

@app.route('/')
def root():
    """
    Root resource
    """
    rep = maze_rep(type_of='item')
    rep.links.add(rel='start', href=link_to_cell(0))
    return maze_response(rep)

@app.route('/cells/999')
def exit():
    """
    Exit resource
    """
    rep = maze_rep(type_of='completed')
    rep.links.add(rel='start', href=link_to_cell(0))
    return maze_response(rep)

@app.route('/cells/<cell_num>')
def cell(cell_num):
    """
    Cell resource
    """
    rep = maze_rep(type_of='cell')
    links = get_links_for_cell(int(cell_num))
    for rel, link in links.iteritems():
        rep.links.add(rel=rel, href=link)
    return maze_response(rep)

if __name__ == "__main__":
    app.debug = True
    app.run()

