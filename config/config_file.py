import yaml


## load config files
DEFAULT_CONFIG_FILE = "default_config.yaml"

appconfig = {}

# load default config
appconfig.update(yaml.safe_load(open(DEFAULT_CONFIG_FILE)))

