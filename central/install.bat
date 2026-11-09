@echo off
set "SCRIPT_PATH=%~dp0Central.py"
set "DESKTOP_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Central.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$WScriptShell = New-Object -ComObject WScript.Shell;" ^
    "$Shortcut = $WScriptShell.CreateShortcut('%DESKTOP_PATH%');" ^
    "$Shortcut.TargetPath = 'python.exe';" ^
    "$Shortcut.Arguments = '\"%SCRIPT_PATH%\"';" ^
    "$Shortcut.WorkingDirectory = '%~dp0';" ^
    "$Shortcut.IconLocation = 'shell32.dll,4';" ^
    "$Shortcut.Description = 'Manage and organize your files/folders easily using CENTRAL!';" ^
    "$Shortcut.Save();"

echo Central is installed. You can close this window.
pause

:: if not python try doing manually python3 central.py
