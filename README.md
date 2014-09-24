Hypermedia Maze Example
===========

## Description

This repository shows an example of a client and server both using a Hypermedia Resource library.

### Hypermedia Client

[Hypermedia Client Code](https://github.com/smizell/maze_client/blob/master/hypermedia_client.py)

This client understands how to interact with resources, by following links and other actions (currently in this example, only follow is supported). Because the Translator has a list of what media types it knows, the Hypermedia Client can put those media types in the `Accept` header. Then, based on what the response's `Content-Type` is, it can automatically parse that response into a Hypermedia Resource. 

This helps move away from requesting specific media types and relying on the client and translator to do the content negotiation.

This Hypermedia Client would also exist as its own library apart from this project.

### Maze Bot

[Maze Bot Code](https://github.com/smizell/maze_client/blob/master/maze_bot.py)

This is the code that actually solves the maze. It relies on the Hypermedia Client to handle all the requests and responses, and it relies on the Hypermedia Resource to provide the general interface. At that point, the developer simply writes the moves the bot should take as it goes through the maze.

### Solver

[Solver Code](https://github.com/smizell/maze_client/blob/master/solver.py)

The solver file uses the Maze Bot to solve the maze. I put this code in a file by itself to separate out the code a little for the purpose of the example.

### Server

[Server Code](https://github.com/smizell/maze_client/blob/master/server.py)

The server code uses the Hypermedia Resource to translate to a specific media type. This allows for a new media type to be served without changing the logic for creating and serving the resources. 

In the best case scenario, the server would handle content negotiation and send the best media type for the client. This current example only supports one media type at a time.

## About the Code

This code shows an example of how to organize code around hypermedia clients using the [Hypermedia Resource library](https://github.com/the-hypermedia-project/hypermedia-resource-python).

To install requirements:

```shell
pip install -r requirements.pip
```

```shell
python server.py http://maze-server.herokuapp.com/
```
