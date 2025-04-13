REM filepath: c:\Users\Escritorio\Documents\Proyectos\screensaver\scripts\copy_to_system32.bat
@echo off
setlocal

:: Arguments
set "OUTPUT_SCR=%1"
set "SYSTEM32_PATH=%2"

:: Copy the .scr file to the system folder
echo Copying "%OUTPUT_SCR%" to "%SYSTEM32_PATH%"...
copy /y "%OUTPUT_SCR%" "%SYSTEM32_PATH%"
if errorlevel 1 (
    echo Failed to copy the .scr file to the system folder.
    pause
    exit /b 1
)

:: Successful completion
echo Screensaver copied successfully.
pause
exit /b 0