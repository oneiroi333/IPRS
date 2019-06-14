import sys

from src.data_composer import DataComposer


composer = DataComposer(verbose=True)
try:
    composer.start()
except RuntimeError:
    sys.exit(1)
