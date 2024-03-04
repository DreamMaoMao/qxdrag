# qxdrag
![image](https://github.com/DreamMaoMao/qxdrag/assets/30348075/d794714e-1519-4439-8b84-3d1a0bc9b748)


Since [dragon](https://github.com/mwh/dragon) and [ripdrag](https://github.com/nik012003/ripdrag) can't drag files to the Xwayland window under the latest hyprland, I decided to write one by myself.

base pyqt5,generate file-list gui from cli which can open in target app.
it should be work both in linux,windows and macos. but i haven't test in macos.


## Linux

https://github.com/DreamMaoMao/qxdrag/assets/30348075/290c8f8a-acda-49ec-bb51-1d6d0006d4ad

## Windows

https://github.com/DreamMaoMao/qxdrag/assets/30348075/7a900e6a-8f4c-4695-9da9-03fac2c020a0

# Dependent
pyqt(>= pyqt5.15.10 and < pyqt6) 

```
sudo pacman -S python3
sudo pacman -S python-pyqt5
pip install pycairo
pip install PyGObject
```

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
