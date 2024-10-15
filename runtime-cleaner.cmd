conhost --headless n-client.exe cmd /c python ai.py --finish-cleanup --silent
n-client.exe cmd /c .\debugger.cmd
%*
start cmd /c start nucleus.log
echo. > aidump.json
timeout /t 2 /nobreak > nul
conhost --headless n-client.exe cmd /c python ai.py --finish-cleanup --silent
exit