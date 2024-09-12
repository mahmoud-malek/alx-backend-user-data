#!/usr/bin/env python3
""" a module that contain a filter for logger """

import re
from typing import List


def filter_datum(fields: Lis[str], redaction: str,
                 message: str, separator: str) -> str:
    """ a filter to obfuscate the important data """
    for key in fields:
        message = re.sub(rf"{key}=.+?{separator}",
                         f"{key}={redaction}{separator}", message)
    return message
