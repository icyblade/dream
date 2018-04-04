import logging


def build_logger(name, level=logging.WARNING):
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.setLevel(level)

    try:
        import coloredlogs
        coloredlogs.install(fmt='[%(levelname)s] %(asctime)s %(name)s: %(message)s', level=level)
    except ImportError:
        pass

    return logger
