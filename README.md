# qxdrag
base pyqt5,generate file-list gui from cli which can open in target app

```conf
'-x', '--and-exit', action='store_true', help='exit after first successful drag ordrop'
'-b', '--basename', action='store_true', help='Always show basename of each file'
'-w', '--width', type=int, help='window width', default=400
'-t', '--height', type=int, help='window height',default=300
'-p', '--path', type=str, help='file full path'
'-e', '--expand', action='store_true', help='generate all file to item in folder'
```

# example:
### x11 or xwayland:
```shell
QT_QPA_PLATFORM=xcb ~/tool/qxdrag.py -x -e -b -p ~/Images/hello.jpg
```

### wayland
```shell
QT_QPA_PLATFORM=wayland ~/tool/qxdrag.py -x -e -b -p ~/Images/hello.jpg
```

### property
x11 class: qxdrag.py