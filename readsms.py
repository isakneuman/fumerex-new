import gammu

def readsms():
    state_machine = gammu.StateMachine()
    state_machine.ReadConfig()
    state_machine.Init()

    status = state_machine.GetSMSStatus()

    remain = status["SIMUsed"] + status["PhoneUsed"] + status["TemplatesUsed"]

    start = True
    
    sms   = []

    try:
        while remain > 0:
            if start:
                sms = state_machine.GetNextSMS(Start=True, Folder=0)
                start = False
            else:
                sms = state_machine.GetNextSMS(Location=sms[0]["Location"], Folder=0)
            remain = remain - len(sms)

            for m in sms:
                if ( m["Text"].isdigit() and m["State"]=='UnRead' ):
                    
                    print("{:<15}: {}".format("Text", m["Text"]))
    except gammu.ERR_EMPTY:
        # This error is raised when we've reached last entry
        # It can happen when reported status does not match real counts
        print("Failed to read all messages!")

readsms()