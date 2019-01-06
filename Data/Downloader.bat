@echo off
ping localhost -n 5 >NUL
cd "C:\Wallpaper"
start " " pythonw Downloader.py "C:\Wallpaper"
exit 0