'''
colorlib
========

Customize object's wireframe and outliner colors.
'''
from collections import OrderedDict

colors = OrderedDict([
    ('red', (1, 0.33, 0.33)),
    ('peach', (1.0, 0.565, 0.33)),
    ('yellow', (1.0, 0.9, 0.33)),
    ('green', (0.33, 1.0, 0.33)),
    ('teal', (0.33, 0.9, 1.0)),
    ('blue', (0.33, 0.33, 1.0)),
    ('purple', (0.77, 0.33, 1.0)),
    ('pink', (1.0, 0.33, 0.9)),
    ('white', (1.0, 1.0, 1.0)),
    ('black', (0.0, 0.0, 0.0)),
])


def get_color(*name_or_rgb):
    '''Lookup color by name.'''

    if len(name_or_rgb) == 3:
        return name_or_rgb
    else:
        return colors[name_or_rgb[0]]


def set_outliner_color(*name_or_rgb):
    '''Set outliner color'''

    from maya import cmds
    color = get_color(*name_or_rgb)
    for node in cmds.ls(sl=True, long=True):
        cmds.setAttr(node + '.useOutlinerColor', True)
        cmds.setAttr(node + '.outlinerColor', *color)


def set_wireframe_color(*name_or_rgb):
    '''Set wireframe color'''

    from maya import cmds
    color = get_color(*name_or_rgb)
    for node in cmds.ls(sl=True, long=True):
        cmds.setAttr(node + '.overrideEnabled', True)
        cmds.setAttr(node + '.overrideRGBColors', 1)
        cmds.setAttr(node + '.overrideColorRGB', *color)


def set_color(*name_or_rgb):
    '''Set outliner and wireframe color'''

    set_outliner_color(*name_or_rgb)
    set_wireframe_color(*name_or_rgb)


def clear_outliner_color():
    '''Clear outliner color for selected objects.'''

    from maya import cmds
    for node in cmds.ls(sl=True, long=True):
        cmds.setAttr(node + '.useOutlinerColor', False)
        cmds.setAttr(node + '.outlinerColor', 0, 0, 0)


def clear_wireframe_color():
    '''Clear wireframe color for selected objects.'''

    from maya import cmds
    for node in cmds.ls(sl=True, long=True):
        cmds.setAttr(node + '.overrideColorRGB', 0, 0, 0)
        cmds.setAttr(node + '.overrideRGBColors', 0)
        cmds.setAttr(node + '.overrideEnabled', False)


def clear_color():
    '''Clear outliner and wireframe colors'''

    clear_outliner_color()
    clear_wireframe_color()
