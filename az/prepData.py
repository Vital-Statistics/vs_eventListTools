# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:29:23 2020

@author: jolucas
"""

def prepData(D):
    from datetime import datetime, timedelta
    dat=D.copy()
    dat.loc[:,'date']=dat.date.apply(lambda x: datetime.strptime(x,'%m/%d/%y'))
    dat.sort_values(['device','date'],axis=0,inplace=True)
    
    #### Throw out data from after a failure
    sm=dat.groupby('device').failure.transform(lambda x: (1-x.ne(1).cumprod().astype(bool)).cumsum())
    dat=dat.loc[sm<2,:]
    
    #### Create a variable for time to failure
    dat['delta']=dat.groupby('device').date.transform(lambda x: (x-x.iloc[-1])/timedelta(days=1))
    
    #### Now the fail date is always the last date.  Create a variable for failure by device
    dat['device_fails']=dat.groupby('device').failure.transform(lambda x: max(x))
    
    # #### Data is monotonic?
    # MT=pd.DataFrame({'device':dat.device.unique()})
    # for nm in cols:
    #     MT=MT.join(dat.groupby('device').apply(lambda x: pd.Index(x[nm]).is_monotonic).rename(nm),on='device')
        
    # MT[cols].apply(sum,axis=0)
    
    cols=['metric'+str(i+1) for i in range(9)]
    
    def td(x):
        y=x.diff()
        y.iloc[0]=x.iloc[0]
        return(y)
    
    for nm in cols:
        dat.loc[:,nm]=dat.groupby('device')[nm].transform(td)
    
    #### The 7th and 8th metric are identical
    cols.remove('metric8')
        
    #### Delete duplicate rows
    dat=dat.drop_duplicates()
    
    # if 'timeFilter' in tfm:
    #     #### Some of the non-fail devices are about to fail
    #     #### Delete 20 days from the end so we know we are
    #     #### training on clean outcomes.
        # dat=dat.loc[((dat.delta< -20) & (dat.device_fails==0)) | (dat.device_fails==1),:]
        # dat.loc[:,'delta']=dat.groupby('device').date.transform(lambda x: (x-x.iloc[-1])/timedelta(days=1))

    for nm in cols:
        dat[nm]=dat[nm].astype(float)

    return([dat,cols])
