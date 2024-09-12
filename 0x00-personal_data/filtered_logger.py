#!/usr/bin/env python3

""" Module for handling personal data """

import re


def filter_datum(fields: set, redaction: str, message: str,
                 separator: str) -> str:
    """ a function to obfuscate the important data """
    regex = re.compile(
        '|'.join([f'{field}=[^{separator}]+' for field in fields]))
    return regex.sub(
        lambda match: f'{match.group(0).split("=")[0]}={redaction}', message)
