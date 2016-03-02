#Ipython code for data analysis.
#Data must be pre fetched using bubble_down.py
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pylab as plt
import datetime as dt

frame=pd.read_csv('C:\Work\TFinal.csv',sep=',',parse_dates=['data'],keep_default_na=False)
frame.rename(columns={'data':'date'},inplace=True)

#Create continuous data for each place for January
frame=frame.sort_values(by=['countries','lat','lon','date'])
frame.set_index('date',inplace=True)
filtered=(frame.groupby(['lat','lon','countries'])).resample('D').fillna(0)
filtered.reset_index(['date','countries','lat','lon'],inplace=True)
idx = pd.DatetimeIndex(start='2016-1-1', end='2016-1-31', freq='D')
df=pd.DataFrame(columns=['x','y','date','count','z','lat','lon'])
id=pd.DataFrame(columns=['x','y','date','count','z','lat','lon'])
for a,b in filtered.groupby(['lat','lon','countries']):
    b.set_index('date',inplace=True)
    try:
        b=b.reindex(idx)
    except:
        b.reset_index('date',inplace=True)
        id=pd.concat([id,b])
        continue
    b['count'].fillna(0,inplace=True)
    b.fillna(method='ffill',inplace=True)
    b.fillna(method='bfill',inplace=True)
    b.reset_index('date',inplace=True)
    df=pd.concat([df,b])
df.to_csv('C:\Work\TFiltered.csv',sep=',')

#Reload the continuously created data
df=pd.read_csv('C:\Work\TFiltered.csv',sep=';',parse_dates=['date'])
del df['Unnamed: 0']
df.set_index(['lat','lon','countries'],inplace=True)

#Calculate the Tscore and rolling mean base don a 7 day sample
df['tscore']=df['count'].groupby(level=[0,1,2]).apply(lambda x: (x-pd.rolling_mean(x,7,7))*np.sqrt(7)/pd.rolling_std(x,7,7))
df['rolling_mean']=df['count'].groupby(level=[0,1,2]).apply(pd.rolling_mean,7,7)
#Filter High Outliers
high_outliers=df[df['tscore']>=1.943]
high_outliers.sort_values(['date','rolling_mean'],ascending=False,inplace=True)

#Plot the graph of each place with a Tscore above threshold
pp=PdfPages('C:\\Work\\Spikes7dayTscore.pdf')
present=[]
for a,b in high_outliers.groupby(level=[0,1,2]):
    if a not in present:
        present.append(a)
        fig=plt.figure()
        ax=fig.add_subplot(111)
        plot_point=zip(b['tscore'].tolist(),b['date'].tolist(),b['count'].tolist())
        gp=df.loc[a].plot(ax=ax,x='date',y='count',marker='o')
        for (tscore,date,count) in plot_point:
            gp.annotate("%.2f"%tscore,xy=(date,count),size='x-small',xytext = (-10, 10),ha='center',textcoords = 'offset points',arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        gp.set_title(a)
        plt.savefig(pp,format='pdf')
        plt.close()
pp.close()

#Chose top 10 places with the highest rolling mean
temp=(high_outliers.groupby('date').head(10)).groupby(['date'])

#plot top 10 or 50 trending places per day:
days = pd.DatetimeIndex(start='2016-01-07', end='2016-01-031', freq='D')
pp=PdfPages('C:\\Work\\TrendEachDay5.pdf')
for day in days:
    fig=plt.figure()
    ax=fig.add_subplot(111)
    places=temp.get_group(str(day.date()))
    for a,item in places.groupby(level=[0,1,2]):
          lat,lon,country=a
          mark="%.2f %.2f "% (lat,lon)
          mark=mark+country
          gp=df.loc[a].plot(ax=ax,x='date',y='count', label=mark)
    ax.axvline(x=day.date(),linestyle='dashed',color='red')
    gp.legend(loc='best',fontsize='xx-small')
    gp.set_title(day,{'fontsize': 'xx-small','verticalalignment': 'bottom'})
    plt.savefig(pp,format='pdf')
    plt.close()
pp.close()

