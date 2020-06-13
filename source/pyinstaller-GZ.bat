@echo off
pyinstaller mail2.py -F -i mail.ico --exclude tkinter --exclude xml
pause