import logging

class NamedLogger():

    def set_logging_name(self, name):
        self.logging_name = name

    def get_logging_name(self):
        if hasattr(self, 'logging_name'):
            return self.logging_name
        else:
            return type(self).__name__

    def log(self, *messages):
        message = ''.join([str(x) for x in ([self.get_logging_name(), " - "] + list(messages))])
        logging.info(message)

    def log_warn(self, *messages):
        message = ''.join([str(x) for x in ([self.get_logging_name(), " - "] + list(messages))])
        logging.warning(message)