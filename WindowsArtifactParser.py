import win32evtlog
import pandas as pd
import os
def login_evt():
    computer = None
    logType = "Security"
    h = win32evtlog.OpenEventLog(computer, logType)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ


    evtDictionary = {'Event ID': [], 'Event Time': [], 'Event Source': [], 'Event Description': [], 'Logon Type': []}


    events = True
    while events:
        events = win32evtlog.ReadEventLog(h, flags, 0)
        for event in events:
            eventID = event.EventID
            evTime = event.TimeGenerated
            evSrc = event.SourceName
            eveDesc = event.StringInserts

            if eventID == 4624:
                logonType = eveDesc[8]
                evtDictionary['Event ID'].append(eventID)
                evtDictionary['Event Time'].append(evTime)
                evtDictionary['Event Source'].append(evSrc)
                evtDictionary['Event Description'].append(eveDesc)
                evtDictionary['Logon Type'].append(logonType)

    df = pd.DataFrame.from_dict(evtDictionary)

    df.to_csv('events.csv')

def prefetch():
    pfDictionary = {'File Name': [], 'Creation Date': [], 'Last Modification Date': []}
    pfPath = "C:\\Windows\\Prefetch"
    pfFiles = os.listdir(pfPath)
    for file in pfFiles:
        filePath = f"C:\\Windows\\Prefetch\\{file}"
        pfFileStats = os.stat(filePath)
        pfFileCreationDate = pfFileStats.st_birthtime
        pfLastModDate = pfFileStats.st_mtime
        pfDictionary['File Name'].append(file)
        pfDictionary['Creation Date'].append(pfFileCreationDate)
        pfDictionary['Last Modification Date'].append(pfLastModDate)
    pfDF = pd.DataFrame.from_dict(pfDictionary)
    pfDF.to_csv('prefetch.csv')

login_evt()
prefetch()