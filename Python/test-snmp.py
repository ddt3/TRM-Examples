import requests
import xml.dom.minidom
import time
from jmfmessages import SendJob

# This library contains contains examples of how jmf can be used to send command to PRISMAsync and obtain information from PRISMAsync
# All jmf messages are send mime-encoded. Note that no libary is used for mime-encoding, messages are mime-encoded "by hand"

URL="http://hq-cep3.oce.nl:8010"
Number=10
Delay=0
SendJob(URL, Number, Delay)
print("\r\nDone")
