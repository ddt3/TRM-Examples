"""
Contains a number of examples on how PRISMAsync jmf/jdf can be used for e.g. job management and printer status
"""
import requests
import xml.dom.minidom
import sys
import time



# This library contains contains examples of how jmf can be used to send command to PRISMAsync and obtain information from PRISMAsync
# All jmf messages are send mime-encoded. Note that no libary is used for mime-encoding, messages are mime-encoded "by hand"

example_job="http://ubuntu-hdok.ocevenlo.oce.net/pdf/SmallJob.pdf"

def RemoveQueueEntries (url, status):
  """Removes all queue entries with the given states

    Parameters:
    url: full link to printer jmf interface e.g. http://prismasync.lan:8010
    status: String of job states. Jobs in this state will be removed: (e.g. "Completed Aborted")

    Returns:
    int:Number of removed queueentries

  """
  headers={'Content-Type': 'multipart/related'}
  # Create a jmf message to retrieve the queue status that Filters on job status, it is allowed to mention multiple job statuses   

  data=mimeheader+"""<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" MaxVersion="1.5" SenderID="Python by hdok" TimeStamp="2020-08-30T11:39:00+02:00" Version="1.5" xsi:type="JMFRootMessage">
      <Query ID="Completed-12345" Type="QueueStatus" xsi:type="QueryQueueStatus">
        <QueueFilter StatusList="{}"/>
    </Query>
</JMF>
""".format(status)+mimefooter

  try:
    response=requests.post(url=url,data=data,headers=headers)
    root = xml.dom.minidom.parseString(response.content)
  except:
    print("Unexpected reply from", url)
    print(sys.exc_info()[0], "occurred.")
    return 0
  
  deletemessage="""MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" SenderID="Python by hdok" TimeStamp="2020-08-30T16:12:32+02:00" Version="1.3">
  <Command ID="PYTHON_IZAEIP_195_20190830161232" Type="RemoveQueueEntry" xsi:type="CommandRemoveQueueEntry">
"""
  Entries=root.getElementsByTagName("QueueEntry")
  nrjobs=(len(Entries))
  if nrjobs:
    for qid in Entries:
      deletemessage += """<QueueEntryDef QueueEntryID="{}" />\n""".format(qid.getAttribute("QueueEntryID"))
    deletemessage += """</Command></JMF>"""+mimefooter
    delresponse =  requests.post(url=url,data=deletemessage, headers=headers)
    if not delresponse.ok:
      nrjobs=0
  return nrjobs

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

  data=mimeheader+"""<?xml version="1.0" encoding="UTF-8"?>
<JMF xmlns="http://www.CIP4.org/JDFSchema_1_1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" MaxVersion="1.5" SenderID="Python by hdok" TimeStamp="2020-08-30T11:39:00+02:00" Version="1.5" xsi:type="JMFRootMessage">
      <Query ID="Completed-12345" Type="QueueStatus" xsi:type="QueryQueueStatus">
        <QueueFilter StatusList="{}"/>
    </Query>
</JMF>
""".format(status)+mimefooter

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


# Mime header
mimeheader = """MIME-Version: 1.0
Content-Type: multipart/related; boundary=-----abcdef1234ddd1234

-------abcdef1234ddd1234
Content-Type: application/vnd.cip4-jmf+xml
Content-ID: file1@user1.canon.com
Content-Disposition: Inline

"""

# Mime Footer
mimefooter = """
-------abcdef1234ddd1234--"""

def SendJob(url):
  """Sends a pre-defined job to the given url

    Parameters:
    url: full link to printer jmf interface e.g. http://prismasync.lan:8010

    Returns:
    id:QueueEntryID of submitted job

  """
  headers={'Content-Type': 'multipart/related'}

  data="""MIME-Version: 1.0  
Content-Type: multipart/related; boundary="=-aaabbbcccdddeee=="

--=-aaabbbcccdddeee==
Content-Disposition: attachement; 
filename=Submit-Job-PRISMAsync.jmf
Content-Id: <part1-Submit-Job-PRISMAsync>
Content-Transfer-Encoding: 7bit
Content-Type: application/vnd.cip4-jmf+xml

<JMF TimeStamp="2020-06-19T12:09:38-07:00" Version="1.4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.CIP4.org/JDFSchema_1_1">
    <Command ID="Submit-Job-PRISMAsync" Type="SubmitQueueEntry">
        <QueueSubmissionParams URL="cid:part2-Submit-Job-PRISMAsync">
            <QueueFilter QueueEntryDetails="None" MaxEntries="1" >
            </QueueFilter>
        </QueueSubmissionParams>
    </Command>
</JMF>

--=-aaabbbcccdddeee==
Content-Disposition: attachement; 
filename=Submit-Job-PRISMAsync.jdf
Content-Id: <part2-Submit-Job-PRISMAsync>
Content-Transfer-Encoding: 7bit
Content-Type: application/vnd.cip4-jdf+xml

<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<JDF xmlns="http://www.CIP4.org/JDFSchema_1_1" Activation="Active" Category="DigitalPrinting" ID="{}" JobPartID="{}" Status="Waiting" Type="Combined" Types="LayoutPreparation Imposition Interpreting Rendering ColorCorrection Folding DigitalPrinting HoleMaking Gathering Screening ColorSpaceConversion Stitching oce:Mailbox" Version="1.3" xmlns:oce="http://www.oce.com/JDF_Extension/1_00" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="Combined">
  <!--Generated by the CIP4 C++ open source JDF Library version  -->
  <Comment ID="c190712202412.-001_000034" Name="oce:TicketVersion">4.00</Comment>
  <Comment ID="c190712202412.-001_000035" Name="oce:DocumentDimension">612.000 792.000</Comment>
  <ResourcePool>
    <LayoutElement Class="Parameter" ID="r190712202412.-001_000038" Status="Available">
      <FileSpec URL="{}"/>
    </LayoutElement>
    <RunList Class="Parameter" ID="r190712202412.-001_000039" Status="Available">
      <LayoutElementRef rRef="r190712202412.-001_000038"/>
    </RunList>
    <Media Class="Consumable" DescriptiveName="Prodesign 90gr"  Dimension="841.88976378 1190.5511811" HoleType="None" ID="r190712202412.-001_000040" MediaColorName="White" MediaSetCount="1" Status="Available" Weight="90" MediaTypeDetails="DME_Uncoated090_CG50_MX150_R2.4_EU" oce:CustomMediaType="DME_Uncoated090_CG50_MX150_R2.4_EU"/>
   MediaTypeDetails="DME_Uncoated090_CG50_MX150_R2.4_EU" oce:CustomMediaType="DME_Uncoated090_CG50_MX150_R2.4_EU
    <LayoutPreparationParams Class="Parameter" ID="r190712202412.-001_000041" Rotate="Rotate0" Sides="TwoSidedFlipY" Status="Available">
      <FitPolicy SizePolicy="ClipToMaxPage"/>
      <PageCell>
        <ImageShift PositionX="Center" PositionY="Center" ShiftBack="0 0" ShiftFront="0 0"/>
      </PageCell>
    </LayoutPreparationParams>
    <InterpretingParams Class="Parameter" ID="r190712202412.-001_000042" Scaling="1 1" Status="Available" oce:MinLineWidthAdjustment="Off"/>
    <RenderingParams Class="Parameter" ID="r190712202412.-001_000043" Status="Available" oce:LineTextFatteningAdjustment="Off">
      <ObjectResolution Resolution="600 600"/>
    </RenderingParams>
    <ColorCorrectionParams Class="Parameter" ID="r190712202412.-001_000044" Status="Available">
      <ColorCorrectionOp AdjustContrast="0" AdjustLightness="0"/>
    </ColorCorrectionParams>
    <ColorSpaceConversionParams Class="Parameter" ID="r190712202412.-001_000045" Status="Available">
      <GeneralID IDUsage="oce:EnhancedColorRendering" IDValue="Off"/>
    </ColorSpaceConversionParams>
    <ScreeningParams Class="Parameter" ID="r190712202412.-001_000046" Status="Incomplete"/>
    <DigitalPrintingParams Class="Parameter" Collate="Sheet" ID="r190712202412.-001_000047" OutputBin="AutoSelect" Status="Available">
      <Disjointing OffsetDirection="None"/>
      <MediaRef rRef="r190712202412.-001_000040"/>
    </DigitalPrintingParams>
    <Component Class="Quantity" ComponentType="PartialProduct" ID="r190712202412.-001_000048" Status="Unavailable"/>
    <oce:MailboxDetails Class="Parameter" ID="r190712202412.-001_000049" Status="Available" UseMailbox="false"/>
    <HoleMakingParams Class="Parameter" ID="r190712202412.-001_000050" Status="Available"/>
    <FoldingParams Class="Parameter" ID="r190712202412.-001_000051" NoOp="true" Status="Available"/>
    <StitchingParams Class="Parameter" ID="r190712202412.-001_000052" NumberOfStitches="0" Status="Available" StitchType="Side"/>
    <Component Class="Quantity" ComponentType="PartialProduct" ID="r190712202412.-001_000053" Status="Unavailable"/>
    <Component Class="Quantity" ComponentType="PartialProduct" ID="r190712202412.-001_000054" Status="Unavailable"/>
    <Component Class="Quantity" ComponentType="FinalProduct" DescriptiveName="Final Component" ID="r190712202412.-001_000055" Status="Unavailable"/>
    <UsageCounter CounterTypes="Impressions" ID="UsageCounter_ID"/>
  </ResourcePool>
  <ResourceLinkPool>
    <CustomerInfoLink Usage="Input" rRef="r190712202412.-001_000036"/>
    <ContactLink Usage="Input" rRef="r190712202412.-001_000037"/>
    <LayoutElementLink Usage="Input" rRef="r190712202412.-001_000038"/>
    <RunListLink Usage="Input" rRef="r190712202412.-001_000039"/>
    <MediaLink Usage="Input" rRef="r190712202412.-001_000040"/>
    <LayoutPreparationParamsLink Usage="Input" rRef="r190712202412.-001_000041"/>
    <InterpretingParamsLink Usage="Input" rRef="r190712202412.-001_000042"/>
    <RenderingParamsLink Usage="Input" rRef="r190712202412.-001_000043"/>
    <ColorCorrectionParamsLink Usage="Input" rRef="r190712202412.-001_000044"/>
    <ColorSpaceConversionParamsLink Usage="Input" rRef="r190712202412.-001_000045"/>
    <ScreeningParamsLink Usage="Input" rRef="r190712202412.-001_000046"/>
    <DigitalPrintingParamsLink Usage="Input" rRef="r190712202412.-001_000047"/>
    <ComponentLink CombinedProcessIndex="6" Usage="Output" rRef="r190712202412.-001_000048"/>
    <oce:MailboxDetailsLink Usage="Input" rRef="r190712202412.-001_000049"/>
    <HoleMakingParamsLink Usage="Input" rRef="r190712202412.-001_000050"/>
    <FoldingParamsLink Usage="Input" rRef="r190712202412.-001_000051"/>
    <StitchingParamsLink Usage="Input" rRef="r190712202412.-001_000052"/>
    <ComponentLink CombinedProcessIndex="11" Orientation="Flip0" Usage="Input" rRef="r190712202412.-001_000053"/>
    <ComponentLink CombinedProcessIndex="11" Orientation="Flip0" Usage="Output" rRef="r190712202412.-001_000054"/>
    <ComponentLink Amount="1" Usage="Output" rRef="r190712202412.-001_000055"/>
  </ResourceLinkPool>
</JDF>

--=-aaabbbcccdddeee==--
""".format(time.asctime(),time.asctime(),example_job)
  try:
    response=requests.post(url=url,data=data,headers=headers)
    root = xml.dom.minidom.parseString(response.content)
  except:
    print("Unexpected reply from", url)
    print(sys.exc_info()[0], "occurred.")
    return 0
  Entries=root.getElementsByTagName("QueueEntry")
  id_array=Entries[0].getAttribute("QueueEntryID")
  return id_array