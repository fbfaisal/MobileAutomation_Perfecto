# Mobile Automation Framework

This repository is a Robot Framework mobile test automation project for
Android and iOS. It uses Appium for device interaction and can run against a
local Appium server or Perfecto.

## Start here

The framework is organized in layers so that test cases stay readable:

```text
tests -> business keywords -> page keywords -> locators
                                    |
                                    v
                           Python mobile library
                                    |
                                    v
                         Appium / local or Perfecto
```

- `tests/` describes the scenario and expected result.
- `resources/keywords/` describes business actions such as logging in.
- `resources/pages/` describes actions on one screen.
- `resources/locators/` stores Android and iOS selectors.
- `libraries/` contains the Python/Appium implementation.
- `config/` maps environment variables into framework configuration.

For a detailed component map, see [Framework architecture](docs/ARCHITECTURE.md).
For a worked example, see [Adding a test](docs/ADDING_A_TEST.md).

## Project structure

```text
MobileAutomation_2/
|-- config/                 Environment-driven YAML configuration
|-- data/                   Test-data files
|-- docs/                   Newcomer and architecture documentation
|-- libraries/              Custom Robot Framework Python libraries
|-- listeners/              Robot execution listeners
|-- reports/                Generated reports, logs, and screenshots
|-- resources/
|   |-- common/             Shared suite setup and teardown
|   |-- keywords/           Reusable business-level keywords
|   |-- locators/           Platform-specific selectors in YAML
|   |-- pages/              Page/screen-level keywords
|   `-- variables/          Shared Robot variables
|-- scripts/                Developer checks for framework components
|-- tests/
|   `-- smoke/              Smoke and framework-validation suites
|-- requirements.txt        Python dependencies
`-- robot.yaml              Reserved for Robot configuration
```

Generated files such as `output.xml`, `log.html`, `report.html`, screenshots,
and logs should not be committed.

## Prerequisites

- Python 3.10 or newer
- Appium 2 and the appropriate Android or iOS driver for local execution
- A connected emulator/device, or access to a Perfecto cloud

## Local setup

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env`, then load its values into the current PowerShell session. The
framework reads operating-system environment variables; it does not load
`.env` automatically.

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*)=(.*)$') {
        [Environment]::SetEnvironmentVariable(
            $matches[1].Trim(),
            $matches[2].Trim(),
            'Process'
        )
    }
}
```

Never commit `.env` or real credentials.

## Run tests

Run a check that does not create a device session:

```powershell
python -m robot --outputdir reports/robot tests/smoke/EnvironmentCheck.robot
python -m robot --outputdir reports/robot tests/smoke/FrameworkValidation.robot
```

Run the login smoke tests after Appium or Perfecto is configured:

```powershell
python -m robot --outputdir reports/robot tests/smoke/Login.robot
```

Run only tests with a specific tag:

```powershell
python -m robot --outputdir reports/robot --include smoke tests
```

Run suites in parallel:

```powershell
python -m pabot --processes 2 --outputdir reports/robot tests
```

Open `reports/robot/report.html` for the summary and
`reports/robot/log.html` for step-by-step details.

## Configuration

All YAML values in `config/` use `${ENVIRONMENT_VARIABLE}` placeholders.
`libraries/ConfigReader.py` replaces them at runtime and converts simple
boolean, integer, and null values.

The minimum values depend on the execution provider:

- `LOCAL`: provider, platform, Appium URL, device, automation engine, and
  application identifiers/path.
- `PERFECTO`: provider, platform, Perfecto host/token, Perfecto device, and
  application identifiers/path.

Use [.env.example](.env.example) as the full reference.

## Naming and ownership rules

- Tests contain intent and assertions, not raw selectors.
- Business workflows belong in `resources/keywords/`.
- Screen-specific actions belong in `resources/pages/`.
- Selectors belong in `resources/locators/<page>.yaml`.
- Generic Appium behavior belongs in `libraries/MobileLibrary.py`.
- Secrets and machine-specific values belong in environment variables.
- Add tags such as `smoke`, `regression`, feature name, and `negative` where
  appropriate.

## Current extension points

`BasePage.robot`, `TransferPage.robot`, `NavigationKeywords.robot`,
`APIHelper.py`, and `DataManager.py` are placeholders. Add behavior there only
when a test requires it; avoid placing unrelated keywords into a generic file.
