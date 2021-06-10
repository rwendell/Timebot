import calendar
import datetime
from datetime import datetime, timedelta, timezone
import win32com.client

def get_work_log():
    work_log = {}
    Outlook = win32com.client.Dispatch("Outlook.Application")
    ns = Outlook.GetNamespace("MAPI")
    appts = ns.GetDefaultFolder(9).Items #Calendar folder

    appts.Sort("[Start]")
    appts.IncludeRecurrences = "True"


    curDay = datetime.today().strftime("%m/%d/%Y");

    appts = appts.Restrict("[Start] >= '" +curDay+" 12:00AM" "' AND [END] <= '" +curDay+" 23:59PM" "'")

    num_entries = 0
    #FIXME  Make the time round to nearest 15 mins (ceiling)
    #TODO   The way we are preventing collisions is kind of messy. Clean this up (KEY IS BEING STORED IN TITLE)
    for indx, a in enumerate(appts):
        #TODO: grab this if it's available and use it for better formatting
        # try:
        #   attach = a.Attachments 
        #   (grab all attachments and search for a .json --> making it easier to do calendar stuff + caching)
        # catch notfoundexception: 
        #   continue
        title = str(a.Subject)
        if title == "Time Entry":   #ensures that time entry isn't part of the work_log
            continue
        key = str(a.Subject) + " [" + str(num_entries) + "]"
        description = str(a.Body) if "Microsoft Teams meeting" not in str(a.Body) else ""
        start = a.Start.strftime("%H:%M")
        end = a.end.strftime("%H:%M")
        work_log[key] = {"Title": key, "Description": description, "Start": start,"End": end, "Link":""} #link will be used later
        num_entries += 1

    return work_log 

#TEST output
if __name__ == '__main__':
    work_log = get_work_log()
    for i in work_log:
        print(str(work_log[i]) + "\n")
    



