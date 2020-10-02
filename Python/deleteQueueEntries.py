import jmfmessages
import argparse

# The following block is used to take command line options for this tool.
# It needs a printer address and an  opional --status. --help is automatically generated
parser = argparse.ArgumentParser(description='Delete all JMF QueueEntries that have the provided status from PRISMAsync')
parser.add_argument('url', type=str, 
                    help='full url to PRISMAsync jmf interface. e.g. http://printer.com:8010')
parser.add_argument('--status', '-s', type=str, default="Completed",
                    help='The status of the jobs that need to be removed (default: Completed)')
args = parser.parse_args()

# The following statement calls RemoveQueueEntries and prints the number of removed QueueEntryIDs

print(jmfmessages.RemoveQueueEntries(args.url, args.status), "QueueEntries have been removed")