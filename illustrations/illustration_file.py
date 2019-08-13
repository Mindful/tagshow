from libxmp import XMPFiles, consts, XMPError, XMPMeta
from yaql import yaqlization


@yaqlization.yaqlize(yaqlize_attributes=True)
class IllustrationFile:

    xmp_key = "IllustrationIndexId"

    def __init__(self, index_id, location, source, source_id, tags, metadata):
        self.index_id = index_id
        self.location = location
        self.tags = tags
        self.source = source
        self.source_id = source_id
        self.file_index_id = None
        self.metadata = metadata

    def add_image_tags(self, source, tag_map):
        pass

    def __str__(self):
        return "({}, {})".format(self.index_id, self.location)

    def __repr__(self):
        return str(self.__dict__)

    def load_file_index_id(self):
        xmp_file = XMPFiles(file_path=self.location, open_forupdate=False)
        try:
            xmp = xmp_file.get_xmp()
            if xmp is not None:
                id_string = xmp_file.get_xmp().get_property(consts.XMP_NS_DC, self.xmp_key)
                self.file_index_id = int(id_string)
        except XMPError:
            raise Exception("Could not load index id from file for {}".format(self))

        xmp_file.close_file()

    def save_index_id_to_file(self):
        xmp_file = XMPFiles(file_path=self.location, open_forupdate=True)
        xmp = xmp_file.get_xmp()
        if xmp is None:
            xmp = XMPMeta()

        xmp.set_property(consts.XMP_NS_DC, self.xmp_key, str(self.index_id))
        if xmp_file.can_put_xmp(xmp):
            xmp_file.put_xmp(xmp)
            xmp_file.close_file()
        else:
            xmp_file.close_file()
            raise Exception("Could not write index id to file for {}".format(self))

    def get_tag_set(self, exclude_sources = []):
        result = set()
        acceptable_sources = [source for source in self.tags if source not in exclude_sources]
        for source in acceptable_sources:
            tags = self.tags[source]
            result |= tags

        return result


