
class IllustrationDownload:

    def __init__(self, source, source_id, url, file_extension, tags, metadata={}, name=None):
        if name:
            self.name = name
        else:
            self.name = '{}_{}.{}'.format(source, str(source_id), file_extension)

        self.source = source
        self.id = source_id
        self.metadata = metadata
        self.raw_tags = tags
        self.url = url

    def tags_for_index(self):
        result = {}
        if len(self.metadata) > 0:
            result['download_metadata'] = self.metadata

        result[self.source] = self.raw_tags
        return result

    def __str__(self):
        return "({}, {})".format(self.url, self.metadata)