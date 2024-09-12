#!/usr/bin/env python3

""" Module for handling personal data """

import re


def filter_datum(fields: set, redaction: str, message: str,
                 separator: str) -> str:
    """ a function to obfuscate the important data """
    pattern = '|'.join([f'{field}=[^{separator}]+' for field in fields])
    return re.sub(
        pattern, lambda match: f'{match.group(0).split("=")[0]}={redaction}', message)
