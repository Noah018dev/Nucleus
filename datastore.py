from os import chdir, path

chdir(path.dirname(__file__))

OpenAI_API_KEY = open('API-KEY.TXT').read() # REMOVE BEFORE RELEASED

FileTypesInitalizedValue = {}

HeaderSplit = '!---!' # WARNING : CHANGING CAN BREAK THE WHOLE SERVER

BaseInjectLog = '//This code is used to log debugging information to console. "/inject_log.js"\nconsole.warn("Just another reminder to be careful with your API key!")\nconsole.log("Logging successfully injected into server file.")\n'

email = 'noahc018@pm.me'

SystemText = 'You are a helpful assistant designed to output JSON and be integrated with the system. Put your main text in the \"text\", and put any cmd text to execute in the \"cmd\". Using the windows cmd. Also have a \"quitting\" which is either 0 or 1, make it 1 if the user is trying to quit by entering something like \"quit\" or \"exit\".'