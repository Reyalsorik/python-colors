#!/usr/bin/env python

"""Contains logic for coloring text."""

from types import SimpleNamespace
from typing import Callable, KeysView


class Colors(type):
    """Metaclass responsible for getting colors and setting new colors."""

    colors = SimpleNamespace(
        default="\033[0m",
        red="\033[91m",
        blue="\033[94m",
        grey="\033[90m",
        cyan="\033[96m",
        black="\033[90m",
        green="\033[92m",
        white="\033[97m",
        yellow="\033[93m",
        magenta="\033[95m"
    )

    @classmethod
    def __dir__(mcs) -> KeysView[str]:
        """List valid color keys."""
        return mcs.colors.__dict__.keys()

    @classmethod
    def __getattr__(mcs, color: str) -> Callable:
        """Get color.

        :param color: color name
        """
        if not hasattr(mcs.colors, color):
            raise AttributeError(f"The color '{color}' is not available, try one of the following: {mcs.colors.__dict__.keys()}")
        return Colorizer(color)

    @classmethod
    def __setattr__(mcs, color: str, value: str) -> None:
        """Set color.

        :param color: color name
        :param value: color value
        """
        setattr(mcs.colors, color, value)

    __getitem__ = __getattr__
    __setitem__ = __setattr__


class Colorizer(object):
    """Colorize text."""

    def __init__(self, color: str) -> None:
        """Initialize.

        :param color: color name
        """
        self.color = color

    def __call__(self, text: str) -> str:
        """Callable.

        :param text: text to color
        """
        return f"{getattr(Colors.colors, self.color)}{text}{Colors.colors.default}"  # End with default to prevent color bleed

    def __str__(self) -> str:
        """Print the colorized text."""
        return self.__call__(self.color)

    def __repr__(self) -> str:
        """Repr."""
        return self(self.__class__.__name__)

    def __add__(self, obj: object) -> str:
        """Add.

        :param obj: object
        """
        return f"{getattr(Colors.colors, self.color)}{obj}"

    def __radd__(self, obj: object) -> str:
        """Radd.

        :param obj: object
        """
        return f"{obj}{getattr(Colors.colors, self.color)}"


class CText(metaclass=Colors):
    r"""Generate colored text strings.

    # Standard usage:
    print(CText.blue("this text is blue"))
    print(CText["blue"]("this text is also blue"))

    # Multiple colors:
    print(CText.blue + "blue text" + CText.red + " now red" + CText.default)

    # Setting a custom color
    CText.orange = u"\u001b[38;5;202m"
    print(CText.orange("this text is orange"))
    """
