import pickle
import logging

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

    def present_images(self):
        pass

    def missing_images(self):
        pass

    def healthy_images(self):
        present_images = self.present_images()

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
                                    completed_download.tags) for completed_download in completed_downloads]

        for illustration in new_illustrations:
            illustration.save_index_id_to_file()

        self.upsert_illustration_list(new_illustrations)



    def get_illustration_by_id(self, illustration_id):
        return self.data.get(illustration_id)
