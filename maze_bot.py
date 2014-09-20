rules = {
    'east'  : ['south','east','north','west'],
    'south' : ['west','south','east','north'],
    'west'  : ['north','west','south','east'],
    'north' : ['east','north','west','south']
}

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
            exit_link = self.cell.links.get('exit').href
            self.cell = self.client.follow(exit_link)
            return

        # Based on the direction we're facing and the defined rules, follow
        # the best link to find the exit.
        available_moves = self.cell.links.get_rels()
        for direction in rules[self.facing]:
            if direction in available_moves:
                direction_link = self.cell.links.get(direction).href
                self.facing = direction
                self.cell = self.client.follow(direction_link)
                return self.make_next_move()

        # How did we find a room with no doors?
        return

    def solve(self):
        if not self.started:
            start_rep = self.client.follow(self.maze_url)
            if start_rep.links.has_rel('start'):
                self.moves += 1
                self.cell = self.client.follow(start_rep.links.get('start').href)
                self.facing = 'north'
                self.started = True

        if self.cell:
            self.make_next_move()
