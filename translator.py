class Translator:

    def __init__(self, adapters={}):
        self.adapters = adapters

    def register(self, adapter):
        self.adapters[adapter.media_type] = adapter

    def translate_from(self, media_type, raw_representation):
        adapter = self.adapters[media_type](adapters=self.adapters)
        return adapter.parse(raw_representation)
