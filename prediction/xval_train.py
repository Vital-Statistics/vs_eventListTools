# -*- coding: utf-8 -*-
"""
Created on Tue May 26 13:52:01 2020

@author: jolucas
"""

import pandas as pd

def xval_train(mod,X,y,folds=20):
    S=pd.concat([y.rename('y'),X],axis=1)
    S['xval']=0
    cols=list(X)
    betaTrace=[]
    grp=pd.Series(random.choices(list(range(folds)),k=len(y)),index=y.index)
    yy=pd.DataFrame({'y':list(y),'grp':grp})
    for i in range(folds):
        ll=yy.grp!=i
        A=S.loc[ll,cols]
        mu=A.mean()
        sig=A.std()
        # mod.fit(S.loc[ll,cols],S.loc[ll,'y'])
        mod.fit((A-mu)/sig,S.loc[ll,'y'])
        betaTrace.append(mod.coef_[0])
        S.loc[~ll,'xval']=mod.predict_proba((S.loc[~ll,cols]-mu)/sig)[:,1]
    return(S['xval'],pd.DataFrame(dict(zip(cols,zip(*betaTrace)))))

def xval_train_xgb(mod,X,y,folds=20,verbose=False):
    S=pd.concat([y.rename('y'),X],axis=1)
    S['xval']=0
    cols=list(X)
    grp=pd.Series(random.choices(list(range(folds)),k=len(y)),index=y.index)
    yy=pd.DataFrame({'y':list(y),'grp':grp})
    for i in range(folds):
        if verbose:
            print(str(i)+' of '+str(folds))
        ll=yy.grp!=i
        A=S.loc[ll,cols]
        mu=A.mean()
        sig=A.std()
        # mod.fit(S.loc[ll,cols],S.loc[ll,'y'])
        mod.fit((A-mu)/sig,S.loc[ll,'y'])
        # betaTrace.append(mod.coef_[0])
        S.loc[~ll,'xval']=mod.predict((S.loc[~ll,cols]-mu)/sig)
    return(S['xval'])

def xval_train_penalty(mod,X,y):
    S=pd.merge(y.rename('y'),X,left_index=True,right_index=True)
    S['xval']=0
    cols=list(X)
    for i in S.index.values:
        ll=S.index.values!=i
        A=S.loc[ll,cols]
        mu=A.mean()
        sig=A.std()
        # mod.fit(S.loc[ll,cols],S.loc[ll,'y'])
        mod.fit((A-mu)/sig,S.loc[ll,'y'])
        # S.loc[~ll,'xval']=mod.predict_proba((S.loc[~ll,cols]-mu)/sig)[:,1]
        S.loc[~ll,'xval']=mod.predict((S.loc[~ll,cols]-mu)/sig)[0]
    return(S['xval'])

def xval_train_deep(mod,X,y,ep=150,bs=50):
    S=pd.merge(y.rename('y'),X,left_index=True,right_index=True)
    S['xval']=0
    cols=list(X)
    ww = mod.get_weights()
    for i in S.index.values:
        ll=S.index.values!=i
        mod.set_weights(ww)
        mod.fit(S.loc[ll,cols],S.loc[ll,'y'],epochs=ep,batch_size=bs,verbose=0)
        S.loc[~ll,'xval']=mod.predict_proba(S.loc[~ll,cols])
    return(S['xval'])
