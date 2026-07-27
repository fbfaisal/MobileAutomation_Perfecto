from libraries.DriverFactory import DriverFactory


driver_factory = DriverFactory()

runtime_config = (
    driver_factory.config_reader
    .get_runtime_config()
)

execution_provider = (
    runtime_config
    .get("execution_provider", "")
    .strip()
    .upper()
)

endpoint = driver_factory._get_endpoint(
    execution_provider
)

print("Execution provider:", execution_provider)
print("Appium endpoint:", endpoint)
print("DriverFactory configuration successful.")