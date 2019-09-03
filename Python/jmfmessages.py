import requests
import xml.dom.minidom

mimeheader = """MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

"""
querystatus = """MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" DeviceID="HQ-CEP4" MaxVersion="1.5" SenderID="CIP4 Alces Bologna-18.03" TimeStamp="2019-08-30T11:39:00+02:00" Version="1.5" xsi:type="JMFRootMessage">
  <Query ID="ALCES_IZAEIP_160_20190830113900" Type="QueueStatus" xsi:type="QueryQueueStatus" />
</JMF>

-------abcdef1234ddd1234--
"""
querystatusComplete = """MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" DeviceID="HQ-CEP4" MaxVersion="1.5" SenderID="CIP4 Alces Bologna-18.03" TimeStamp="2019-08-30T11:39:00+02:00" Version="1.3" xsi:type="JMFRootMessage">
  <Query ID="Completed-12345" Type="QueueStatus" xsi:type="QueryQueueStatus">
        <QueueFilter StatusList="Held Completed"/>
    </Query>
</JMF>

-------abcdef1234ddd1234--
"""

removequeuentry="""MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" SenderID="CIP4 Alces Bologna-18.03" TimeStamp="2019-08-30T16:12:32+02:00" Version="1.3">
  <Command ID="ALCES_IZAEIP_195_20190830161232" Type="RemoveQueueEntry" xsi:type="CommandRemoveQueueEntry">
    <QueueEntryDef QueueEntryID="XXYYXXYYXXYY" />
  </Command>
</JMF>



-------abcdef1234ddd1234--
"""

def RemoveQueueEntries (url, status):
  headers={'Content-Type': 'multipart/related'}
  data="""MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" DeviceID="HQ-CEP4" MaxVersion="1.5" SenderID="CIP4 Alces Bologna-18.03" TimeStamp="2019-08-30T11:39:00+02:00" Version="1.5" xsi:type="JMFRootMessage">
      <Query ID="Completed-12345" Type="QueueStatus" xsi:type="QueryQueueStatus">
        <QueueFilter StatusList="{}"/>
    </Query>
</JMF>

-------abcdef1234ddd1234--
""".format(status)

  response=requests.post(url=url,data=data,headers=headers)
  root = xml.dom.minidom.parseString(response.content)

  deletemessage="""MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" SenderID="CIP4 Alces Bologna-18.03" TimeStamp="2019-08-30T16:12:32+02:00" Version="1.3">
  <Command ID="ALCES_IZAEIP_195_20190830161232" Type="RemoveQueueEntry" xsi:type="CommandRemoveQueueEntry">
"""
  Entries=root.getElementsByTagName("QueueEntry")
  nrjobs=(len(Entries))
  if nrjobs:
    for qid in Entries:
      deletemessage += """<QueueEntryDef QueueEntryID="{}" />\n""".format(qid.getAttribute("QueueEntryID"))
    deletemessage += """</Command></JMF>"""
    delresponse =  requests.post(url=url,data=deletemessage, headers=headers)
    if not delresponse.ok:
      nrjobs=0
  return nrjobs
