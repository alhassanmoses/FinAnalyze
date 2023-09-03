"""
dependencies.sharedutils.api_messages

By default, uses `en-gb.json` file inside the `API_MESSAGES` top-level folder.

If language changes, set `dependencies.sharedutils.api_messages.default_locale` and run `dependencies.sharedutils.api_messages.refresh()`.
"""
import json
import os
import logging

default_locale = "en-gb"
cached_messages = {}


def refresh():
    logging.info("Refreshing API response language...")

    global cached_messages
    with open(f"{os.getcwd()}/API_MESSAGES/{default_locale}.json") as f:
        cached_messages = json.load(f)


def gettext(name):  # TODO: switch from a manual translation approach to using Babel
    return cached_messages[name]


refresh()
