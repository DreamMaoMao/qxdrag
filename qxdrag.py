#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget,QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QUrl,QSize
from PyQt5.QtGui import QDrag,QPixmap,QCursor,QPainter,QIcon
import sys,os
import argparse
import mimetypes
import platform


def islinux():
    pstr = platform.system()
    if pstr == "Linux":
        return True
    else:
        return False

def get_icon_path(file_path,from_dir):
    mime_type, _ = mimetypes.guess_type(file_path)    
    if mime_type == None:
        mime_type = "inode/directory"

    if "image" in mime_type and not from_dir:
        return file_path
    
    elif islinux() :
        import gi
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
    else:
        return None


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

        # 设置拖拽时的光标样式（Linux 下通常会自动应用，但可以手动指定）
        cursor = QCursor(Qt.ClosedHandCursor)
        QApplication.setOverrideCursor(cursor)
        drag.setDragCursor(cursor.pixmap(), Qt.CopyAction)
    
        # 只使用图标创建pixmap
        icon = item.icon()
        if not icon.isNull():
            pixmap = icon.pixmap(QSize(args.size, args.size))
            # 调整pixmap大小
            if pixmap.width() > 128 or pixmap.height() > 128:
                pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            drag.setPixmap(pixmap)
            # 设置热点在图标中心
            drag.setHotSpot(pixmap.rect().center())
    
        # 当释放按钮时，复制文件并退出
        drag.exec_(Qt.CopyAction)
        if args.and_exit:
            sys.exit()

class Window(QWidget):
    global args
    def __init__(self):
        super().__init__()
        self.file_path = args.path
        self.initUI()

    def set_item(self,file_path,from_dir):
        if args.basename:
            show_path = os.path.basename(file_path)
        else:
            show_path = file_path
        self.listWidget.addItem(show_path)
        item = self.listWidget.item(self.listWidget.count()-1)
        item.setData(Qt.UserRole,file_path)
        icon = QIcon(get_icon_path(file_path,from_dir))
        item.setIcon(icon)
        self.listWidget.setIconSize(QSize(args.size,args.size))

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
                background-color:#57340c;
                color: #ecd4ac;
                border-style: none;
                border-radius: 10px;
                border-bottom: 5px solid #2a1803;
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
        self.setWindowTitle('qxdrag')
        self.setStyleSheet(style)
        self.listWidget = MyListWidget()
        if args.expand and os.path.isdir(self.file_path):
            files = os.listdir(self.file_path)    
            if not platform.system() == "Windows":
                split_str = "/"
            else:
                split_str = "\\"        
            for file in files:
                self.set_item(self.file_path+split_str+file,True)
        else:
            self.set_item(self.file_path,False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listWidget)
        self.setLayout(vbox)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='generate drag file gui from cli')
    parser.add_argument('-x', '--and-exit', action='store_true', help='exit after first successful drag or drop')
    parser.add_argument('-b', '--basename', action='store_true', help='Always show basename of each file')
    parser.add_argument('-w', '--width', type=int, help='window width', default=400)
    parser.add_argument('-t', '--height', type=int, help='window height',default=300)
    parser.add_argument('-p', '--path', type=str, help='file full path')
    parser.add_argument('-e', '--expand', action='store_true', help='generate all file to item in folder')
    parser.add_argument('-s', '--size', type=int, help='icon size', default=64)

    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = Window()
    desktop = QApplication.desktop()
    window_x = desktop.availableGeometry().x() + int(desktop.availableGeometry().width()/2) - int(args.width/2)
    window_y = desktop.availableGeometry().y() + int(desktop.availableGeometry().height()/2) - int(args.height/2)
    window.setGeometry(window_x,window_y,args.width,args.height)
    window.setWindowFlags(Qt.Dialog)
    window.show()
    sys.exit(app.exec_())