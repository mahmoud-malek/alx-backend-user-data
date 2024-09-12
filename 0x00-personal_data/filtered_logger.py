#!/usr/bin/env python3
""" a module that contain a filter for logger """

import re
from typing import List


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """ a filter to obfuscate the important data """
    pattern = '|'.join([f'{field}=[^{separator}]+' for field in fields])
    return re.sub(pattern,
                  lambda match: f'{match.group(0).split("=")[0]}={redaction}',
                  message)
