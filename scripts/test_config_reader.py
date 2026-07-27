import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from libraries.ConfigReader import ConfigReader


config = ConfigReader()

print(config.get_execution_config())
print(config.get_device_config("android"))
print(config.get_application_config("bank_app"))