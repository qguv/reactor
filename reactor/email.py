#!/usr/bin/env python3

import re

# FIXME
def send(to, contents):
    print(f"Email to {to}:")
    print(contents)


def mask(address):
    username, _, domain = address.partition('@')
    username_masked = ''.join('*' if i else c for i, c in enumerate(username))
    return '@'.join([username_masked, domain])
