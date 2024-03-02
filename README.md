# qxdrag
Since [dragon](https://github.com/mwh/dragon) and [ripdrag](https://github.com/nik012003/ripdrag) can't drag files to the Xwayland window under the latest hyprland, I decided to write one by myself.

base pyqt5,generate file-list gui from cli which can open in target app

It works perfectly in x11 and xwayland modes, but in wayland mode there is a little problem, which is that if you enable the auto exit option, it requires you to click once the window to exit after finish drag.

https://github.com/DreamMaoMao/qxdrag/assets/30348075/290c8f8a-acda-49ec-bb51-1d6d0006d4ad




```conf
'-x', '--and-exit', action='store_true', help='exit after first successful drag to open'
'-b', '--basename', action='store_true', help='only show basename of each file'
'-w', '--width', type=int, help='window width', default=400
'-t', '--height', type=int, help='window height',default=300
'-p', '--path', type=str, help='dir full path'
'-e', '--expand', action='store_true', help='generate all file to item in folder'
'-s', '--size', type=int, help='icon size', default=64

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
