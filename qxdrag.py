#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget,QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtGui import QDrag,QPixmap,QCursor,QPainter
import sys,os
import argparse


class MyListWidget(QListWidget):
    global args
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True) 
        self.setAcceptDrops(True) 
        self.setDropIndicatorShown(True) 

    def startDrag(self, e):
        item = self.currentItem()
        mime_data = QMimeData()
        mime_data.setUrls([QUrl.fromLocalFile(item.data(Qt.UserRole))])
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        rect = self.visualRect(self.indexFromItem(item))
        painter.drawPixmap(rect, self.viewport().grab(rect))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(QCursor.pos()))
        # when release button,copy file and exit
        
        drag.exec_(Qt.CopyAction)
        if args.and_exit:
            sys.exit()


class Window(QWidget):
    global args
    def __init__(self):
        super().__init__()
        self.file_path = args.path
        self.initUI()

    def initUI(self):
        style = """
            QWidget {
                background-color: #222;
                color: #ecd4ac;
                font-family: 'Arial';
                font-size: 12px;
            }
            
            QListWidget {
                background-color: #555555;
                color: #ecd4ac;
                border-style: none;
                border-radius: 4px;
                padding: 4px;
                font-size: 25px;
            }
            QListWidget::item {
                background-color:#333;
                color: #ecd4ac;
                border-style: none;
                border-radius: 10px;
                border-bottom: 5px solid #191818;
                margin-bottom: 3px;

            }
            QListWidget::item:selected {
                background-color:#db9d3f;
                color: #000000;
                border-style: none;
                border-radius: 10px;
                border-bottom: 5px solid #a77428;
                margin-bottom: 3px;
                font-size: 25px;
            }
             
        """
        self.setStyleSheet(style)
        self.listWidget = MyListWidget()
        if args.basename:
            show_path = os.path.basename(self.file_path)
        else:
            show_path = self.file_path

        self.listWidget.addItem(show_path)

        item = self.listWidget.item(self.listWidget.count()-1)
        item.setData(Qt.UserRole,self.file_path)

        # 设置可以拖拽
        self.listWidget.setDragEnabled(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget)
        self.setLayout(vbox)
        self.listWidget.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generate drag file gui from cli')
    parser.add_argument('-x', '--and-exit', action='store_true', help='exit after first successful drag or drop')
    parser.add_argument('-b', '--basename', action='store_true', help='Always show basename of each file')
    parser.add_argument('-w', '--width', type=int, help='window width', default=400)
    parser.add_argument('-e', '--height', type=int, help='window height',default=300)
    parser.add_argument('-p', '--path', type=str, help='file full path')

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = Window()
    # window.setGeometry(50, 50, 50, 50)
    window.resize(args.width,args.height)
    window.show()
    sys.exit(app.exec_())
