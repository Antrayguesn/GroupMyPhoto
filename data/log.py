import logging

logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG, format="")

INFO_RUN_STRATEGY = "INFO_0001"
INFO_LOADING_DATA = "INFO_0002"
INFO_PROCESSING_DATA = "INFO_0003"
INFO_WRITING_DATA = "INFO_0004"
INFO_END_PROCESS = "INFO_0005"
INFO_LOADING_PHOTO = "INFO_0006"

INFO_RUN_STRATEGIES = "INFO_0007"

DEBUG_UNABLE_TO_FIND_CENTROID = "DEBUG_000"
DEBUG_PHOTO_ALREADY_EXIST = "DEBUG_0001"
DEBUG_PHOTO_ALREADY_DELETED = "DEBUG_002"
DEBUG_NO_CENTROID = "DEBUG_003"
DEBUG_NO_KEY_COORD = "DEBUG_004"

WARNING_UNEXECPT_ERROR = "WARNING_0001"


def log(code, msg, service_code=None, **kwargs):
    severity = code.split("_")[0]
    json_log = {"CODE": code, "MSG": msg, "SEVERITY": severity, "SERVICE_CODE": service_code, **kwargs}
    if severity == "INFO":
        logger.info(json_log)
    elif severity == "DEBUG":
        logger.debug(json_log)
    elif severity == "ERROR":
        logger.error(json_log)
    elif severity == "WARNING":
        logger.warning(json_log)
