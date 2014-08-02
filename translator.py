class Translator:

    def __init__(self, adapters={}):
        self.adapters = adapters

    def register(self, adapter):
        self.adapters[adapter.media_type] = adapter

    def translate_from(self, media_type, raw_representation):
        adapter = self.adapters[media_type]()
        return adapter.parse(raw_representation)
