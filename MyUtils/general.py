import os
import sys


class HiddenPrints:
    """
    Function to prevent code printing.
    Source: https://www.codegrepper.com/code-examples/python/python+turn+off+printing
    Example:
        with HiddenPrints():
            print("This wont print")
    """

    def __init__(self):
        pass

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
