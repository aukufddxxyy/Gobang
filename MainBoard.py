import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QMainWindow, QFrame
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.Qt import QCursor
import os
from FiveChess import fiveChess


class Board(QFrame):

    msg2_status_bar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.winner = None

        self.chess_board = fiveChess()

        self.margin = 20
        self.padding = 50
        self.m_p = self.margin+self.padding
        self.side = 1
        self.r = 24

        self.timer = QBasicTimer()
        self.time_passed = 0

        self.init_board()

    def init_board(self):
        self.setFocusPolicy(Qt.StrongFocus)

    def square_size(self):
        square_width = (self.contentsRect().width()-self.m_p*2) // 14
        square_height = (self.contentsRect().height()-self.m_p*2) // 14
        if square_height > square_width:
            return square_width
        else:
            return square_height

    def start(self):
        self.msg2_status_bar.emit(str(self.time_passed))
        self.timer.start(1, self)

    def paintEvent(self, event):
        qp = QPainter(self)
        rect = self.contentsRect()
        top = rect.top()
        bottom = rect.bottom()
        left = rect.left()
        right = rect.right()
        self.drawChessBoard(qp, top, bottom, left, right)

    def drawChessBoard(self, qp, t, b, l, r):
        # brush = QBrush(Qt.SolidPattern)
        color = QColor(0xDEB887)
        width = min([b-t, r-l])

        qp.fillRect(l, t, width, width, color)

        pen = QPen(Qt.black, 4, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.margin,self.margin,width-self.margin,self.margin)
        qp.drawLine(self.margin,self.margin,self.margin,width-self.margin)
        qp.drawLine(width-self.margin,self.margin,width-self.margin,width-self.margin)
        qp.drawLine(self.margin,width-self.margin,width-self.margin,width-self.margin)

        board_width = (width-2*self.m_p)//14
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(15):
            qp.drawLine(self.m_p, self.m_p+i*board_width, self.m_p+14*board_width, self.m_p+i*board_width)
            qp.drawLine(self.m_p+i*board_width, self.m_p, self.m_p+i*board_width, self.m_p+14*board_width)
        
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRoundedRect(self.m_p-2+3*board_width,self.m_p-2+3*board_width,4,4,2,2)
        qp.drawRoundedRect(self.m_p-2+3*board_width,self.m_p-2+11*board_width,4,4,2,2)
        qp.drawRoundedRect(self.m_p-2+7*board_width,self.m_p-2+7*board_width,4,4,2,2)
        qp.drawRoundedRect(self.m_p-2+11*board_width,self.m_p-2+3*board_width,4,4,2,2)
        qp.drawRoundedRect(self.m_p-2+11*board_width,self.m_p-2+11*board_width,4,4,2,2)

        brush_b = QBrush(Qt.black, Qt.SolidPattern) 
        brush_w = QBrush(Qt.white, Qt.SolidPattern)
        for j in range(15):
            for i in range(15):
                if self.chess_board.checkerboard[j][i] == 1:
                    qp.setBrush(brush_b) 
                    qp.drawRoundedRect(self.m_p+i*board_width-self.r,self.m_p+j*board_width-self.r,2*self.r,2*self.r,self.r,self.r)
                elif self.chess_board.checkerboard[j][i] == -1:
                    qp.setBrush(brush_w)
                    qp.drawRoundedRect(self.m_p+i*board_width-self.r,self.m_p+j*board_width-self.r,2*self.r,2*self.r,self.r,self.r)

    def revoke(self):
        if self.chess_board.remove():
            self.side *= -1
            self.winner = None
            self.msg2_status_bar.emit('')
            self.update()

    def reset(self):
        self.chess_board.clear()
        self.side = 1
        self.winner = None
        self.msg2_status_bar.emit('')
        self.update()

    def mousePressEvent(self, event):
        cur_x = event.localPos().x()
        cur_y = event.localPos().y()
        col = int((cur_x - self.m_p + self.square_size()/2) // self.square_size())
        row = int((cur_y - self.m_p + self.square_size()/2) // self.square_size())
        if 0 <= col < self.chess_board.size and 0 <= row < self.chess_board.size and self.chess_board.is_void((col, row)):
            if not self.winner:
                self.chess_board.set_in((col,row), self.side)
                if self.chess_board.is_win((col,row)) and self.side == 1:
                    self.winner = '黑棋获胜'
                    self.msg2_status_bar.emit(self.winner)
                elif self.chess_board.is_win((col,row)) and self.side == -1:
                    self.winner = '白棋获胜'
                    self.msg2_status_bar.emit(self.winner)
                self.side *= -1
                self.update()
