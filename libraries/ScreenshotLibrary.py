import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from appium.webdriver.webdriver import WebDriver
from robot.api import logger


class ScreenshotLibrary:
    """
    Handles screenshot capture for Appium mobile sessions.

    The screenshot directory can be supplied through:

        SCREENSHOT_DIRECTORY

    Example:

        $env:SCREENSHOT_DIRECTORY = "reports/screenshots"
    """

    def __init__(
        self,
        driver: Optional[WebDriver] = None,
        screenshot_directory: Optional[str] = None,
    ) -> None:
        self.driver = driver
        self.screenshot_directory = (
            screenshot_directory
            or os.getenv("SCREENSHOT_DIRECTORY")
        )

    def set_driver(self, driver: WebDriver) -> None:
        """
        Set or replace the active Appium driver.
        """

        if driver is None:
            raise ValueError(
                "Cannot set screenshot driver because "
                "the provided driver is None."
            )

        self.driver = driver

    def clear_driver(self) -> None:
        """
        Remove the stored driver reference.
        """

        self.driver = None

    def capture_screenshot(
        self,
        name: str = "mobile_screenshot",
        driver: Optional[WebDriver] = None,
    ) -> str:
        """
        Capture a screenshot and return its absolute path.

        A driver supplied to this method takes priority over
        the driver previously supplied through set_driver().
        """

        active_driver = driver or self.driver

        self._validate_driver(active_driver)

        screenshot_directory = (
            self._get_screenshot_directory()
        )

        screenshot_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        safe_name = self._sanitize_filename(name)
        timestamp = self._generate_timestamp()

        file_name = (
            f"{safe_name}_{timestamp}.png"
        )

        file_path = (
            screenshot_directory / file_name
        ).resolve()

        try:
            screenshot_saved = (
                active_driver.save_screenshot(
                    str(file_path)
                )
            )

        except Exception as error:
            raise RuntimeError(
                "Unable to capture mobile screenshot. "
                f"Requested path: {file_path}"
            ) from error

        if screenshot_saved is False:
            raise RuntimeError(
                "The Appium driver reported that the "
                "screenshot was not saved. "
                f"Requested path: {file_path}"
            )

        logger.info(
            f"Mobile screenshot saved: {file_path}",
            also_console=True,
        )

        return str(file_path)

    def capture_failure_screenshot(
        self,
        test_name: str,
        driver: Optional[WebDriver] = None,
    ) -> str:
        """
        Capture a screenshot using a failure-specific name.
        """

        safe_test_name = (
            self._sanitize_filename(test_name)
        )

        screenshot_name = (
            f"FAILED_{safe_test_name}"
        )

        return self.capture_screenshot(
            name=screenshot_name,
            driver=driver,
        )

    def get_screenshot_directory(self) -> str:
        """
        Return the resolved screenshot directory.
        """

        return str(
            self._get_screenshot_directory()
            .resolve()
        )

    def _get_screenshot_directory(self) -> Path:
        """
        Resolve the configured screenshot directory.
        """

        directory = self.screenshot_directory

        if directory is None:
            raise RuntimeError(
                "Screenshot directory is not configured. "
                "Set the SCREENSHOT_DIRECTORY environment "
                "variable or pass screenshot_directory to "
                "ScreenshotLibrary."
            )

        directory_value = str(directory).strip()

        if not directory_value:
            raise RuntimeError(
                "Screenshot directory cannot be empty. "
                "Set SCREENSHOT_DIRECTORY to a valid path."
            )

        return Path(directory_value)

    @staticmethod
    def _validate_driver(
        driver: Optional[WebDriver],
    ) -> None:
        """
        Validate that a driver is available.
        """

        if driver is None:
            raise RuntimeError(
                "Cannot capture a screenshot because "
                "no active Appium driver is available."
            )

        if not hasattr(driver, "save_screenshot"):
            raise TypeError(
                "The provided driver does not support "
                "save_screenshot()."
            )

    @staticmethod
    def _sanitize_filename(name: object) -> str:
        """
        Convert a test or screenshot name into a safe filename.
        """

        value = str(name).strip()

        if not value:
            value = "mobile_screenshot"

        sanitized_value = re.sub(
            r'[<>:"/\\|?*\x00-\x1F]',
            "_",
            value,
        )

        sanitized_value = re.sub(
            r"\s+",
            "_",
            sanitized_value,
        )

        sanitized_value = re.sub(
            r"_+",
            "_",
            sanitized_value,
        )

        sanitized_value = (
            sanitized_value
            .strip(" ._")
        )

        if not sanitized_value:
            return "mobile_screenshot"

        return sanitized_value[:150]

    @staticmethod
    def _generate_timestamp() -> str:
        """
        Generate a timestamp containing milliseconds.
        """

        return (
            datetime.now()
            .strftime("%Y%m%d_%H%M%S_%f")[:-3]
        )