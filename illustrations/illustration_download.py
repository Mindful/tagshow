
class IllustrationDownload:

    def __init__(self, source, source_id, url, file_extension, tags, metadata={}, name=None):
        if name:
            self.name = name
        else:
            self.name = '{}_{}.{}'.format(source, str(source_id), file_extension)

        self.source = source
        self.id = source_id
        self.metadata = metadata
        self.tags = tags
        self.url = url
