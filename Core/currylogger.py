def CurryLogger(Type : str) -> callable :
    def Log(Content : str) -> None :
        with open('nucleus.log', 'a') as LogFile :
            try :
                LogFile.write(f'[{Type}]\t{Content}\n')
            except UnicodeEncodeError as e :
                LogFile.write(f'[WARNING]\t{e}\n')
                LogFile.write(f'[{Type}]\tThis was a log but it couldn\'t be encoded.\n')
    
    return Log

info = CurryLogger('INFO')
warn = CurryLogger('WARN')
debug = CurryLogger('DEBUG')
error = CurryLogger('ERROR')
fatal = CurryLogger('FATAL')