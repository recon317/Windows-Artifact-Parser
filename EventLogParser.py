import win32evtlog
import pandas as pd


computer = None
logType = "Security"
h = win32evtlog.OpenEventLog(computer, logType)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ


dictionary = {'Event ID': [], 'Event Time': [], 'Event Source': [], 'Event Description': [], 'Logon Type': []}


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
            dictionary['Event ID'].append(eventID)
            dictionary['Event Time'].append(evTime)
            dictionary['Event Source'].append(evSrc)
            dictionary['Event Description'].append(eveDesc)
            dictionary['Logon Type'].append(logonType)

df = pd.DataFrame.from_dict(dictionary)

df.to_csv('events.csv')