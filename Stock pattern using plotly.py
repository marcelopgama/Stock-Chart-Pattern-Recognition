import pandas as pdr
import yfinance as yf
from sklearn.metrics import r2_score
import plotly.graph_objects as go


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
    
    rng=close[i:i+len(vBottom)] #Look foward

    #region Check if range has good volatility
    window=close[i-199+9:i+9]
    windowChange=max(window['Close'])/min(window['Close'])-1
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

#region Chart --------------------------------------------------------------------------------------
fig=go.Figure(data=[
                    go.Candlestick(
                        x=stockData.index,
                        open=stockData['Open'],
                        high=stockData['High'],
                        low=stockData['Low'],
                        close=stockData['Close'])                   
                            ]) 

if minimos.empty==False:
    fig.add_trace(go.Scatter(
                        x=minimos.index,
                        y=minimos['Close'],
                        marker=dict(color="Black", size=5),
                        mode='markers',
                        name='Bottom points'))
    
if maximos.empty==False:
     fig.add_trace(go.Scatter(
                        x=maximos.index,
                        y=maximos['Close'],
                        marker=dict(color="Purple", size=5),
                        mode='markers',
                        name='Top points'))

if len(vTopCollection)>0:
    for top in vTopCollection:
        fig.add_trace(go.Scatter(
                        x=top.index,
                        y=top['Close'],
                        marker=dict(color="Purple", size=10),
                        mode='lines',
                        name='Top V'))
       
if len(vBottomCollection)>0:
    for bottom in vBottomCollection:
        fig.add_trace(go.Scatter(
                       x=bottom.index,
                        y=bottom['Close'],
                        marker=dict(color="Black", size=10),
                        mode='lines',
                        name='Bottom V')) 

#Remove holidays and weekends
fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"]), 
        dict(values=["2015-12-25", "2016-01-01"])
    ]
)                               

fig.show()

#endregion

