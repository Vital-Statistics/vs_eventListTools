

def obsWindow(eList):
    u=eList.groupby(by='PAT_ID')['EVENT_TIME'].aggregate([min,max])
    u.rename(columns={'min':'First Observation','max':'Last Observation'},inplace=True)
    return(u)
    
