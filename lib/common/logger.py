import logging


class Logger:

    def __init__(self, name):
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter('[%(levelname)s] %(name)s - %(message)s'))
        self.logger = logging.getLogger(name)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False
        self.name = name

        self.set_level(logging.INFO)

    def set_level(self, level):
        self.handler.setLevel(level)
        self.logger.setLevel(level)

    def debug(self , msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
