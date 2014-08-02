from adapters.maze_xml import MazeXMLAdapter
from translator import Translator
from hypermedia_client import HypermediaClient

rules = {
    'east'  : ['south','east','north','west'],
    'south' : ['west','south','east','north'],
    'west'  : ['north','west','south','east'],
    'north' : ['east','north','west','south']
}

def solve_maze(maze_url):
    # Load our hypermedia format translator and register
    # the media type we'll be using
    translator = Translator()
    translator.register(MazeXMLAdapter)

    # Load up the hypermedia client and give it the translort so
    # it knows what to put in the Accept header
    client = HypermediaClient(translator)

    # Start the bot and solve the maze
    bot = MazeXMLBot(client=client, maze_url=maze_url)
    bot.solve()

    return bot

class MazeXMLBot:

    MAX_MOVES = 100

    def __init__(self, client, maze_url):
        self.client = client
        self.maze_url = maze_url

        # Current direction bot is facing
        self.facing = ''

        # Total moves for bot
        self.moves = 0

        # Has the bot started or completed the maze
        self.started = False
        self.completed = False

        # Representation of the bot's current cell
        self.cell = None

    def make_next_move(self):
        self.moves += 1

        # Just so our bot doesn't wander forever
        if self.moves == self.MAX_MOVES:
            return

        # We beat the maze!
        if self.cell.links.has_rel('exit'):
            self.completed = True
            exit_link = self.cell.links.get_by_rel('exit').href
            self.cell = self.client.follow(exit_link)
            return

        # Based on the direction we're facing and the defined rules, follow
        # the best link to find the exit.
        available_moves = self.cell.links.all_rels()
        for direction in rules[self.facing]:
            if direction in available_moves:
                direction_link = self.cell.links.get_by_rel(direction).href
                self.facing = direction
                self.cell = self.client.follow(direction_link)
                return self.make_next_move()

        # How did we find a room with no doors?
        return

    def solve(self):
        if not self.started:
            start_rep = self.client.follow(maze_url)
            if start_rep.links.has_rel('start'):
                self.moves += 1
                self.cell = self.client.follow(start_rep.links.get_by_rel('start').href)
                self.facing = 'north'
                self.started = True

        if self.cell:
            self.make_next_move()

if __name__ == '__main__':
    maze_url = 'http://amundsen.com/examples/mazes/2d/five-by-five/'
    victory_bot = solve_maze(maze_url)
    print "Completed: " + str(victory_bot.completed)
    print "Moves: " + str(victory_bot.moves)
