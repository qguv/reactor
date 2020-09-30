import xdg_toml_config

__version__ = '0.1.0'
app_name = 'reactor'
config = xdg_toml_config.read(app_name)
