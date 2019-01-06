@echo off
python -V 
If %errorlevel% == 0 (
    pip freeze|findstr praw
    If %errorlevel% == 1 (pip install praw)
    pip freeze|findstr wxPython
    If %errorlevel% == 1 (pip install -U wxPython)
	pip freeze|findstr PIL
    If %errorlevel% == 1 (pip install Pillow)
    mkdir C:\WallPaper
    move Data\Downloader.bat "C:%homepath%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    move Data C:\WallPaper\Data
    move Downloader.py C:\WallPaper\Downloader.py
    pythonw "C:\WallPaper\Downloader.py" "C:\WallPaper"
) else (
    echo "Install python Please"
)

