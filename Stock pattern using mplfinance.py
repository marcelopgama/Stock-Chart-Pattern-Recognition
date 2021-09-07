import pandas as pdr
import yfinance as yf
import mplfinance as mpl
from sklearn.metrics import r2_score

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

#region Look all candles----------------------------------------------------------------------------
i=window-1
while i<len(close)-len(vBottom):#Same lenght of pattern
    
    rng=close[i:i+len(vBottom)]#Look foward

    #region Check if range has good volatility
    windowData=close[i-199+len(vBottom):i+len(vBottom)]
    windowChange=max(windowData['Close'])/min(windowData['Close'])-1
    change=max(rng['Close'])/min(rng['Close'])-1
    #endregion

    if (change/windowChange)>=volatility:
        scaledRng=scaleChange(rng['Close'])

        #region R² - Check if range matches any pattern
        TopRes=r2_score(vTop,scaledRng)
        BottomRes=r2_score(vBottom,scaledRng)        
       
        if TopRes>0.5:
            b=rng[rng['Close']==max(rng['Close'])] 
            x=('{:%Y-%m-%d %H:%M}'.format(rng.head(1).index.to_pydatetime()[0]),rng.head(1)['Close'].to_numpy()[0])
            y=('{:%Y-%m-%d %H:%M}'.format(b.index.to_pydatetime()[0]),b['Close'].to_numpy()[0])
            z=('{:%Y-%m-%d %H:%M}'.format(rng.tail(1).index.to_pydatetime()[0]),rng.tail(1)['Close'].to_numpy()[0])
            newArray=[x,y,z]            
            maximos=maximos.append(b) 
            vTopCollection.append(newArray)            
        elif BottomRes>0.5:
            b=rng[rng['Close']==min(rng['Close'])]
            x=('{:%Y-%m-%d %H:%M}'.format(rng.head(1).index.to_pydatetime()[0]),rng.head(1)['Close'].to_numpy()[0])
            y=('{:%Y-%m-%d %H:%M}'.format(b.index.to_pydatetime()[0]),b['Close'].to_numpy()[0])
            z=('{:%Y-%m-%d %H:%M}'.format(rng.tail(1).index.to_pydatetime()[0]),rng.tail(1)['Close'].to_numpy()[0])
            newArray=[x,y,z] 
            minimos=minimos.append(b)                     
            vBottomCollection.append(newArray)            
        #endregion
            
    i+=1    
#endregion

#region Charts --------------------------------------------------------------------------------------
mpl.plot(stockData,
        type='candle',        
        style='yahoo',
        alines=dict(alines=vTopCollection,colors=['b']),
        show_nontrading=True,
        title='V-Top pattern')
mpl.plot(stockData,
        type='candle',        
        style='yahoo',
        alines=dict(alines=vBottomCollection,colors=['r']),
        show_nontrading=True,
        title='V-Bottom pattern')
#endregion
