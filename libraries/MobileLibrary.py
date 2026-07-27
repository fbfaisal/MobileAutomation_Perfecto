from typing import Optional, Tuple

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from robot.api.deco import keyword, library
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from libraries.DriverFactory import DriverFactory
from libraries.ScreenshotLibrary import ScreenshotLibrary


@library(scope="SUITE", auto_keywords=False)
class MobileLibrary:
    """
    Robot Framework library for mobile session management,
    screenshots, waits, element interactions, and validations.

    Supported execution providers:
    - LOCAL
    - PERFECTO
    """

    def __init__(self) -> None:
        self.driver_factory = DriverFactory()
        self.screenshot_library = ScreenshotLibrary()
        self.ROBOT_LIBRARY_LISTENER = self

    # ------------------------------------------------------------------
    # Session management
    # ------------------------------------------------------------------

    @keyword("Open Mobile Application")
    def open_mobile_application(self) -> None:
        """
        Create a new Appium driver session and pass the active
        driver to ScreenshotLibrary.
        """

        driver = self.driver_factory.create_driver()
        self.screenshot_library.set_driver(driver)

    @keyword("Close Mobile Application")
    def close_mobile_application(self) -> None:
        """
        Close the active Appium driver session and clear the
        driver reference from ScreenshotLibrary.
        """

        try:
            self.driver_factory.quit_driver()
        finally:
            self.screenshot_library.clear_driver()

    @keyword("Get Mobile Driver")
    def get_mobile_driver(self) -> WebDriver:
        """
        Return the active Appium driver.

        Raises an error when no active driver exists.
        """

        return self.driver_factory.get_driver()

    @keyword("Mobile Session Should Be Active")
    def mobile_session_should_be_active(self) -> None:
        """
        Fail if no mobile driver session is active.
        """

        if self._get_optional_driver() is None:
            raise AssertionError(
                "Expected an active mobile session, "
                "but no Appium driver exists."
            )

    @keyword("Mobile Session Should Not Be Active")
    def mobile_session_should_not_be_active(self) -> None:
        """
        Fail if a mobile driver session is active.
        """

        if self._get_optional_driver() is not None:
            raise AssertionError(
                "Expected no active mobile session, "
                "but an Appium driver exists."
            )

    # ------------------------------------------------------------------
    # Wait keywords
    # ------------------------------------------------------------------

    @keyword("Wait Until Element Is Visible")
    def wait_until_element_is_visible(
        self,
        locator: str,
        timeout: object = 20,
    ) -> WebElement:
        """
        Wait until an element is visible and return it.

        Robot example:

            Wait Until Element Is Visible
            ...    accessibility_id=Login
            ...    20
        """

        driver = self.get_mobile_driver()
        resolved_locator = self._get_locator(locator)
        timeout_value = self._convert_timeout(timeout)

        try:
            return WebDriverWait(
                driver,
                timeout_value,
            ).until(
                EC.visibility_of_element_located(
                    resolved_locator
                )
            )

        except TimeoutException as error:
            raise AssertionError(
                f"Element was not visible within "
                f"{timeout_value} seconds: {locator}"
            ) from error

    @keyword("Wait Until Element Is Clickable")
    def wait_until_element_is_clickable(
        self,
        locator: str,
        timeout: object = 20,
    ) -> WebElement:
        """
        Wait until an element is clickable and return it.
        """

        driver = self.get_mobile_driver()
        resolved_locator = self._get_locator(locator)
        timeout_value = self._convert_timeout(timeout)

        try:
            return WebDriverWait(
                driver,
                timeout_value,
            ).until(
                EC.element_to_be_clickable(
                    resolved_locator
                )
            )

        except TimeoutException as error:
            raise AssertionError(
                f"Element was not clickable within "
                f"{timeout_value} seconds: {locator}"
            ) from error

    @keyword("Wait Until Element Is Not Visible")
    def wait_until_element_is_not_visible(
        self,
        locator: str,
        timeout: object = 20,
    ) -> None:
        """
        Wait until an element is no longer visible.
        """

        driver = self.get_mobile_driver()
        resolved_locator = self._get_locator(locator)
        timeout_value = self._convert_timeout(timeout)

        try:
            WebDriverWait(
                driver,
                timeout_value,
            ).until(
                EC.invisibility_of_element_located(
                    resolved_locator
                )
            )

        except TimeoutException as error:
            raise AssertionError(
                f"Element remained visible after "
                f"{timeout_value} seconds: {locator}"
            ) from error

    # ------------------------------------------------------------------
    # Element interaction keywords
    # ------------------------------------------------------------------

    @keyword("Click Mobile Element")
    def click_mobile_element(
        self,
        locator: str,
        timeout: object = 20,
    ) -> None:
        """
        Wait until the element is clickable and click it.
        """

        element = self.wait_until_element_is_clickable(
            locator,
            timeout,
        )

        element.click()

    @keyword("Input Mobile Text")
    def input_mobile_text(
        self,
        locator: str,
        text: object,
        timeout: object = 20,
        clear_existing: object = True,
    ) -> None:
        """
        Enter text into a visible mobile element.

        By default, the existing value is cleared first.
        """

        element = self.wait_until_element_is_visible(
            locator,
            timeout,
        )

        if self._convert_to_boolean(clear_existing):
            element.clear()

        element.send_keys(str(text))

    @keyword("Clear Mobile Text")
    def clear_mobile_text(
        self,
        locator: str,
        timeout: object = 20,
    ) -> None:
        """
        Clear text from a visible mobile element.
        """

        element = self.wait_until_element_is_visible(
            locator,
            timeout,
        )

        element.clear()

    @keyword("Get Mobile Element Text")
    def get_mobile_element_text(
        self,
        locator: str,
        timeout: object = 20,
    ) -> str:
        """
        Return the text from a visible mobile element.
        """

        element = self.wait_until_element_is_visible(
            locator,
            timeout,
        )

        return element.text

    # ------------------------------------------------------------------
    # Verification keywords
    # ------------------------------------------------------------------

    @keyword("Mobile Element Should Be Visible")
    def mobile_element_should_be_visible(
        self,
        locator: str,
        timeout: object = 20,
    ) -> None:
        """
        Verify that an element becomes visible.
        """

        self.wait_until_element_is_visible(
            locator,
            timeout,
        )

    @keyword("Mobile Element Should Not Be Visible")
    def mobile_element_should_not_be_visible(
        self,
        locator: str,
        timeout: object = 5,
    ) -> None:
        """
        Verify that an element is not visible.
        """

        driver = self.get_mobile_driver()
        resolved_locator = self._get_locator(locator)
        timeout_value = self._convert_timeout(timeout)

        try:
            WebDriverWait(
                driver,
                timeout_value,
            ).until(
                EC.invisibility_of_element_located(
                    resolved_locator
                )
            )

        except TimeoutException as error:
            raise AssertionError(
                f"Element was visible but should not be: "
                f"{locator}"
            ) from error

    @keyword("Mobile Element Text Should Be")
    def mobile_element_text_should_be(
        self,
        locator: str,
        expected_text: object,
        timeout: object = 20,
    ) -> None:
        """
        Verify that an element's text exactly matches
        the expected text.
        """

        actual_text = self.get_mobile_element_text(
            locator,
            timeout,
        )

        expected_value = str(expected_text)

        if actual_text != expected_value:
            raise AssertionError(
                f"Mobile element text did not match.\n"
                f"Locator: {locator}\n"
                f"Expected: {expected_value!r}\n"
                f"Actual: {actual_text!r}"
            )

    @keyword("Mobile Element Text Should Contain")
    def mobile_element_text_should_contain(
        self,
        locator: str,
        expected_text: object,
        timeout: object = 20,
    ) -> None:
        """
        Verify that an element's text contains
        the expected value.
        """

        actual_text = self.get_mobile_element_text(
            locator,
            timeout,
        )

        expected_value = str(expected_text)

        if expected_value not in actual_text:
            raise AssertionError(
                f"Mobile element text did not contain "
                f"the expected value.\n"
                f"Locator: {locator}\n"
                f"Expected to contain: {expected_value!r}\n"
                f"Actual: {actual_text!r}"
            )

    # ------------------------------------------------------------------
    # Screenshot keywords
    # ------------------------------------------------------------------

    @keyword("Capture Mobile Screenshot")
    def capture_mobile_screenshot(
        self,
        name: str = "mobile_screenshot",
    ) -> str:
        """
        Capture a screenshot of the current mobile screen
        and return the saved file path.
        """

        driver = self.get_mobile_driver()

        return self.screenshot_library.capture_screenshot(
            name=name,
            driver=driver,
        )

    @keyword("Capture Failure Screenshot")
    def capture_failure_screenshot(
            self,
            test_name: str = "test_failure",
    ) -> str:
        """
        Capture a failure screenshot and return the saved
        file path.
        """

        driver = self.get_mobile_driver()

        return self.screenshot_library.capture_failure_screenshot(
            test_name=test_name,
            driver=driver,
        )
    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_optional_driver(
        self,
    ) -> Optional[WebDriver]:
        """
        Return the current driver without raising an error.
        """

        return self.driver_factory.driver

    @staticmethod
    def _get_locator(
        locator: str,
    ) -> Tuple[str, str]:
        """
        Convert a Robot Framework locator string into an
        Appium locator tuple.

        Supported formats:

        id=login_button
        xpath=//android.widget.Button
        accessibility_id=Login
        accessibility=Login
        class=android.widget.Button
        class_name=android.widget.Button
        name=Login
        android_uiautomator=new UiSelector().text("Login")
        ios_predicate=name == "Login"
        ios_class_chain=**/XCUIElementTypeButton[`name == "Login"`]
        """

        if locator is None:
            raise ValueError(
                "Locator cannot be None."
            )

        locator_value = str(locator).strip()

        if not locator_value:
            raise ValueError(
                "Locator cannot be empty."
            )

        if "=" not in locator_value:
            raise ValueError(
                "Invalid locator format. Use "
                "'strategy=value'. "
                f"Received: {locator_value!r}"
            )

        strategy, value = locator_value.split("=", 1)

        normalized_strategy = (
            strategy
            .strip()
            .lower()
            .replace("-", "_")
            .replace(" ", "_")
        )

        locator_target = value.strip()

        if not locator_target:
            raise ValueError(
                f"Locator value cannot be empty: "
                f"{locator_value!r}"
            )

        strategies = {
            "id": AppiumBy.ID,
            "xpath": AppiumBy.XPATH,
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "accessibility": AppiumBy.ACCESSIBILITY_ID,
            "class": AppiumBy.CLASS_NAME,
            "class_name": AppiumBy.CLASS_NAME,
            "name": AppiumBy.NAME,
            "android_uiautomator":
                AppiumBy.ANDROID_UIAUTOMATOR,
            "ios_predicate":
                AppiumBy.IOS_PREDICATE,
            "ios_class_chain":
                AppiumBy.IOS_CLASS_CHAIN,
        }

        if normalized_strategy not in strategies:
            supported_strategies = ", ".join(
                sorted(strategies.keys())
            )

            raise ValueError(
                f"Unsupported locator strategy: "
                f"{strategy!r}. Supported strategies: "
                f"{supported_strategies}"
            )

        return (
            strategies[normalized_strategy],
            locator_target,
        )

    @staticmethod
    def _convert_timeout(
        timeout: object,
    ) -> float:
        """
        Convert Robot Framework timeout input into
        a positive numeric value.
        """

        try:
            timeout_value = float(timeout)

        except (TypeError, ValueError) as error:
            raise ValueError(
                f"Timeout must be numeric. "
                f"Received: {timeout!r}"
            ) from error

        if timeout_value <= 0:
            raise ValueError(
                f"Timeout must be greater than zero. "
                f"Received: {timeout_value}"
            )

        return timeout_value

    @staticmethod
    def _convert_to_boolean(
        value: object,
    ) -> bool:
        """
        Convert Robot Framework boolean-like values
        into Python booleans.
        """

        if isinstance(value, bool):
            return value

        normalized_value = str(value).strip().lower()

        if normalized_value in {
            "true",
            "yes",
            "1",
            "on",
        }:
            return True

        if normalized_value in {
            "false",
            "no",
            "0",
            "off",
            "none",
            "",
        }:
            return False

        raise ValueError(
            f"Unable to convert value to boolean: "
            f"{value!r}"
        )