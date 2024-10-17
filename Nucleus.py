from sys import argv
from os import system
from datastore import ProductDisplayName

for _ in range(127) :
    argv.append('')
print('Nucleus 0.1.0')

HelpMessage = f'''{ProductDisplayName} created by Noah018dev. Please help us with our Github!!!
\tnucleus --help                           - Prints this message.
\tnucleus --execute --defaults             - Runs Nucleus AI with default settings.
\tnucleus --execute --advanced-runtime     - Allows you to customize your runtime. For advanced users.
\tnucleus --utility get-version            - Prints the current version of Nucleus.
\tnucleus --utility cleanup                - Cleans all files that are cleaned on exit in case of a crash.'''

if len(argv) == 1 :
    print('You have ran this with no command line arguments.')
    print('Try using --help.')
else :
    match argv[1] :
        case '--execute' :
            match argv[2] :
                case '--advanced-runtime' :
                    system('python runtimesettings.py --advanced')
                case '--defaults' :
                    system('python runtimesettings.py --auto')
                case _ :
                    print('nucleus --execute --defaults             - Runs Nucleus AI with default settings.')
                    print('nucleus --execute --advanced-runtime     - Allows you to customize your runtime. For advanced users.')
        
        case '--help' :
            print(HelpMessage)
            quit()

        case '--utility' :
            match argv[2] :
                case 'get-version' :
                    print(ProductDisplayName)
                case 'cleanup' :
                    if argv[3] == 'silent' :
                        system('python ai.py --finish-cleanup --silent')
                    else :
                        system('python ai.py --finish-cleanup')
                case _ :
                    print('nucleus --utility get-version            - Prints the current version of Nucleus.')
                    print('nucleus --utility cleanup                - Cleans all files that are cleaned on exit in case of a crash.')
                    print('nucleus --utility cleanup silent         - Exits without waiting for key press.')