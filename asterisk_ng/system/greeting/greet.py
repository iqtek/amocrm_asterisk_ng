from asterisk_ng import __author__
from asterisk_ng import __description__
from asterisk_ng import __license__
from asterisk_ng import __name__
from asterisk_ng import __version__


__all__ = ["greet"]


def greet() -> None:
    greeting = f"# {__name__} v{__version__} \n" \
            f"# Author: '{__author__}' License: {__license__}. \n" \
            f"# {__description__} \n" \
            f"# Made with ❤ by ergnoore."
    print(greeting)
