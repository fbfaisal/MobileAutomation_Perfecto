import sys
import os
# Ensure project root is on PYTHONPATH so sibling packages like 'libraries' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libraries.CapabilityManager import CapabilityManager


manager = CapabilityManager()


android_caps = manager.get_capabilities(
    "android"
)

print(android_caps)


ios_caps = manager.get_capabilities(
    "ios"
)

print(ios_caps)