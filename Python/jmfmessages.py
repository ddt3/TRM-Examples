"""
Contains a number of examples on how PRISMAsync jmf/jdf can be used for e.g. job management and printer status
"""
import base64
import os
import re
import sys
import time
import uuid
import xml.dom.minidom
import requests
from base64io import Base64IO

# This library contains contains examples of how jmf can be used to send command to PRISMAsync and obtain information from PRISMAsync
# All jmf messages are send mime-encoded. Note that no libary is used for mime-encoding, messages are mime-encoded "by hand"


# Mime header used for sending jmf
mimeheader_jmf = """MIME-Version: 1.0
Content-Type: multipart/related; boundary="ThisIsARandomString"

--ThisIsARandomString
Content-ID: part1@cpp.canon
Content-Type: application/vnd.cip4-jmf+xml
content-transfer-encoding:7bit 
Content-Disposition: attachment

"""
# Mime header used for sending jdf
mimeheader_jdf = """
--ThisIsARandomString
Content-ID: part2@cpp.canon 
content-transfer-encoding:7bit 
content-type: application/vnd.cip4-jdf+xml; charset="us-ascii" 
content-disposition: attachment; filename="Ticket.jdf"

"""
# Mime header used for sending pdf
mimeheader_pdf = """
--ThisIsARandomString
Content-ID: part3@cpp.canon
Content-Type: application/octet-stream; name=Job1.pdf
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=Job1.pdf

"""

# Mime Footer
mimefooter = """
--ThisIsARandomString--"""


def read_jmfjdf (message_file):
  """Read a jmf or jdf file from disk into a string

    Parameters:
    Filename

    Returns:
    string:Content of file

  """
  try:

    file = open(message_file)
    message=file.read()
    file.close
  except :
    print ("ERR: Trouble reading: ", message_file)
    exit()
  return message
  
def read_pdf (pdf_file):
  try:

    file = open(pdf_file)
    pdf=file.read()
    file.close
  except :
    print ("ERR: Trouble reading: ", pdf_file)
    exit()
  return pdf

def ReturnQueueEntries (url, status):
  """Return all queue entries with the given states

    Parameters:
    url: full link to printer jmf interface e.g. http://prismasync.lan:8010
    status: states that need to be reported (e.g. "Completed Aborted") use " " to not filter at all and receive all queue entries

    Returns:
    array of QueueEntryIDs

  """
  headers={'Content-Type': 'multipart/related'}
  # Create a jmf message to retrieve the queue status that Filters on job status, it is allowed to mention multiple job statuses   
  
  jmf_message=read_jmfjdf("jmfjdf/QueueStatus.jmf")
  jmf_message=jmf_message.replace("STATUS",status)
  data=mimeheader_jmf+jmf_message+mimefooter

  try:
    response=requests.post(url=url,data=data,headers=headers)
    root = xml.dom.minidom.parseString(response.content)
  except:
    print("Unexpected reply from", url)
    print(sys.exc_info()[0], "occurred.")
    return 0
  Entries=root.getElementsByTagName("QueueEntry")
  id_array=[]
  for qid in Entries:
    id_array.append(qid.getAttribute("QueueEntryID"))
  return id_array

example_job="cid:Job1.pdf"

def RemoveQueueEntries (url, status):
  """Removes all queue entries with the given states

    Parameters:
    url: full link to printer jmf interface e.g. http://prismasync.lan:8010
    status: String of job states. Jobs in this state will be removed: (e.g. "Completed Aborted")

    Returns:
    int:Number of removed queueentries

  """
  queue_ids=ReturnQueueEntries(url,status)
  nrjobs=len(queue_ids)
  if nrjobs:  
    to_delete=""
    for i in range(nrjobs):
      to_delete+="<QueueEntryDef QueueEntryID=\""+queue_ids[i]+"\" />\n"

    jmf_message=read_jmfjdf('jmfjdf/RemoveQueueEntry.jmf')
    jmf_message=jmf_message.replace("<QueueEntryDef QueueEntryID=\"QUEUEENTRY\" />",to_delete)
    headers={'Content-Type': 'multipart/related'}
    deletemessage=mimeheader_jmf+jmf_message+mimefooter
    
    try:
      delresponse =  requests.post(url=url,data=deletemessage, headers=headers)
      root = xml.dom.minidom.parseString(delresponse.content)
    except:
      print("Unexpected reply from", url)
      print(sys.exc_info()[0], "occurred.")
      return 0
    entries=root.getElementsByTagName("Comment")
    if  entries:
      for qid in entries:
        print(qid.firstChild.nodeValue)
        nrjobs-=1
    return nrjobs

def SendJob(url,pdfurl):
  """Sends a pre-defined job to the given url

    Parameters:
    url: full link to printer jmf interface e.g. http://prismasync.lan:8010

    Returns:
    id:QueueEntryID of submitted job

  """
  # Because a PDF file can have a large size, the complete message is first created as a file on disk
  unique_filename = str(uuid.uuid4())
  encoded_filename="EN-"+unique_filename
  sendmime=str(pdfurl).replace("file://","")
  if sendmime:
    #PDF file can be found on disk
    try:
      print ("Filename:", sendmime) 
      with open(sendmime, "rb") as source, open(encoded_filename, "wb") as target:
          with Base64IO(target) as encoded_target:
              for line in source:
                  encoded_target.write(line)
    except:
      print("File", sendmime, "could not be opened")
      return 0

  else:
    pass
    #PDF file can be found on a website
  with open(unique_filename, 'w') as outfile:
    outfile.write(mimeheader_jmf)
    with open("jmfjdf/SubmitQueueEntry.jmf",'r') as tempfile:
      jmf_message=tempfile.read()
      jmf_message=re.sub("URL=\".*\"","URL=\"cid:part2@cpp.canon\"",jmf_message)
    outfile.write(jmf_message)

    outfile.write(mimeheader_jdf)
    with open("jmfjdf/job1.jdf", 'r') as tempfile:
      jdf_message=tempfile.read()
      jdf_message=re.sub("URL=\".*\"","URL=\"cid:part3@cpp.canon\"",jdf_message)
      
      #Adding the current time to the JDF ticket ID and PARTID, easier to find in PRISMAsync jmf logging.
      jdf_message=jdf_message.replace("REPLACE_ID",time.asctime())
      jdf_message=jdf_message.replace("REPLACE_JOBPARTID",time.asctime())
    outfile.write(jdf_message)
    if sendmime :
      outfile.write(mimeheader_pdf)
      with open("jmfjdf/encoded_file",'r') as tempfile:
        for line in tempfile:
          outfile.write(line)
    outfile.write(mimefooter)
  
  with open(unique_filename,'r') as datafile:
    headers={'Content-Type': 'multipart/related'}
    try:
      response=requests.post(url=url, data=datafile.read(), headers=headers)
      root = xml.dom.minidom.parseString(response.content)
    except:
      print("Unexpected reply from", url)
      print(sys.exc_info()[0], "occurred.")
      return 0
    Entries=root.getElementsByTagName("QueueEntry")
    id_array=Entries[0].getAttribute("QueueEntryID")
  os.remove(unique_filename)
  os.remove(encoded_filename)
  return id_array
