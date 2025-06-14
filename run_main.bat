@echo off
:MENU
cls
echo.
echo ===================================
echo       AO3 EPUB TOOLS
echo ===================================
echo  1. Run
echo  q. Quit
echo ===================================
set /p choice=Input choice and enter 

if /i "%choice%"=="q" goto END
if "%choice%"=="1" (
    cls
    echo Running main.py ...
    python main.py
    echo.
    echo Press any button to return to main menu...
    pause >nul
    goto MENU
)

echo Invalid input, retry
pause
goto MENU

:END
echo Quit
exit