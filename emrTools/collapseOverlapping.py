# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:55:12 2021

@author: JoeLucas
"""

def collapseOverlapping(q,unit,st='startTime',et='stopTime',preferredLabel=None,gap=1):
    import datetime
    q.sort_values([unit,st,et],inplace=True)
    delta=[False]+ list((q.startTime.iloc[1:].reset_index(drop=True)-q.stopTime.iloc[:-1].reset_index(drop=True))/datetime.timedelta(days=1)>gap)
    newEvent=1*(~q.duplicated(subset=unit,keep='first') | (pd.Series(delta,index=q.index.values)))
    eid=newEvent.cumsum().rename('eventID')
    res=q.join(eid)
    t=res.groupby('eventID')[[st,et,'paid']].agg({st:'min',et:'max','paid':'sum'})
    res=res.drop(columns=[st,et,'paid']).join(t,on='eventID')
    if preferredLabel is not None:
        q.Label=pd.Categorical(q.Label,categories=preferredLabel)
    res.sort_values(['eventID','Label'],inplace=True)
    res=res.loc[~res.duplicated(subset='eventID',keep='first')]
    return(res)
