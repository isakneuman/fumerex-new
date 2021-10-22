import gammu

def init_gsm():
    state_machine = gammu.StateMachine()
    state_machine.ReadConfig()
    state_machine.Init()
    return state_machine

def get_new_message(state_machine):
    status         =   state_machine.GetSMSStatus()
    count_new_sms  =   status["UnRead"]
    start = True
    new_sms   = []
    sms       = []
    try:
        while count_new_sms > 0:
            if start:
                sms = state_machine.GetNextSMS(Start=True, Folder=0)
                start = False
            else:
                sms = state_machine.GetNextSMS(Location=sms[0]["Location"], Folder=0)
            count_new_sms = count_new_sms - len(sms)

            for m in sms:
                if ( m["Text"].isdigit() ):
                    new_sms.append(m["Text"])
            return new_sms
    except gammu.ERR_EMPTY:
            # This error is raised when we've reached last entry
            # It can happen when reported status does not match real counts
        print("Failed to read all messages!")

state_machine = init_gsm()
array = get_new_message(state_machine)
print(array)