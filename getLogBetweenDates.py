import os
import re

from ConnectionSSH import ConnectionSSH
import ReadProperties

basePath = os.path.dirname(os.path.abspath(__file__))
basePath = basePath + os.sep + 'resources' + os.sep

connectionSSH = ConnectionSSH()

ConfigParser = ReadProperties.ConfigParser()
prop = ConfigParser.read_config()

instancePatternWithDate = prop.get('weblogic', 'log.instance.start.date') + prop.get('arg', 'date') + prop.get('weblogic', 'log.instance.end.date')

if not os.path.exists(basePath):
    print('The localpath don\'t exist')
    quit()
else:
    shell = connectionSSH.get_ssh_connection()
    stdin, stdout, stderr = shell.exec_command('ls ' + prop.get('weblogic', 'log.path'))
    if prop.get('weblogic', 'log.path') in stdout.readline():
        connectionSSH.download_file(prop.get('weblogic', 'log.path'), basePath + 'AdminServer.out')

if not os.path.exists(basePath + 'AdminServer.out'):
    print('Can\'t download ' + basePath + 'AdminServer.out')
else:
    log = open(basePath + 'result.out', 'w+')
    with open(basePath + 'AdminServer.out') as file:
        for line in file.readlines():
            if re.match(instancePatternWithDate, line):
                log.write(line)

log.close()
file.close()
os.remove(basePath + 'AdminServer.out', dir_fd=None)

connectionSSH.ssh.close()
