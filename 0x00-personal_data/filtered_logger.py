#!/usr/bin/env python3
""" a module that contain a filter for logger """

import re


def filter_datum(fields, redaction, message, separator):
    """ a filter to obfuscate the important data """
    pattern = '|'.join([f'{field}=[^{separator}]+' for field in fields])
    return re.sub(pattern,
                  lambda match: f'{match.group(0).split("=")[0]}={redaction}',
                  message)
