from hypermedia_resource import HypermediaResource
from hypermedia_client import HypermediaClient
from maze_bot import MazeXMLBot

def solve_maze(maze_url):
    resource = HypermediaResource()

    # Load up the hypermedia client and give it the hypermedia
    # resource so it knows what to put in the Accept header
    client = HypermediaClient(resource)

    # Start the bot and solve the maze
    bot = MazeXMLBot(client=client, maze_url=maze_url)
    bot.solve()

    return bot

if __name__ == '__main__':
    # Mike Amundsen's Server
    #maze_url = 'http://amundsen.com/examples/mazes/2d/five-by-five/'

    # Local Server (python server.py)
    maze_url = 'http://127.0.0.1:5000/'

    victory_bot = solve_maze(maze_url)
    print "Completed: " + str(victory_bot.completed)
    print "Moves: " + str(victory_bot.moves)
