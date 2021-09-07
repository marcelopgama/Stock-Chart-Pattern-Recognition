import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
from matplotlib.widgets import SpanSelector
from matplotlib import gridspec
import pandas as pdr
import yfinance as yf
from sklearn.metrics import r2_score
import numpy as np

#region Inputs
stock='EURUSD=X'
volatility=0.1 #minimum of 10% of the window
window=200 #window of data for comparison
degreeOfConfidance=0.5 #0 to 1
#endregion

#region Load data and extract data 
#Timeframes: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
stockData=yf.download(stock, period='50d',interval='1h',auto_adjust=True)
close = pdr.DataFrame(data=stockData, index=stockData.index, columns=["Close"])
#endregion

#region Patterns -----------------------------------------------------------------------------------
vBottom=[5.0,4.0,3.0,2.0,1.0,2.0,3.0,4.0,5.0]
vTop=[1.0,2.0,3.0,4.0,5.0,4.0,3.0,2.0,1.0]
#endregion

#Function to scale the range to match pattern scale------------------------------------------------------------
def scaleChange(range):
    minValue=min(range)
    maxValue=max(range)    
    b=(5-1)/(maxValue-minValue)
    a=1-b*minValue
    newRng=[]
    for x in rng['Close']:
        newRng.append(round(b*x+a,6))
    return newRng    

#region Collections-----------------------------------------------------------------
minimos=pdr.DataFrame()
maximos=pdr.DataFrame()
vTopCollection=[]
vBottomCollection=[]
#endregion

#region Look all candles-----------------------------------------------------------
i=window-1
while i<len(close)-len(vBottom): #Same lenght of pattern

    rng=close[i:i+len(vBottom)]#Look foward

    #region Check if range has good volatility
    windowData=close[i-window-1+len(vBottom):i+len(vBottom)]
    windowChange=max(windowData['Close'])/min(windowData['Close'])-1
    change=max(rng['Close'])/min(rng['Close'])-1
    #endregion

    if (change/windowChange)>=volatility:
        scaledRng=scaleChange(rng['Close'])       
      
        #region R² - Check if range matches any pattern
        TopRes=r2_score(vTop,scaledRng)
        BottomRes=r2_score(vBottom,scaledRng)        
       
        if TopRes>degreeOfConfidance:
            b=rng[rng['Close']==max(rng['Close'])]
            maximos=maximos.append(b)             
            vTopCollection.append(rng)
        elif BottomRes>degreeOfConfidance:
            b=rng[rng['Close']==min(rng['Close'])]            
            minimos=minimos.append(b) 
            vBottomCollection.append(rng)
        #endregion    
    i+=1    
#endregion

#region Charts --------------------------------------------------------------------------------------

#region Adjusting Data 
newStockData=stockData
newStockData.reset_index(inplace=True)
newStockData.drop('Volume', inplace=True, axis=1)
newStockData['index'] = pdr.to_datetime(newStockData['index'])
newStockData['index'] = newStockData['index'].apply(mpl_dates.date2num)
#endregion

#region Formatting figure
fig=plt.figure()

#Setting grid
spec = gridspec.GridSpec(ncols=1, nrows=2,
                         width_ratios=[1], wspace=0,
                         hspace=0, height_ratios=[4, 1])

#Setting labels and titles
ax = fig.add_subplot(spec[0])
ax2 = fig.add_subplot(spec[1])
ax.set_xlabel('Date')
ax.set_ylabel('Price')

#Formatting Date
date_format = mpl_dates.DateFormatter('%Y/%m/%d %H:%M')
ax.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

line2 = ax2.plot([])
width=15/(24*60) #fraction of the day
candlestick_ohlc(ax, newStockData.values, width=width, colorup='green', colordown='red', alpha=1)
candlestick_ohlc(ax2, newStockData.values, width=width, colorup='green', colordown='red', alpha=1)

#endregion

#region Range Selector
def onselect(xmin, xmax):
    indmin, indmax = np.searchsorted(newStockData['index'], (xmin, xmax))    
    region_x = newStockData['index'][indmin:indmax]
    region_y = newStockData['Close'][indmin:indmax]    

    if len(region_x) >= 2:
        ax2.set_xlim(region_x.head(1).values, region_x.tail(1).values)               
        ax2.set_ylim(region_y.min()*0.998, region_y.max()*1.002)
        ax.set_xlim(region_x.head(1).values, region_x.tail(1).values)               
        ax.set_ylim(region_y.min()*0.998, region_y.max()*1.002)
        fig.canvas.draw()

span = SpanSelector(ax2, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='tab:blue'))

#endregion

#region Plot min and max points and patterns
if minimos.empty==False:
    ax.scatter(y=minimos['Close'],x=minimos.index,label="Mínimos",color='b')
    for min in vBottomCollection:
        ax.plot(min['Close'],color='b')
if maximos.empty==False:
    ax.scatter(y=maximos['Close'],x=maximos.index,label="Máximos",color='k') 
    for max in vTopCollection:
        ax.plot(max['Close'],color='k')

#endregion    
       
ax.legend()
plt.show()
#endregion