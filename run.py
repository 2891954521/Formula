import sys

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:

        command = input('run with: \n1.server\n2.gui\ninput 1 or 2 (default is 2):')
        
        if command == '':
            command = 'gui'
        elif command == '1':
            command = 'server'
        elif command == '2':
            command = 'gui'
    else:
        command = args[1]

    if command == 'server':
        import Server
        Server.run()
    elif command == 'gui':
        import GUI
        GUI.run()
    else:
        print('Unknown command')
        print('Usage: python run.py [server|gui]')
        sys.exit(1)