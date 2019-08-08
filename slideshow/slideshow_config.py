import yaml
from common.named_logger import NamedLogger
from illustrations.index import Index


class SlideshowConfig(NamedLogger):


    INCLUDE_ILLUSTRATIONS = 'include_illustrations'
    EXCLUDE_ILLUSTRATIONS = 'exclude_illustrations'
    INCLUDE_TAGS = 'include_tags'
    REQUIRED_TAGS = 'required_tags'
    EXCLUDE_TAGS = 'exclude_tags'
    EXCLUDE_TAG_SOURCES = 'exclude_tag_sources'

    RECOGNIZED_CONFIGS = [INCLUDE_ILLUSTRATIONS, EXCLUDE_ILLUSTRATIONS, INCLUDE_TAGS, EXCLUDE_TAGS, EXCLUDE_TAG_SOURCES,
                          REQUIRED_TAGS]

    def __init__(self, conf_filename):
        self.conf_filename = conf_filename
        self.set_logging_name("Conf file ("+conf_filename+")")
        self.conf_values = []
        with open(conf_filename, 'r') as yaml_file:
            conf_file = yaml.safe_load(yaml_file)
            for key in conf_file:
                if key not in SlideshowConfig.RECOGNIZED_CONFIGS:
                    self.log("Found unrecognized config argument: ", key)
                else:
                    self.conf_values[key] = conf_file[key]


    def compute_illustration_list(self):
        index = Index.get_or_create_instance()
        result_list = [] #get all included tags








