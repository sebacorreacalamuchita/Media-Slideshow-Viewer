REM filepath: c:\Users\Escritorio\Documents\Proyectos\screensaver\scripts\create_screensaver.bat
@echo off
setlocal

:: Variables
set "PROJECT_DIR=%~dp0.."
set "SCRIPT_PATH=%PROJECT_DIR%\vysor3.py"
set "CONFIG_PATH=%PROJECT_DIR%\config.json"
set "DIST_PATH=%PROJECT_DIR%\dist"
set "BUILD_PATH=%PROJECT_DIR%\build"
set "OUTPUT_SCR=%DIST_PATH%\vysor3.scr"
set "SYSTEM32_PATH=%WINDIR%\System32\vysor3.scr"
set "COPY_SCRIPT=%~dp0copy_to_system32.bat"

:: Check if Python is installed
echo Checking Python installation...
py --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install it before proceeding.
    pause
    exit /b 1
)

:: Check if pip is installed
echo Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not installed. Please install pip before proceeding.
    pause
    exit /b 1
)

:: Install PyInstaller if not installed
echo Checking PyInstaller installation...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller.
        pause
        exit /b 1
    )
)

:: Ensure the dist folder exists
if not exist "%DIST_PATH%" (
    echo Creating dist folder...
    mkdir "%DIST_PATH%"
    if errorlevel 1 (
        echo Failed to create dist folder.
        pause
        exit /b 1
    )
)

:: Check if required files exist
if not exist "%SCRIPT_PATH%" (
    echo The file vysor3.py was not found at "%SCRIPT_PATH%".
    pause
    exit /b 1
)
if not exist "%CONFIG_PATH%" (
    echo The file config.json was not found at "%CONFIG_PATH%".
    pause
    exit /b 1
)

:: Create executable with PyInstaller
echo Creating the .scr executable...
pyinstaller --onefile --noconsole --add-data "%CONFIG_PATH%;." --name "vysor3" --distpath "%DIST_PATH%" --workpath "%BUILD_PATH%" --specpath "%BUILD_PATH%" "%SCRIPT_PATH%"
if errorlevel 1 (
    echo Failed to create the executable with PyInstaller.
    pause
    exit /b 1
)

:: Rename the executable to .scr extension
if exist "%OUTPUT_SCR%" del "%OUTPUT_SCR%"
rename "%DIST_PATH%\vysor3.exe" "vysor3.scr"
if errorlevel 1 (
    echo Failed to rename the executable to .scr.
    pause
    exit /b 1
)

:: Call the second script to copy the .scr file with administrator privileges
echo Running the copy script with administrator privileges...
powershell -Command "Start-Process '%COPY_SCRIPT%' -ArgumentList '%OUTPUT_SCR%', '%SYSTEM32_PATH%' -Verb RunAs"
if errorlevel 1 (
    echo Failed to copy the .scr file to the system folder.
    pause
    exit /b 1
)

:: Successful completion
echo Screensaver installed successfully.
pause
exit /b 0