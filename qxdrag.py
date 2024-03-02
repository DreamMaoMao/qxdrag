#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget,QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtGui import QDrag,QPixmap,QCursor,QPainter
import sys



class MyListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True) 
        self.setAcceptDrops(True) 
        self.setDropIndicatorShown(True) 

    def startDrag(self, e):

        item = self.currentItem()
        mime_data = QMimeData()
        mime_data.setUrls([QUrl.fromLocalFile(item.text())])
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
        sys.exit()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = sys.argv[1]
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
        self.listWidget.addItem(self.file_path)
        # 设置可以拖拽
        self.listWidget.setDragEnabled(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget)
        self.setLayout(vbox)
        self.listWidget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    # window.setGeometry(50, 50, 50, 50)
    window.resize(400,300)
    window.show()
    sys.exit(app.exec_())
