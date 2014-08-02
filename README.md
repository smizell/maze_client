Maze Client
===========

This code shows an example of how to organize code around hypermedia clients.

To install:

```shell
pip install -r requirements.pip
```

## Adapters

[Adapters Directory](https://github.com/smizell/maze_client/tree/master/adapters)

An adapter is code that understands how to convert from a media type to a representer, and from a representer to a media type. The point of this is to provide a general interface to hypermedia formats, to allow client developers to work with the interface rather than the specifics of media types.

## Representer

[Representer Code](https://github.com/smizell/maze_client/blob/master/representer.py)

The representer is the general interface for a resource. It provides the general interface to the resource to abstract away the differences between media types.

This is of course as an example purpose only, but the representers and adapters would be standalone libraries that could be used in other clients. Once a media type can be represented with this model, it can be used anywhere else, even on the server side.

An example of this type of representer model is [Halpert](https://github.com/smizell/halpert).

## Translator

[Translator Code](https://github.com/smizell/maze_client/blob/master/translator.py)

The translator is where these Adapters are registered. A Translator is basically taught how to understand these different media types by giving it adapters, that know the specifics of the media types.

## Hypermedia Client

[Hypermedia Client Code](https://github.com/smizell/maze_client/blob/master/hypermedia_client.py)

This client understands how to interact with resources, by following links and other actions (currently in this example, only follow is supported). Because the Translator has a list of what media types it knows, the Hypermedia Client can put those media types in the `Accept` header. Then, based on what the response's `Content-Type` is, it can automatically parse that response into a Representer. 

This helps move away from requesting specific media types and relying on the client and translator to do the content negotiation.

This Hypermedia Client would also exist as its own library apart from this project.

## Maze Bot

[Maze Bot Code](https://github.com/smizell/maze_client/blob/master/maze_bot.py)

This is the code that actually solves the maze. It relies on the Hypermedia Client to handle all the requests and responses, and it relies on the Representer to provide the general interface. At that point, the developer simply writes the moves the bot should take as it goes through the maze.

## Solver

The solver file uses the Maze Bot to solve the maze. I put this code in a file by itself to separate out the code a little for the purpose of the example.
