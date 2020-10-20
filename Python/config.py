import configparser
import argparse

config = configparser.ConfigParser()
config_file='config.ini'

try:
    config.read('config.ini')
    printer = config['Printer']
    jobs = config['Jobs']
except:
    print("Config file not read, creating a new one")
    if not config.has_section('Printer'):
        config.add_section('Printer')
        config.set('Printer', 'prismasync_url', "http://PRISMAsync.network.lan:8010")
    if not config.has_section('Jobs'):
        config.add_section('Jobs')
        config.set('Jobs', 'status', "Completed")
    with open('config.ini', 'w') as fp:
        config.write(fp) 
    print("Please adapt",config_file, "to your situation")
    exit(0)

# The following block is used to take command line options for this tool.
# It needs a printer address and an  opional --status. --help is automatically generated
parser = argparse.ArgumentParser(description='Delete all JMF QueueEntries that have the provided status from PRISMAsync')
parser.add_argument('--url', type=str, default=printer['prismasync_url'],
                    help='full url to PRISMAsync jmf interface. e.g. http://printer.com:8010')
parser.add_argument('--status', '-s', type=str, default=jobs['status'],
                    help='The status of the jobs that need to be removed (default: Completed)')
args = parser.parse_args()


url=args.url
status=args.status