#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget,QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtGui import QDrag,QPixmap,QCursor,QPainter,QIcon
import sys,os
import argparse
import mimetypes
import gi

def get_icon_path(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)    
    if mime_type == None:
        mime_type = "inode/directory"
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gio
    icon_theme = Gtk.IconTheme.get_default()
    icon = Gio.content_type_get_icon(mime_type)
    image_file = None
    for entry in icon.to_string().split():
        if entry != "." and entry != "GThemedIcon":
            try:
                image_file = icon_theme.lookup_icon(entry, 32, 0).get_filename()
            except:
                pass
        if image_file:
            break
    return image_file    


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

        # generate a pixmap to follow mouse move
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

    def set_item(self,file_path):
        if args.basename:
            show_path = os.path.basename(file_path)
        else:
            show_path = file_path
        self.listWidget.addItem(show_path)
        item = self.listWidget.item(self.listWidget.count()-1)
        item.setData(Qt.UserRole,file_path)
        icon = QIcon(get_icon_path(file_path))
        item.setIcon(icon)

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
        if args.expand and os.path.isdir(self.file_path):
            files = os.listdir(self.file_path)            
            for file in files:
                self.set_item(self.file_path+"/"+file)
        else:
            self.set_item(self.file_path)

        # print()
        # 设置可以拖拽
        # self.listWidget.setDragEnabled(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget)
        self.setLayout(vbox)
        self.listWidget.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generate drag file gui from cli')
    parser.add_argument('-x', '--and-exit', action='store_true', help='exit after first successful drag or drop')
    parser.add_argument('-b', '--basename', action='store_true', help='Always show basename of each file')
    parser.add_argument('-w', '--width', type=int, help='window width', default=400)
    parser.add_argument('-t', '--height', type=int, help='window height',default=300)
    parser.add_argument('-p', '--path', type=str, help='file full path')
    parser.add_argument('-e', '--expand', action='store_true', help='generate all file to item in folder')

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = Window()
    # window.setGeometry(50, 50, 50, 50)
    window.resize(args.width,args.height)
    window.show()
    sys.exit(app.exec_())
