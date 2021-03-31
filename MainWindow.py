import sys
from PyQt5.QtWidgets import QDesktopWidget, QCheckBox, QMainWindow, QComboBox, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
import os
# from AutoCell import Space
# import config
from MainBoard import Board


class AutoCell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_board = Board(self)
        self.reset_button = QPushButton('重新开始', self)
        self.revoke_button = QPushButton('撤销', self)

        self.status_bar = self.statusBar()

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.main_board)
        self.reset_button.move(1000, 200)
        self.revoke_button.move(1000, 400)

        self.reset_button.clicked.connect(self.main_board.reset)
        self.revoke_button.clicked.connect(self.main_board.revoke)
        self.main_board.msg2_status_bar[str].connect(self.status_bar.showMessage)

        self.main_board.start()

        self.resize(1200, 900)
        self.setMinimumSize(1200, 900)

        self.center()
        self.setWindowTitle('fiveChess')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
