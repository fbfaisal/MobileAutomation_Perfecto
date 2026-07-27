from typing import Optional

from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.webdriver import WebDriver

from libraries.CapabilityManager import CapabilityManager
from libraries.ConfigReader import ConfigReader


class DriverFactory:
    """
    Creates and manages Appium driver sessions.

    Supported execution providers:
    - LOCAL
    - PERFECTO
    """

    def __init__(self) -> None:
        self.config_reader = ConfigReader()
        self.capability_manager = CapabilityManager()
        self.driver: Optional[WebDriver] = None

    def create_driver(self) -> WebDriver:
        """
        Create a driver using the configured execution provider.
        """

        if self.driver is not None:
            return self.driver

        runtime_config = self.config_reader.get_runtime_config()

        execution_provider = self._normalize(
            runtime_config.get("execution_provider")
        )

        capabilities = self.capability_manager.get_capabilities()
        endpoint = self._get_endpoint(execution_provider)

        options = AppiumOptions()
        options.load_capabilities(capabilities)

        try:
            self.driver = webdriver.Remote(
                command_executor=endpoint,
                options=options,
            )

            return self.driver

        except Exception as error:
            self.driver = None

            raise RuntimeError(
                f"Unable to create Appium driver using "
                f"provider '{execution_provider}' and "
                f"endpoint '{endpoint}'."
            ) from error

    def _get_endpoint(self, execution_provider: str) -> str:
        """
        Return the Appium endpoint for the selected provider.
        """

        if execution_provider == "LOCAL":
            return self._get_local_endpoint()

        if execution_provider == "PERFECTO":
            return self._get_perfecto_endpoint()

        raise ValueError(
            f"Unsupported execution provider: "
            f"'{execution_provider}'."
        )

    def _get_local_endpoint(self) -> str:
        """
        Return the local Appium server endpoint.

        LOCAL_APPIUM_URL may be supplied through an environment
        variable resolved by the configuration layer.
        """

        execution_config = (
            self.config_reader.get_execution_config()
        )

        local_endpoint = execution_config.get(
            "local_appium_url"
        )

        if not self._has_value(local_endpoint):
            raise ValueError(
                "Missing local Appium endpoint. Set "
                "LOCAL_APPIUM_URL before local execution."
            )

        return str(local_endpoint).strip()

    def _get_perfecto_endpoint(self) -> str:
        """
        Build the Perfecto Appium endpoint from the configured host.
        """

        perfecto_config = (
            self.config_reader.get_perfecto_config()
        )

        host = perfecto_config.get("host")

        if not self._has_value(host):
            raise ValueError(
                "Missing Perfecto configuration value: host"
            )

        normalized_host = (
            str(host)
            .strip()
            .removeprefix("https://")
            .removeprefix("http://")
            .rstrip("/")
        )

        return (
            f"https://{normalized_host}"
            "/nexperience/perfectomobile/wd/hub"
        )

    def get_driver(self) -> WebDriver:
        """
        Return the active driver instance.
        """

        if self.driver is None:
            raise RuntimeError(
                "Appium driver has not been created. "
                "Call create_driver() first."
            )

        return self.driver

    def quit_driver(self) -> None:
        """
        Close the current driver session safely.
        """

        if self.driver is None:
            return

        try:
            self.driver.quit()
        finally:
            self.driver = None

    @staticmethod
    def _normalize(value: object) -> str:
        if value is None:
            return ""

        return str(value).strip().upper()

    @staticmethod
    def _has_value(value: object) -> bool:
        if value is None:
            return False

        if isinstance(value, str):
            return bool(value.strip())

        return True