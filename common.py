import json
from types import SimpleNamespace


def parseJson(dataJson: str) -> SimpleNamespace:
    """
    The function converts a string to a dictionary.

    :param dataJson: str
    :return: SimpleNamespace
    """
    return json.loads(dataJson, object_hook=lambda d: SimpleNamespace(**d))

