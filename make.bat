
pyinstaller -F main.py^
 --hidden-import plyer.platforms^
 --hidden-import plyer.platforms.win^
 --hidden-import plyer.platforms.win.notification
