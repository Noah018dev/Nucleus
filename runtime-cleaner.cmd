conhost --headless n-client.exe cmd /c python ai.py --finish-cleanup --silent
n-client.exe cmd /c .\debugger.cmd
%*
echo. > aidump.json
timeout /t 2 /nobreak > nul
conhost --headless n-client.exe cmd /c python ai.py --finish-cleanup --silent
start n-client.exe python logviewer.py nucleus.log
exit