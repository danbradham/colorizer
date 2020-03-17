# -*- coding: utf-8 -*-

# Standard library imports
import sys

# Third party imports
from Qt import QtWidgets

# Local imports
from .ui import Dialog


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    d = Dialog()
    sys.exit(d.exec_())
