import requests

class HypermediaClient:

    def __init__(self, resource):
        self.resource = resource

    def headers(self):
        media_types = self.resource.adapters.get_media_types()
        return { 'Accept': ",".join(media_types) }

    def follow(self, link):
        """
        Follows a link using a GET request
        """
        print link
        response = requests.get(url=link, headers=self.headers())
        media_type = response.headers.get('content-type').split('; ')[0]
        representer = self.resource.translate_from(media_type, response.text)
        return representer

