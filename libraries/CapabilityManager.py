from typing import Any

from libraries.ConfigReader import ConfigReader
from libraries.ValidationManager import ValidationManager


class CapabilityManager:
    """Builds provider-specific Appium capabilities."""

    def __init__(self) -> None:
        self.config_reader = ConfigReader()
        self.validation = ValidationManager()

    def get_capabilities(self) -> dict[str, Any]:
        self.validation.validate_all()

        runtime_config = self.config_reader.get_runtime_config()
        device_config = self.config_reader.get_device_config()
        application_config = self.config_reader.get_application_config()

        execution_provider = (
            runtime_config
            .get("execution_provider", "")
            .strip()
            .upper()
        )

        capabilities = {
            "platformName": (
                device_config.get("platform_name")
                or runtime_config.get("platform")
            ),
            "appium:automationName": (
                device_config.get("automation_name")
            ),
            "appium:deviceName": (
                device_config.get("device_name")
                or runtime_config.get("device")
            ),
            "appium:platformVersion": (
                device_config.get("platform_version")
            ),
            "appium:app": (
                application_config.get("app_path")
            ),
            "appium:appPackage": (
                application_config.get("package_name")
            ),
            "appium:appActivity": (
                application_config.get("activity_name")
            ),
            "appium:bundleId": (
                application_config.get("bundle_id")
            ),
        }

        if execution_provider == "PERFECTO":
            perfecto_config = (
                self.config_reader.get_perfecto_config()
            )

            capabilities.update(
                {
                    "perfecto:securityToken": (
                        perfecto_config.get("security_token")
                    ),
                    "perfecto:deviceName": (
                        device_config.get("device_name")
                        or runtime_config.get("device")
                    ),
                }
            )

        return self._remove_empty_capabilities(capabilities)

    @staticmethod
    def _remove_empty_capabilities(
        capabilities: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            key: value
            for key, value in capabilities.items()
            if value is not None and value != ""
        }

    def get_masked_capabilities(self) -> dict[str, Any]:
        capabilities = self.get_capabilities().copy()

        token_key = "perfecto:securityToken"

        if token_key in capabilities:
            capabilities[token_key] = "********"

        return capabilities