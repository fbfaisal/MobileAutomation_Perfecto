import os
import yaml
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn


@library(scope="GLOBAL", auto_keywords=False)
class LocatorReader:

    def __init__(self, locator_directory="resources/locators"):
        self.locator_directory = locator_directory

    @keyword("Get Locator")
    def get_locator(self, page_name, locator_name):
        platform = self._get_platform()

        file_path = os.path.join(
            self.locator_directory,
            f"{page_name}.yaml",
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Locator file not found: {file_path}"
            )

        with open(file_path, "r", encoding="utf-8") as file:
            locator_data = yaml.safe_load(file) or {}

        if locator_name not in locator_data:
            raise KeyError(
                f"Locator '{locator_name}' was not found in {file_path}"
            )

        platform_locators = locator_data[locator_name]

        if platform not in platform_locators:
            raise KeyError(
                f"No '{platform}' locator configured for "
                f"'{locator_name}' in {file_path}"
            )

        return platform_locators[platform]

    def _get_platform(self):
        platform = BuiltIn().get_variable_value("${PLATFORM}")

        if not platform:
            platform = os.getenv("PLATFORM")

        if not platform:
            raise ValueError(
                "PLATFORM is not configured. "
                "Set PLATFORM to android or ios."
            )

        platform = str(platform).strip().lower()

        if platform not in {"android", "ios"}:
            raise ValueError(
                f"Unsupported platform: {platform}"
            )

        return platform