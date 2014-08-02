import requests

def get_accept_header(translator):
    media_types = translator.adapters.keys()
    return ",".join(media_types)

class HypermediaClient:

    def __init__(self, translator):
        # The accept header is derived from what the translator can understand
        self.accept_header = get_accept_header(translator)

    def headers(self):
        return { 'Accept': self.accept_header }

    def follow(self, link):
        """
        Follows a link using a GET request
        """
        return requests.get(url=link.href, headers=self.headers())
