from importlib.metadata import version

LIB = "impedance"

try:
    __version__ = version(LIB)

# If the user don't have impedance installed
except ModuleNotFoundError:
    __version__ = f"Could not find {LIB} installed."
