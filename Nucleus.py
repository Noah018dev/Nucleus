from sys import argv
from os import system

print('Nucleus 0.1.0')

if len(argv) == 1 :
    print('You have ran this with no command line arguments.')
else :
    match argv[1] :
        case '--execute' :
            match argv[2] :
                case '--advanced-runtime' :
                    system('python runtimesettings.py --advanced')
                case '--defaults' :
                    system('python runtimesettings.py --auto')
                case _ :
                    print('nucleus --execute --auto                 - Runs Nucleus AI with default settings.')
                    print('nucleus --execute --advanced-runtime     - Allows you to customize your runtime. For advanced users.')