import abc
import yaml

class BaseFetcher(abc.ABC):

    CONFIG_FILE_NAME = "fetcher_config.yaml"

    @abc.abstractmethod
    def fetch(self):
        pass

    def get_config(self):
        with open(BaseFetcher.CONFIG_FILE_NAME, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)