from common.named_logger import NamedLogger
from illustrations.index import Index
import os
from shutil import copyfile


class Slideshow(NamedLogger):

    def __init__(self, conf_filename):
        self.conf_filename = conf_filename
        self.set_logging_name("Conf file ("+conf_filename+")")
        with open(conf_filename) as show_file:
            self.yaql_query = show_file.read()


    def compute_illustration_list(self):
        index = Index.get_or_create_instance()
        return index.yaql_query(self.yaql_query)

    def write_slideshow(self):
        output_dir_name = self.conf_filename +'_slideshow'
        if os.path.exists(output_dir_name):
            self.log_warn("Aborting writing slideshow because of existing directory ", output_dir_name)
        else:
            self.log("Creating output directory", output_dir_name)
            os.mkdir(output_dir_name)
            illustrations = self.compute_illustration_list()
            for illustration in illustrations:
                copyfile(illustration.location, os.path.join(output_dir_name, illustration.location))
















