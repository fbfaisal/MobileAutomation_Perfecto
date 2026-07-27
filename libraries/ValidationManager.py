from libraries.ConfigReader import ConfigReader


class ValidationManager:
    """
    Validates runtime, device, application, and provider-specific
    configuration before driver creation.
    """

    SUPPORTED_PROVIDERS = {
        "LOCAL",
        "PERFECTO",
    }

    SUPPORTED_PLATFORMS = {
        "ANDROID",
        "IOS",
    }

    def __init__(self) -> None:
        self.config_reader = ConfigReader()

    def validate_runtime_config(self) -> bool:
        runtime = self.config_reader.get_runtime_config()

        required_fields = (
            "execution_provider",
            "platform",
            "environment",
            "application",
            "device",
        )

        missing_fields = [
            field
            for field in required_fields
            if not self._has_value(runtime.get(field))
        ]

        if missing_fields:
            raise ValueError(
                "Missing runtime configuration values: "
                f"{missing_fields}"
            )

        self.validate_execution_provider(
            runtime.get("execution_provider")
        )

        self.validate_platform(
            runtime.get("platform")
        )

        return True

    def validate_execution_provider(
        self,
        execution_provider: str,
    ) -> bool:
        normalized_provider = self._normalize(
            execution_provider
        )

        if normalized_provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(
                "Unsupported execution provider: "
                f"'{execution_provider}'. "
                "Supported providers are: "
                f"{sorted(self.SUPPORTED_PROVIDERS)}"
            )

        return True

    def validate_platform(
        self,
        platform: str,
    ) -> bool:
        normalized_platform = self._normalize(platform)

        if normalized_platform not in self.SUPPORTED_PLATFORMS:
            raise ValueError(
                f"Unsupported platform: '{platform}'. "
                "Supported platforms are: "
                f"{sorted(self.SUPPORTED_PLATFORMS)}"
            )

        return True

    def validate_perfecto_config(self) -> bool:
        perfecto = self.config_reader.get_perfecto_config()

        required_fields = (
            "host",
            "security_token",
        )

        missing_fields = [
            field
            for field in required_fields
            if not self._has_value(perfecto.get(field))
        ]

        if missing_fields:
            raise ValueError(
                "Missing Perfecto configuration values: "
                f"{missing_fields}"
            )

        return True

    def validate_device_config(self) -> bool:
        device = self.config_reader.get_device_config()

        required_fields = (
            "platform_name",
            "automation_name",
            "device_name",
        )

        missing_fields = [
            field
            for field in required_fields
            if not self._has_value(device.get(field))
        ]

        if missing_fields:
            raise ValueError(
                "Missing device configuration values: "
                f"{missing_fields}"
            )

        runtime = self.config_reader.get_runtime_config()

        runtime_platform = self._normalize(
            runtime.get("platform")
        )

        device_platform = self._normalize(
            device.get("platform_name")
        )

        if runtime_platform != device_platform:
            raise ValueError(
                "Platform mismatch between runtime and device "
                "configuration. "
                f"Runtime platform: '{runtime.get('platform')}', "
                f"device platform: "
                f"'{device.get('platform_name')}'."
            )

        return True

    def validate_application_config(self) -> bool:
        application = (
            self.config_reader
            .get_application_config()
        )

        if not self._has_value(
            application.get("app_path")
        ):
            raise ValueError(
                "Missing application configuration value: "
                "app_path"
            )

        self._validate_application_extension(
            application.get("app_path")
        )

        return True

    def validate_all(self) -> bool:
        self.validate_runtime_config()
        self.validate_device_config()
        self.validate_application_config()

        runtime = self.config_reader.get_runtime_config()

        execution_provider = self._normalize(
            runtime.get("execution_provider")
        )

        if execution_provider == "PERFECTO":
            self.validate_perfecto_config()

        return True

    def _validate_application_extension(
        self,
        app_path: str,
    ) -> bool:
        runtime = self.config_reader.get_runtime_config()

        platform = self._normalize(
            runtime.get("platform")
        )

        normalized_app_path = str(
            app_path
        ).strip().lower()

        if platform == "ANDROID":
            valid_extensions = (
                ".apk",
                ".aab",
            )

            if not normalized_app_path.endswith(
                valid_extensions
            ):
                raise ValueError(
                    "Android execution requires an application "
                    "path ending in '.apk' or '.aab'. "
                    f"Received: '{app_path}'"
                )

        elif platform == "IOS":
            if not normalized_app_path.endswith(".ipa"):
                raise ValueError(
                    "iOS execution requires an application "
                    "path ending in '.ipa'. "
                    f"Received: '{app_path}'"
                )

        return True

    @staticmethod
    def _has_value(value: object) -> bool:
        if value is None:
            return False

        if isinstance(value, str):
            return bool(value.strip())

        return True

    @staticmethod
    def _normalize(value: object) -> str:
        if value is None:
            return ""

        return str(value).strip().upper()