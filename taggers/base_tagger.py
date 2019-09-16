import abc
from common.named_logger import NamedLogger
from illustrations.index import Index


class BaseTagger(abc.ABC, NamedLogger):

    @abc.abstractmethod
    def compute_tags(self, illustration):
        pass

    def add_tags_to_illustrations(self, illustrations):
        self.log("Retagging illustration list of length ", len(illustrations))
        for illustration in illustrations:
            self.log("Computing tags for ", illustration.name)
            new_tags = self.compute_tags(illustration)
            self.log(new_tags)
            illustration.tags[self.SOURCE_NAME] = new_tags

        self.log("Saving retagged images...")
        Index.get_or_create_instance().upsert_illustration_list(illustrations)
        self.log("Done")
