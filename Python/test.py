import requests
import xml.dom.minidom
import jmfmessages

url = 'http://hq-cep4:8010'
# with open(r'my.mjm','rb') as tempObj:
#    data=tempObj.read()
headers={'Content-Type': 'multipart/related'}
response=requests.post(url=url,data=jmfmessages.querystatusComplete,headers=headers)
# print(response.content)
root = xml.dom.minidom.parseString(response.content)
for qid in root.getElementsByTagName("QueueEntry"):
  # print(qid.getAttribute("QueueEntryID"))
  # data=jmfmessages.removequeuentry.replace("XXYYXXYYXXYY",qid.getAttribute("QueueEntryID")))
  delresponse=requests.post(url=url,data=jmfmessages.removequeuentry.replace("XXYYXXYYXXYY",qid.getAttribute("QueueEntryID")),headers=headers)
  del
# print(root.getElementsByTagName("QueueEntry").item(1).getAttribute("QueueEntryID"))