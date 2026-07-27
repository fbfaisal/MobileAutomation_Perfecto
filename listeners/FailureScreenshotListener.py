from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class FailureScreenshotListener:
    """
    Robot Framework listener that automatically captures
    a screenshot when a test fails.
    """

    ROBOT_LISTENER_API_VERSION = 3

    def end_test(self, data, result) -> None:
        """
        Capture a failure screenshot after a failed test.
        """

        if result.status != "FAIL":
            return

        test_name = result.name

        logger.warn(
            f"Test failed. Attempting to capture screenshot: "
            f"{test_name}"
        )

        try:
            mobile_library = (
                BuiltIn().get_library_instance(
                    "MobileLibrary"
                )
            )

            driver = mobile_library.driver_factory.driver

            if driver is None:
                logger.warn(
                    "Failure screenshot was not captured "
                    "because no active Appium driver exists."
                )
                return

            screenshot_path = (
                mobile_library
                .screenshot_library
                .capture_failure_screenshot(
                    test_name=test_name,
                    driver=driver,
                )
            )

            logger.info(
                f"Failure screenshot captured: "
                f"{screenshot_path}",
                also_console=True,
            )

        except RuntimeError as error:
            logger.warn(
                "Failure screenshot could not be captured: "
                f"{error}"
            )

        except Exception as error:
            logger.warn(
                "Unexpected error while capturing the "
                f"failure screenshot: {error}"
            )