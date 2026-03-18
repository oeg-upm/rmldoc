import logging


class LoggerRMLdoc:

    def __init__(self, logging_group, logging_stream):
        self.logging_group = logging_group
        self.logging_stream = logging_stream

        self.log = logging.getLogger("remote_logger")
        self.log.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

        self.log.handlers.clear()
        self.log.addHandler(ch)
