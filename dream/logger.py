import logging

import coloredlogs


def build_logger(name, level=logging.WARNING):
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.setLevel(level)

    coloredlogs.install(fmt='[%(levelname)s] %(asctime)s %(name)s: %(message)s', level=level)

    return logger
