from flask import Flask
from datastore import HeaderSplit, BaseInjectLog
from fluiddata import *
from time import time

Times500Error = 999999999999999999999999

app = Flask(__name__)

def FluidServe(LocalFilePath : str) -> str:
    with open(LocalFilePath, 'r') as FileHandle :
        Content = FileHandle.read()
    ContentHeader : dict = eval(Content.split(HeaderSplit)[1])
    Content = f'<script src="/logging.js"></script>{Content.split(HeaderSplit)[0]}'

    ServerClearHandle = open('inject_log.js', 'w')
    ServerLog = open('inject_log.js', 'a')

    ServerClearHandle.write(BaseInjectLog)

    for Check in ContentHeader:
        Content = Content.replace(Check, eval(ContentHeader[Check]))
        ServerLog.write(f'console.log(\'Content "{Check}" replaced for "{ContentHeader[Check]}"\')\n')

    if BaseInjectLog in Content :
        return Content
    else :
        return StaticServe('errorpages/500.html')

def StaticServe(LocalFilePath : str) -> str :
    return open(LocalFilePath, 'r')

@app.route("/logging.js")
def DebugLog() :
    return StaticServe('inject_log.js')

@app.route("/")
def RootPath() :
    return FluidServe('fluidroot/index.html')

@app.errorhandler(404)
def ErrorHandler(Data) :
    #return '<script>location.href = "/"</script>'
    return StaticServe('errorpages/404.html')

