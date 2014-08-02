import requests

def get_accept_header(translator):
    media_types = translator.adapters.keys()
    return ",".join(media_types)

class HypermediaClient:

    def __init__(self, translator):
        # The accept header is derived from what the translator can understand
        self.translator = translator
        self.accept_header = get_accept_header(self.translator)

    def headers(self):
        return { 'Accept': self.accept_header }

    def follow(self, link):
        """
        Follows a link using a GET request
        """
        response = requests.get(url=link, headers=self.headers())
        media_type = response.headers.get('content-type').split('; ')[0]
        representer = self.translator.translate_from(media_type, response.text)
        return representer

