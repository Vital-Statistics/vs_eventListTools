# -*- coding: utf-8 -*-
"""
Created on Tue May 26 13:52:01 2020

@author: jolucas
"""

def xval_train(mod,U,cols,dat=None):
    S=U.copy()
    S['xval']=0
    S.reset_index(drop=True,inplace=True)
    # S['call']=0
    for i in range(len(S)):
        # ll=pd.Series(range(len(S))!=i,index=S.index)
        ll=S.index.values!=i
        mod.fit(S.loc[ll,cols],S.loc[ll,'device_fails'])
        S.loc[~ll,'xval']=mod.predict_proba(S.loc[~ll,cols])[:,1]
        # S.loc[~ll,'call']==mod.predict(S.loc[~ll,cols])
        if dat is not None:
            dv=dat.device==S.loc[i,'device']
            dat.loc[dv,'yhat']=mod.predict_proba(dat.loc[dv,cols])[:,1]
    mod.fit(S[cols],S.device_fails)
        
    return(S[['device','xval']].set_index('device')['xval'])


def xval_train_deep(mod,U,cols,dat=None):
    S=U.copy()
    S['xval']=0
    S.reset_index(drop=True,inplace=True)
    ww = mod.get_weights()
    # S['call']=0
    for i in range(len(S)):
        # ll=pd.Series(range(len(S))!=i,index=S.index)
        ll=S.index.values!=i
        mod.set_weights(ww)
        mod.fit(S.loc[ll,cols],S.loc[ll,'device_fails'],epochs=150,batch_size=10)
        S.loc[~ll,'xval']=mod.predict_proba(S.loc[~ll,cols])[:,1]
        # S.loc[~ll,'call']==mod.predict(S.loc[~ll,cols])
        if dat is not None:
            dv=dat.device==S.loc[i,'device']
            dat.loc[dv,'yhat']=mod.predict_proba(dat.loc[dv,cols])[:,1]
    mod.fit(S[cols],S.device_fails)
        
    return(S[['device','xval']].set_index('device')['xval'])
