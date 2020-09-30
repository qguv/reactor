#!/usr/bin/env python3

import tomlkit

from pathlib import Path
from os import environ

_config = None


def xdg_config_home() -> Path:
    try:
        return Path(environ["XDG_CONFIG_HOME"])
    except KeyError:
        return Path(environ["HOME"]) / ".config"


def config_path_preferences(app_name):
    yield xdg_config_home() / app_name / "config.toml"
    yield Path("/etc") / app_name / "config.toml"
    yield Path(__file__).parent / "config.toml"


def config_path(app_name):
    paths = (path for path in config_path_preferences(app_name) if path.exists())
    return next(gen)


def read(app_name):
    if _config is None:
        _config = tomlkit.parse(config_path(app_name))
    return _config
