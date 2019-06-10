import abc
import yaml
import logging
import os

class BaseFetcher(abc.ABC):

    CONFIG_FILE_NAME = "illustrations/fetchers/fetcher_config.yaml"

    @abc.abstractmethod
    def fetch(self):
        pass

    def get_config(self):
        with open(BaseFetcher.CONFIG_FILE_NAME, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)

    def log(self, *messages):
        message = ''.join([str(x) for x in ([type(self).__name__, " - "] + list(messages))])
        logging.info(message)

    def log_warn(self, *messages):
        message = ''.join([str(x) for x in ([type(self).__name__, " - "] + list(messages))])
        logging.warning(message)

    def file_extension_from_image_url(self, url):
        url_basename = os.path.basename(url)
        extension = os.path.splitext(url_basename)[1][1:]
        return extension