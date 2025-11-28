import logging
from core.settings import settings

def get_logger():
    logger = logging.getLogger("NomadV15")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(settings.LOG_PATH)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

logger = get_logger()
