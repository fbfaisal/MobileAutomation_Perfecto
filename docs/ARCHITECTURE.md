# Framework architecture

## Execution flow

For a typical login test, control moves through these components:

```text
tests/smoke/Login.robot
  -> resources/keywords/LoginKeywords.robot
     -> resources/pages/LoginPage.robot
        -> libraries/LocatorReader.py
           -> resources/locators/login.yaml
        -> libraries/MobileLibrary.py
           -> libraries/DriverFactory.py
              -> libraries/CapabilityManager.py
                 -> libraries/ConfigReader.py
                    -> config/*.yaml + environment variables
           -> Appium server or Perfecto
```

This separation is intentional. A changed selector should normally require a
change only in a locator YAML file. A changed workflow should normally require
a change only in a business-keyword file.

## Layer responsibilities

| Layer | Location | Responsibility |
|---|---|---|
| Test suites | `tests/` | Scenarios, tags, setup/teardown, and assertions |
| Business keywords | `resources/keywords/` | Reusable user workflows |
| Page objects | `resources/pages/` | Actions and checks for one app screen |
| Locators | `resources/locators/` | Android/iOS selector mappings |
| Shared variables | `resources/variables/` | Non-secret Robot defaults |
| Python libraries | `libraries/` | Driver, waits, gestures, screenshots, config |
| Configuration | `config/` | Environment-variable mappings |
| Listeners | `listeners/` | Cross-cutting Robot execution hooks |
| Artifacts | `reports/` | Generated Robot reports and screenshots |

## Core Python components

### `ConfigReader`

Reads YAML from `config/`, substitutes `${NAME}` from the process
environment, and converts `true`, `false`, integer, and null-like strings.
Missing environment variables currently resolve to an empty string.

### `ValidationManager`

Checks provider, platform, device, application, and Perfecto requirements
before a driver is created. Validation errors should be treated as setup
problems rather than test failures.

### `CapabilityManager`

Combines runtime, device, and application configuration into W3C Appium
capabilities. It adds Perfecto-specific capabilities when the provider is
`PERFECTO` and can return a masked version for safe diagnostics.

### `DriverFactory`

Chooses the local or Perfecto endpoint, creates one Appium driver, returns the
active driver, and closes it safely.

### `MobileLibrary`

Exposes Robot keywords for session lifecycle, waits, input, clicking,
assertions, text retrieval, and screenshots. This is the primary interface
between Robot resource files and Appium.

### `LocatorReader`

Loads a named locator from `resources/locators/<page>.yaml` and selects its
Android or iOS value according to `PLATFORM`.

### `ScreenshotLibrary`

Writes named and failure screenshots under `reports/screenshots/`.

## Configuration model

```text
process environment
  -> config/runtime.yaml       provider/platform/environment/app/device
  -> config/execution.yaml     Appium URL, timeout, retry/report settings
  -> config/devices.yaml       automation engine and device properties
  -> config/applications.yaml  app path/package/activity/bundle
  -> config/perfecto.yaml      cloud endpoint, token, reporting metadata
  -> config/environments.yaml  test URL and credentials
  -> config/logging.yaml       log behavior
```

Configuration files are templates, not places for credentials. Put secrets in
the process environment or a CI secret store.

## Locator format

Each logical element has a platform mapping:

```yaml
login_button:
  android: "accessibility_id=login_button"
  ios: "accessibility_id=login_button"
```

Supported strategies include `id`, `xpath`, `accessibility_id`, `class_name`,
`name`, `android_uiautomator`, `ios_predicate`, and `ios_class_chain`.
Prefer accessibility IDs when the application provides stable ones.

## Session lifetime

`MobileLibrary` has Robot `SUITE` scope. A test or suite setup calls
`Open Mobile Application`, which creates the driver and shares it with the
screenshot component. Teardown calls `Close Mobile Application`, which quits
the driver and clears its references.

## Known incomplete areas

The repository contains several extension placeholders:

- `resources/pages/BasePage.robot`
- `resources/pages/TransferPage.robot`
- `resources/keywords/NavigationKeywords.robot`
- `libraries/APIHelper.py`
- `libraries/DataManager.py`

Some older framework-launch examples use the singular path `resource/` and
the legacy `PerfectoLibrary`. New suites should follow `Login.robot`: import
from `resources/` and use `CommonKeywords.robot`/`MobileLibrary.py`.
