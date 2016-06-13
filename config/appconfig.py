import os
import yaml


## load config files
DEFAULT_CONFIG_FILE = "default_config.yaml"
CONFIG_FILE = "config.yaml"

appconfig = {}

# load default config
appconfig.update(yaml.safe_load(open(DEFAULT_CONFIG_FILE)))

# override with user config:
if os.path.exists(CONFIG_FILE):
    appconfig.update(yaml.safe_load(open(CONFIG_FILE)))
