# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 09:55:12 2021

@author: JoeLucas
"""

def collapseOverlapping(q,unit,st='startTime',et='stopTime',preferredLabel=None,gap=1,lbl='Label',sumCol='paid'):
    import datetime
    if 'eventID' in set(q):
        print('Dropping "eventID" column from q.')
        q=q.drop(columns='eventID')
    q.sort_values([unit,st,et],inplace=True)
    t=q.groupby(unit)[et].apply(lambda x:x.sort_values().reset_index(drop=True)).reset_index()
    q[et]=list(t[et])
    # delta=[False]+ list((q[st].iloc[1:].reset_index(drop=True)-q[et].iloc[:-1].reset_index(drop=True))/datetime.timedelta(days=1)>gap)
    # priorEnd=np.where(q[et].array[1:]>q[et].array[:-1],q[et].array[1:],q[et].array[:-1])
    # q['priorEnd']=[q[et].iloc[0]]+list(priorEnd)
    # q.loc[~q.duplicated(subset=unit,keep='first'),'priorEnd']=q.loc[~q.duplicated(subset=unit,keep='first'),et]
    # q[et]=q.priorEnd
    delta=[False]+ list((q[st].array[1:]-q[et].array[:-1])/datetime.timedelta(days=1)>gap)
    newEvent=1*(~q.duplicated(subset=unit,keep='first') | (pd.Series(delta,index=q.index.values)))
    eid=newEvent.cumsum().rename('eventID')
    res=q.join(eid)
    t=res.groupby('eventID')[[st,et,sumCol]].agg({st:'min',et:'max',sumCol:'sum'})
    res=res.drop(columns=[st,et,sumCol]).join(t,on='eventID')
    # if sumColumns is not None:
    #     sc=res.groupby('eventID')[sumColumns].sum()
    if preferredLabel is not None:
        q[lbl]=pd.Categorical(q[lbl],categories=preferredLabel)
        res.sort_values(['eventID',lbl],inplace=True)
        res=res.loc[~res.duplicated(subset='eventID',keep='first')]
    else:
        res.sort_values(['eventID',et],inplace=True)
        res=res.loc[~res.duplicated(subset='eventID',keep='last')]
    # print(res.head())
    # print('\n')
    # print(sc.head())
    # if sumColumns is not None:
    #     res=res.drop(columns=sumColumns).join(sc,on='eventID')
    return(res)
