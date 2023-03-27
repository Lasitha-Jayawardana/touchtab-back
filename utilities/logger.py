import logging


# TODO
def setup_logger():
    logger = logging.getLogger('CRM-server')
    logger.setLevel(logging.DEBUG)

    hipster_format = logging.Formatter(
        '%(asctime)s %(levelname)10s %(thread)d --- [%(name)10s] %(module)20s.%(funcName)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(hipster_format)
    logger.addHandler(ch)

    return logger


logger = setup_logger()
extra = {'app_name': "{}".format("test-CRM"), "app_port": "5000"}
