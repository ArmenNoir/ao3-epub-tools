@echo off
setlocal enabledelayedexpansion

:: Calirbre convert dir
set CONVERTER="C:\Program Files\Calibre2\ebook-convert.exe"

:: the dir where you want to put converted files
cd /d "%~dp0"
set INPUT_DIR=convert

for %%f in ("%INPUT_DIR%\*.epub") do (
    echo Converting: %%~nxf

    set "input=%%f"
    set "output=%%~dpnf.azw3"

    %CONVERTER% "!input!" "!output!"
)

echo echo All conversions done!
pause
