from pprint import pprint

from libraries.CapabilityManager import CapabilityManager


capability_manager = CapabilityManager()

capabilities = capability_manager.get_masked_capabilities()

pprint(capabilities)

print("Capability generation successful.")