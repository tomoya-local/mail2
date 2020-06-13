@echo off
pyinstaller imap-mail.py -F --exclude tkinter --exclude xml
pause