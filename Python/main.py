import jmfmessages
import argparse

parser = argparse.ArgumentParser(description='Delete all JMF QueueEntries that have the provided status from PRISMAsync')

parser.add_argument('--url', '-u', type=str, 
                    help='full url to PRISMAsync jmf interface. e.g. http://printer.com:8010')
parser.add_argument('--status', '-s', type=str, default="Completed",
                    help='The status of the jobs that need to be removed (default: Completed)')
args = parser.parse_args()
print(jmfmessages.RemoveQueueEntries(args.url, args.status), "jobs have been removed")