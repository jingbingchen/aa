import logging


class BaseLogging(object):
    """
    log 基础类
    """

    def __init__(self, level, is_console=True):
        logging.basicConfig(filename='log/' + __name__ + '.log',
                            format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=level,
                            filemode='a', datefmt='%Y-%m-%d%I:%M:%S %p')
        self.log = logging.getLogger()
        if is_console:
            self.log.addHandler(logging.StreamHandler())

    def debug(self, msg, *args):
        if self.log.level == logging.DEBUG:
            self.log.debug(msg.format(*args))

    def info(self, msg, *args):
        if self.log.level == logging.INFO:
            self.log.info(msg.format(*args))

    def warning(self, msg, *args):
        self.log.warning(msg.format(*args))

    def error(self, msg, *args):
        self.log.error(msg.format(*args))


log = BaseLogging(logging.INFO)