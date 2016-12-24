import logging.config


if __name__ == "__main__":
    logging.config.fileConfig("logging.conf")
    #logger = logging.getLogger("root")

    logging.debug("It's logging")