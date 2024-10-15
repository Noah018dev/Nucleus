title Error Check (You can just close me)
color 0f
@echo off
cls
.venv\Scripts\sourcery.exe review . --fix
echo.
pause
exit