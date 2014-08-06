import translator

class Representer(translator.Translator):
    """
    Representer model of a resource

    There are a lot more methods and variables that would be added here,
    but for example purposes, only the necessary ones are included. The
    purpose of this representer would be to have a class that can
    handle any kind of resource representation in any kind of media
    type.
    """

    def __init__(self, type_of, adapters, links=None):
        # This will be where our links are stored
        if links:
            self.links = links
        else:
            self.links = Links()

        # This will be how we define if this representer is for
        # a collection, item, or cell
        if type_of:
            self.type_of = type_of
        else:
            self.type_of = None

        # So our representer knows how to translate to other registered
        # media types
        self.adapters = adapters

    def translate_to(self, media_type):
        adapter = self.adapters[media_type]()
        return adapter.build(self)

class Links:
    """
    Links, actions, forms, etc for a given representation
    """

    def __init__(self):
        self.items = []

    def add(self, rel, href):
        link = Link(rel, href)
        self.items.append(link)
        return link

    def filter_by_rel(self, rel):
        return [item for item in self.items if item.rel == rel]

    def get_by_rel(self, rel):
        return self.filter_by_rel(rel)[0]

    def has_rel(self, rel):
        return len(self.filter_by_rel(rel)) > 0

    def all_rels(self):
        return [item.rel for item in self.items]

class Link:
    """
    Individual link, action, form, etc. Maze+XML will only use
    links in this example.
    """

    def __init__(self, rel, href):
        self.rel = rel
        self.href = href
