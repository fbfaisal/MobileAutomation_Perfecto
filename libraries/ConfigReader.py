import os
import re
from pathlib import Path
from typing import Any

import yaml


class ConfigReader:
    ROBOT_VARIABLE_PATTERN = re.compile(r"\$\{([^}]+)}")

    def __init__(self, config_path: str | None = None):
        project_root = Path(__file__).resolve().parent.parent

        self.config_path = (
            Path(config_path).resolve()
            if config_path
            else project_root / "config"
        )

    def read_yaml(self, file_name: str) -> dict:
        file_path = self.config_path / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Configuration file was not found: {file_path}"
            )

        with file_path.open("r", encoding="utf-8") as file:
            raw_data = yaml.safe_load(file) or {}

        resolved_data = self._resolve_value(raw_data)

        if not isinstance(resolved_data, dict):
            raise ValueError(
                f"Configuration file must contain a YAML mapping: {file_path}"
            )

        return resolved_data

    def _resolve_value(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: self._resolve_value(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [self._resolve_value(item) for item in value]

        if isinstance(value, str):
            resolved = self._replace_environment_variables(value)
            return self._convert_type(resolved)

        return value

    def _replace_environment_variables(self, value: str) -> str:
        def replace(match: re.Match) -> str:
            variable_name = match.group(1)
            variable_value = os.getenv(variable_name)

            if variable_value is None:
                return ""

            return variable_value

        return self.ROBOT_VARIABLE_PATTERN.sub(replace, value)

    @staticmethod
    def _convert_type(value: str) -> Any:
        normalized = value.strip()

        if normalized.lower() == "true":
            return True

        if normalized.lower() == "false":
            return False

        if normalized.lower() in {"none", "null"}:
            return None

        if normalized.isdigit():
            return int(normalized)

        return normalized

    def get_runtime_config(self) -> dict:
        return self.read_yaml("runtime.yaml").get("runtime", {})

    def get_execution_config(self) -> dict:
        return self.read_yaml("execution.yaml").get("execution", {})

    def get_perfecto_config(self) -> dict:
        return self.read_yaml("perfecto.yaml").get("perfecto", {})

    def get_device_config(self) -> dict:
        return self.read_yaml("devices.yaml").get("devices", {}).get(
            "selected", {}
        )

    def get_application_config(self) -> dict:
        return self.read_yaml("applications.yaml").get(
            "applications", {}
        ).get("selected", {})

    def get_environment_config(self) -> dict:
        return self.read_yaml("environments.yaml").get(
            "environments", {}
        ).get("selected", {})

    def get_logging_config(self) -> dict:
        return self.read_yaml("logging.yaml").get("logging", {})