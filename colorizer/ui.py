# -*- coding: utf-8 -*-

# Standard library imports
from __future__ import print_function, absolute_import
from string import Template

# Third party imports
from Qt import QtCore, QtGui, QtWidgets

# Local imports
from . import api, util


class Swatch(QtWidgets.QWidget):

    clicked = QtCore.Signal(object)
    style = Template('''
        QWidget{
            background-color: rgb($cr, $cg, $cb);
            border-radius: $radius;
        }
        QWidget:hover{
            background-color: rgb($hr, $hg, $hb);
        }
    ''')

    def __init__(self, color, size=24, **kwargs):
        super(Swatch, self).__init__(**kwargs)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.set_color(color)
        self.set_size(size)
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.refresh_style()

    def set_size(self, size):
        self.setFixedSize(size, size)
        self._size = size
        self.refresh_style()

    def get_size(self):
        return self._size

    def set_color(self, color):
        self._color = util.color_as_qcolor(color)

    def get_color(self):
        return self._color

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit(self._color)

    def refresh_style(self):
        color = util.color_as_tuple(self._color)
        hover = QtGui.QColor(self._color)
        hover.setHsl(
            hover.hslHue(),
            hover.hslSaturation(),
            util.clamp(hover.lightness() + 25),
        )
        hover = util.color_as_tuple(hover)
        radius = self._size * 0.5
        style = self.style.substitute(
            radius=radius,
            cr=color[0],
            cg=color[1],
            cb=color[2],
            hr=hover[0],
            hg=hover[1],
            hb=hover[2],
        )
        self.setStyleSheet(style)

    def sizeHint(self):
        return QtCore.QSize(self._size, self._size)


class ClearSwatch(Swatch):

    style = Template('''
        QWidget{
            border: 2 solid rgb($cr, $cg, $cb);
            background-color: transparent;
            border-radius: $radius;
        }
        QWidget:hover{
            border: 2 solid rgb($hr, $hg, $hb);
        }
    ''')

    def refresh_style(self):
        color = util.color_as_tuple(self._color)
        hover = util.color_as_tuple(util.lift(self._color, 40))
        radius = self._size * 0.5
        style = self.style.substitute(
            radius=radius,
            cr=color[0],
            cg=color[1],
            cb=color[2],
            hr=hover[0],
            hg=hover[1],
            hb=hover[2],
        )
        self.setStyleSheet(style)


class Swatches(QtWidgets.QListWidget):

    style = '''
    QListWidget{
        background-color: transparent;
        border: 0;
        padding: 0;
        margin: 0;
    }
    '''

    def __init__(self, size, *args, **kwargs):
        super(Swatches, self).__init__(*args, **kwargs)
        self._size = size
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setSpacing(int(size * 0.2))
        self.setViewMode(QtWidgets.QListView.IconMode)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet(self.style)

    def set_size(self, size):
        for i in range(self.count()):
            item = self.item(i)
            item.swatch.set_size(size)
            item.setSizeHint(item.swatch.sizeHint())
        self.setSpacing(int(size * 0.2))
        self._size = size

    def get_size(self):
        return self._size

    def add_swatch(self, color, swatch_cls=Swatch):
        swatch = swatch_cls(color, self._size)
        item = QtWidgets.QListWidgetItem()
        item.swatch = swatch
        item.setSizeHint(swatch.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, swatch)
        return swatch


class Dialog(QtWidgets.QDialog):

    style = '''
    QWidget {
        background-color: rgb(45, 45, 45);
        color: rgb(215, 215, 215);
    }
    QPushButton {
        background-color: rgba(0, 0, 0, 0);
        border: 0;
    }
    QPushButton:hover {
        background-color: rgba(0, 0, 0, 50);
    }
    QPushButton:pressed {
        background-color: rgba(0, 0, 0, 100);
    }
    '''

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('parent', get_parent())
        super(Dialog, self).__init__(*args, **kwargs)

        self.swatches = Swatches(size=36, parent=self)
        self.outliner = QtWidgets.QCheckBox('Outliner', parent=self)
        self.outliner.setChecked(True)
        self.wireframe = QtWidgets.QCheckBox('Wireframe', parent=self)
        self.wireframe.setChecked(True)
        self.smaller = QtWidgets.QPushButton(
            QtGui.QIcon(util.resource('smaller.png')),
            '',
            parent=self,
        )
        self.smaller.setFixedSize(24, 24)
        self.smaller.clicked.connect(self._on_smaller_clicked)
        self.bigger = QtWidgets.QPushButton(
            QtGui.QIcon(util.resource('bigger.png')),
            '',
            parent=self,
        )
        self.bigger.setFixedSize(24, 24)
        self.bigger.clicked.connect(self._on_bigger_clicked)
        self.tools = QtWidgets.QHBoxLayout()
        self.tools.setAlignment(QtCore.Qt.AlignLeft)
        self.tools.setSpacing(0)
        self.tools.setContentsMargins(0, 0, 0, 0)
        self.tools.addWidget(self.smaller)
        self.tools.addWidget(self.bigger)

        self.form = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        self.form.addWidget(self.outliner)
        self.form.addWidget(self.wireframe)
        self.form.addStretch(1)
        self.form.addLayout(self.tools)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addLayout(self.form)
        self.layout.addWidget(self.swatches)
        self.setLayout(self.layout)

        self._mouse_pressed = False
        self._mouse_position = None

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored,
            QtWidgets.QSizePolicy.Ignored,
        )
        self.setMinimumWidth(self.swatches.get_size())
        self.setWindowTitle('Colorizer')
        self.setWindowIcon(QtGui.QIcon(util.resource('colorizer.png')))
        self.setStyleSheet(self.style)

        self._add_swatches()
        self.resize(376, 150)

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._mouse_pressed = True
            self._mouse_position = event.pos()

    def mouseMoveEvent(self, event):
        if self._mouse_pressed:
            vector = event.pos() - self._mouse_position
            self.move(self.pos() + vector)

    def mouseReleaseEvent(self, event):
        self._mouse_pressed = False
        self._mouse_position = None

    def resizeEvent(self, event):
        self._update_layout()

    def state(self):
        return {
            'wireframe': self.wireframe.isChecked(),
            'outliner': self.outliner.isChecked(),
        }

    def _update_layout(self):
        width = self.rect().width()
        if width > 200:
            if self.form.direction() == QtWidgets.QBoxLayout.LeftToRight:
                return
            self.form.setDirection(QtWidgets.QBoxLayout.LeftToRight)
            self.form.insertStretch(2, 1)
        else:
            if self.form.direction() == QtWidgets.QBoxLayout.TopToBottom:
                return
            self.form.setDirection(QtWidgets.QBoxLayout.TopToBottom)
            stretch = self.form.takeAt(2)
            del stretch

    def _add_swatches(self):
        swatch = self.swatches.add_swatch('#444', ClearSwatch)
        swatch.clicked.connect(self._on_clear_clicked)

        greyscale = '0f2468a'
        for c in greyscale:
            swatch = self.swatches.add_swatch('#' + c * 6)
            swatch.clicked.connect(self._on_swatch_clicked)

        for name, c in api.colors.items():
            if name in ['black', 'white']:
                continue
            swatch = self.swatches.add_swatch(c)
            swatch.clicked.connect(self._on_swatch_clicked)

    def _on_smaller_clicked(self):
        size = util.clamp(self.swatches.get_size() - 4, 12, 72)
        self.swatches.set_size(size)
        self.setMinimumWidth(size)

    def _on_bigger_clicked(self):
        size = util.clamp(self.swatches.get_size() + 4, 12, 72)
        self.swatches.set_size(size)
        self.setMinimumWidth(size)

    def _on_swatch_clicked(self, color):
        color = util.color_as_float3(color)
        state = self.state()
        if state['outliner']:
            api.set_outliner_color(*color)
        if state['wireframe']:
            api.set_wireframe_color(*color)

    def _on_clear_clicked(self, color):
        state = self.state()
        if state['outliner']:
            api.clear_outliner_color()
        if state['wireframe']:
            api.clear_wireframe_color()


def get_parent():
    try:
        import maya
        for widget in QtWidgets.QApplication.instance().topLevelWidgets():
            if widget.objectName() == 'MayaWindow':
                return widget
    except ImportError:
        pass


def show(cache={}):
    '''Show the Colorizer Dialog'''

    if not cache:
        cache['_'] = Dialog()

    cache['_'].show()
    return cache['_']
