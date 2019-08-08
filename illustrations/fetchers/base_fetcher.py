import abc
import yaml
import os
from common.named_logger import NamedLogger


class BaseFetcher(abc.ABC, NamedLogger):

    CONFIG_FILE_NAME = "illustrations/fetchers/fetcher_config.yaml"

    @abc.abstractmethod
    def fetch(self, max_count=None):
        pass

    def get_config(self):
        with open(BaseFetcher.CONFIG_FILE_NAME, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

    def file_extension_from_image_url(self, url):
        url_basename = os.path.basename(url)
        extension = os.path.splitext(url_basename)[1][1:]
        return extension