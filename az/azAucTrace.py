# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:16:20 2020

@author: jolucas
"""

def azAucTrace(dat,wdw=60):
    aucTrace=pd.DataFrame({'delta':-1*pd.array(range(wdw)),'auc':0,'N':0,'N Fail':0})
    for i in range(wdw):
        S=rocTime(dat,lag=i)
        aucTrace.loc[i,'N']=len(S)
        aucTrace.loc[i,'N Fail']=sum(S.device_fails)
        fpr, tpr, _ = metrics.roc_curve(S.device_fails,S.yhat)
        aucTrace.loc[i,'auc']=metrics.auc(fpr,tpr)
        
    return(aucTrace)
