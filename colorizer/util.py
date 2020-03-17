# -*- coding: utf-8 -*-

# Standard library imports
import os

# Third party imports
from Qt import QtGui

__all__ = [
    'resource',
    'clamp',
    'lift',
    'color_as_tuple',
    'color_as_qcolor',
]

try:
    basestring
except NameError:
    basestring = str


package_path = os.path.dirname(__file__).replace('\\', '/')


def resource(*parts):
    return os.path.join(package_path, *parts).replace('\\', '/')


def clamp(value, mn=0, mx=255):
    return max(min(value, mx), mn)


def lift(color, amount):
    color = color_as_qcolor(color)
    return QtGui.QColor(
        clamp(color.red() + amount),
        clamp(color.blue() + amount),
        clamp(color.green() + amount),
    )


def is_8bit(color):
    if not isinstance(color, (tuple, list)):
        return False

    return all([isinstance(c, int) and c < 256 for c in color])


def color_as_tuple(color):
    if isinstance(color, (tuple, list)):
        if is_8bit(color):
            return color
        else:
            return tuple(*[int(c * 255) for c in color])
    elif isinstance(color, QtGui.QColor):
        return color.red(), color.green(), color.blue()
    elif isinstance(color, basestring):
        c = QtGui.QColor(0, 0, 0)
        c.setNamedColor(color)
        return c.red(), c.green(), c.blue()
    else:
        raise ValueError('Color must be one of [tuple, list, QColor, str]')


def color_as_float3(color):
    if isinstance(color, (tuple, list)):
        if is_8bit(color):
            return tuple(*[int(c / 255.0) for c in color])
        else:
            return color
    elif isinstance(color, QtGui.QColor):
        return color.redF(), color.greenF(), color.blueF()
    elif isinstance(color, basestring):
        c = QtGui.QColor(0, 0, 0)
        c.setNamedColor(color)
        return c.redF(), c.greenF(), c.blueF()
    else:
        raise ValueError('Color must be one of [tuple, list, QColor, str]')


def color_as_qcolor(color):
    if isinstance(color, QtGui.QColor):
        return color
    if isinstance(color, (tuple, list)):
        if is_8bit(color):
            return QtGui.QColor(*color)
        else:
            return QtGui.QColor(*[int(c * 255) for c in color])
    elif isinstance(color, basestring):
        c = QtGui.QColor(0, 0, 0)
        c.setNamedColor(color)
        return c
    else:
        raise ValueError('Color must be one of [tuple, list, QColor, str]')
