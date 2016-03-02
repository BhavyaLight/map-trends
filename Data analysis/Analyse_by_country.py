#Ipython code for data analysis.
#Data must be pre fetched using bubble_down.py
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pylab as plt
import datetime as dt

frame=pd.read_csv('C:\Work\TFinal.csv',sep=',',parse_dates=['data'],keep_default_na=False)
frame.rename(columns={'data':'date'},inplace=True)
#Group data by country
frame.set_index(['countries','date'],inplace=True)
filtered=frame.groupby(level=[0,1]).sum()
filtered.reset_index(['countries'],inplace=True)
filtered=(filtered.groupby(['countries'])).resample('D').fillna(0)
filtered.reset_index(['countries','date'],inplace=True)
#Remove borderlying places --> filtered=filtered[filtered.countries.str.contains('[^\|]')]
idx = pd.DatetimeIndex(start='2016-1-1', end='2016-1-31', freq='D')
df=pd.DataFrame(columns=['countries','count'])

#Fill gaps in the values
for a,b in filtered.groupby(['countries']):
    b.set_index('date',inplace=True)
    b=b.reindex(idx)
    b['count'].fillna(0,inplace=True)
    b.fillna(method='ffill',inplace=True)
    b.fillna(method='bfill',inplace=True)
    b.reset_index('date',inplace=True)
    df=pd.concat([df,b])
del df['date']

df.rename(columns={'index':'date'},inplace=True)
df.set_index(['countries'],inplace=True)
#Calculate the Tscore and rolling mean of each country
df['tscore']=df['count'].groupby(level=0).apply(lambda x: (x-pd.rolling_mean(x,7,7))*np.sqrt(7)/pd.rolling_std(x,7,7))
df['rolling_mean']=df['count'].groupby(level=0).apply(pd.rolling_mean,7,7)
high_outliers=df[df['tscore']>=1.943]

#Plot each country with a high Tscore to see trends
pp=PdfPages('C:\\Work\\Country_Trends.pdf')
present=[]
for a,b in high_outliers.groupby(level=0):
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

#Plot the monthly graph for the top 10 trending countries for each day in Jan.
high_outliers.sort_values(['date','rolling_mean'],ascending=False,inplace=True)
temp=(high_outliers.groupby('date').head(10)).groupby('date')
#plot top 10 or 50 trending places per day:
days = pd.DatetimeIndex(start='2016-01-07', end='2016-01-031', freq='D')
pp=PdfPages('C:\\Work\\CountryEachDayMean.pdf')
for day in days:
    fig=plt.figure()
    ax=fig.add_subplot(111)
    places=temp.get_group(str(day.date()))
    for country,item in places.groupby(level=0):
          gp=df.loc[country].plot(ax=ax,x='date',y='count', label=country)
    ax.axvline(x=day.date(),linestyle='dashed',color='red')
    gp.legend(loc='best',fontsize='xx-small')
    gp.set_title(day,{'fontsize': 'xx-small','verticalalignment': 'bottom'})
    plt.savefig(pp,format='pdf')
    plt.close()
pp.close()