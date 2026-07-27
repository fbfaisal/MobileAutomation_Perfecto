from pprint import pprint

from libraries.ConfigReader import ConfigReader
from libraries.ValidationManager import ValidationManager


config = ConfigReader()
validation = ValidationManager()

pprint(config.get_runtime_config())
pprint(config.get_device_config())
pprint(config.get_application_config())
pprint(config.get_perfecto_config())
pprint(config.get_execution_config())

validation.validate_all()

print("All parameterized configuration values are valid.")