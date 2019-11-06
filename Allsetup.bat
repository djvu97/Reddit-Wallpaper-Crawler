@echo off
python -V 
If errorlevel 0 (
    pip freeze|findstr praw & if errorlevel 1 (pip install praw)
    pip freeze|findstr wxPython & if errorlevel 1 (pip install -U wxPython)
    mkdir C:\WallPaper
    move Data\Downloader.bat "C:%homepath%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    move Data C:\WallPaper\Data
    move Downloader.py C:\WallPaper\Downloader.py
    pythonw "C:\WallPaper\Downloader.py" "C:\WallPaper"
    exit 0
) else (
    start https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe
)

