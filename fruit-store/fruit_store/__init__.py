import logging
import os

# TODO: IMPROVE ON THIS!!
logging.basicConfig(level=logging.INFO)

if "VERSION" not in os.environ:
    logging.warning("VERSION not defined")

__version__ = os.environ.get("VERSION", "Undefined")
