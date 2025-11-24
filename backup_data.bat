@echo off
echo ====================================
echo Backing Up Job Application Data
echo ====================================
echo.

REM Create backup folder with timestamp
set timestamp=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
set backup_folder=backups\backup_%timestamp%

echo Creating backup folder: %backup_folder%
mkdir "%backup_folder%" 2>nul

REM Backup database
echo Backing up database...
copy "backend\job_tracker.db" "%backup_folder%\job_tracker.db" >nul
if %errorlevel% equ 0 (
    echo [OK] Database backed up
) else (
    echo [ERROR] Failed to backup database
)

REM Backup uploads folder
echo Backing up uploaded files...
xcopy "backend\uploads" "%backup_folder%\uploads" /E /I /Q >nul
if %errorlevel% equ 0 (
    echo [OK] Uploads backed up
) else (
    echo [ERROR] Failed to backup uploads
)

echo.
echo ====================================
echo Backup Complete!
echo ====================================
echo Location: %backup_folder%
echo.

REM Show backup size
for /f %%A in ('dir /s /a "%backup_folder%" ^| find "File(s)"') do set size=%%A
echo Total files backed up

echo.
echo You can restore by copying files from backup folder
echo back to backend\ folder.
echo.
pause

