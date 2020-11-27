import requests
import xml.dom.minidom
import time
# import config7
from jmfmessages import SendJob

# This library contains contains examples of how jmf can be used to send command to PRISMAsync and obtain information from PRISMAsync
# All jmf messages are send mime-encoded. Note that no libary is used for mime-encoding, messages are mime-encoded "by hand"

print("Job was submitted and has QueueEntryID:",SendJob("http://fat-cep-601.ocevenlo.oce.net:8010", "file://C:/Users/hdok/source/repos/TRM-Examples/Python/jmfjdf/Test.pdf"))
print("Job was submitted and has QueueEntryID:",SendJob("http://fat-cep-601.ocevenlo.oce.net:8010", "http://ubuntu-hdok.ocevenlo.oce.net/pdf/PosterFashionWomanplusTextSample.pdf"))