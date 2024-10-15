title Error Check
color 0f
@echo off
cls
.venv\Scripts\sourcery.exe review . --fix
echo.
pause
exit