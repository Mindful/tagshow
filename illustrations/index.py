import pickle
import logging
import os

from . import illustration_file
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%H')


class Index:
    index_file_name = 'index_data.pickle'
    next_available_id_key = '_next_id'
    instance = None

    @staticmethod
    def get_or_create_instance():
        if Index.instance is None:
            fresh_instance = Index()
            Index.instance = fresh_instance

        return Index.instance

    def __init__(self):
        if Index.instance is not None:
            raise Exception("There should only be one instance of Index. Please use get_instance()")

        self._load()

    def _load(self):
        try:
            with open(self.index_file_name, 'rb') as data_file:
                self.data = pickle.load(data_file)
        except FileNotFoundError:
            self.data = {self.next_available_id_key: 1}
            self.save()

    def _illustration_id_keys(self):
        return [key for key in self.data.keys() if isinstance(key, int)]

    def present_illustrations(self):
        present_illustrations = []
        for key in self._illustration_id_keys():
            illustration = self.data[key]
            present = os.path.isfile(illustration.location)
            if present:
                present_illustrations.append(illustration)

        return present_illustrations

    def healthy_illustrations(self):
        healthy_illustrations = []
        present_illustrations = self.present_illustrations()
        for illustration in present_illustrations:
            healthy = True
            try:
                illustration.load_file_index_id()
            except Exception:
                healthy = False

            healthy = (healthy and (illustration.index_id == illustration.file_index_id))
            if (healthy):
                healthy_illustrations.append(illustration)

        return healthy_illustrations

    def present_ids_for_source(self, source):
        present_illustrations = self.present_illustrations()
        return set([illustration.source_id for illustration in present_illustrations if illustration.source == source])

    def verify(self):
        pass #TODO: look at all the images in our index, make sure we can find them by name (if not, find all images we don't know about, check them for metadata)

    def save(self):
        with open(self.index_file_name, 'wb') as data_file:
            pickle.dump(self.data, data_file)

    def _requisition_id_range(self, count):
        next_id = self.data[self.next_available_id_key]
        self.data[self.next_available_id_key] = next_id + count
        self.save()
        return range(next_id, next_id+count)

    def upsert_illustration(self, illustration):
        self.upsert_illustration_list(list(illustration))

    def upsert_illustration_list(self, illustration_list):
        for illustration in illustration_list:
            self.data[illustration.index_id] = illustration
        self.save()

    def register_new_illustration_file(self, file_location, initial_tags):
        return self.register_new_illustration_list([(file_location, initial_tags)])[0]

    def register_new_illustration_list(self, completed_downloads):
        id_iterator = iter(self._requisition_id_range(len(completed_downloads)))
        new_illustrations = [illustration_file.IllustrationFile(next(id_iterator), completed_download.name,
                    completed_download.source, completed_download.id, completed_download.tags_for_index())
                    for completed_download in completed_downloads]

        for illustration in new_illustrations:
            illustration.save_index_id_to_file()

        self.upsert_illustration_list(new_illustrations)



    def get_illustration_by_id(self, illustration_id):
        return self.data.get(illustration_id)