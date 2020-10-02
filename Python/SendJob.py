import requests
import xml.dom.minidom
import time
from jmfmessages import SendJob

# This library contains contains examples of how jmf can be used to send command to PRISMAsync and obtain information from PRISMAsync
# All jmf messages are send mime-encoded. Note that no libary is used for mime-encoding, messages are mime-encoded "by hand"

url="http://fat-cep-601.ocevenlo.oce.net:8010"

print("Job was submitted and has QueueEntryID:",SendJob(url))