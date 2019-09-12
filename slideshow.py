from common.named_logger import NamedLogger
from illustrations.index import Index
import os
from shutil import copyfile


class Slideshow(NamedLogger):

    def __init__(self, conf_filename):
        self.conf_filename = conf_filename
        self.set_logging_name("Conf file ("+conf_filename+")")
        try:
            with open(conf_filename+".txt") as show_file:
                self.yaql_query = show_file.read()

        except FileNotFoundError:
            self.log("Could not find "+conf_filename+".txt, trying "+conf_filename)
            try:
                with open(conf_filename) as show_file:
                    self.yaql_query = show_file.read()
            except FileNotFoundError:
                raise Exception("Could not find conf file "+conf_filename)


    def compute_illustration_list(self):
        index = Index.get_or_create_instance()
        return index.yaql_query(self.yaql_query)

    def write_slideshow(self):
        output_dir_name = self.conf_filename +'_slideshow'
        if os.path.exists(output_dir_name):
            self.log_warn("Aborting writing slideshow because of existing directory ", output_dir_name)
        else:
            illustrations = self.compute_illustration_list()
            if len(illustrations) == 0:
                self.log_warn("Aborting slideshow generation because no illustrations found for config ",
                              self.conf_filename)
            else:
                self.log("Creating output directory ", output_dir_name)
                os.mkdir(output_dir_name)
                for illustration in illustrations:
                    copyfile(illustration.location, os.path.join(output_dir_name, os.path.split(illustration.location)[1]))

                self.log("Finished writing slideshow")
















