# Trading system v5 - data fetching using python Multiplprocessing library with multiple processes
# and displaying it on a Flask local web-server

# flask --app Trading_system_v3 run --debug --with-threads
# --reload --with-threads




# home page should have both ususal BO & ORB table with OI data

# Add a separate page/tab for Swing trading, stocks close to weekly high stocks, 
# stocks close to 52week high (As per a chartink scanner that you have got from youtube)

# Add a separate page/tab where a table which should have rsi colums & avg_rsi column for all the stocks







from nselib import capital_market
from flask import Flask, render_template
from jugaad_data.nse import NSELive
import pandas as pd
import multiprocessing
import time
import sys
from datetime import datetime
import yfinance as yf
import re

current_process = multiprocessing.current_process()
process_name = current_process.name
event = multiprocessing.Event()
trading_system_server = Flask(__name__)



# RUN THIS CODE FROM - 9:16am



# ALSO SET THE SERVER IN AUTO REFRESHING MODE AFTER EVERY LOOP that runs again which runs again after 5 MINUTES
# JUST LIKE A DEVELOPMENT SERVER AUTOFREFERESHES EVERYTIME A CHANGE IS MADE TO THE CODE

# When the home page will display the top 10 stocks sorted using ADX values, make sure you create another 
#                       secondary page where i can print the entire 200 stocks sorted according to the ADX values




'''num_rows = len(yf_data)
k = [k+1 for k in range(num_rows)]
yf_data['Index'] = k
yf_data = yf_data.reset_index(drop=True)
yf_data = yf_data.set_index('Index')'''

# add the above code to change the index numbering






eqList = ['RELIANCE', 'TCS', 'HDFCBANK', 'ICICIBANK','BHARTIARTL', 'SBIN', 'INFY', 'ITC']

''',
    'HINDUNILVR', 'LT', 'BAJFINANCE', 'MARUTI', 'HCLTECH', 'SUNPHARMA', 'NTPC', 'ONGC',
    'AXISBANK', 'ADANIENT', 'TATAMOTORS', 'TITAN', 'KOTAKBANK', 'POWERGRID', 'ADANIPORTS',
    'ULTRACEMCO', 'ASIANPAINT', 'COALINDIA', 'M&M', 'BAJAJFINSV', 'BAJAJ-AUTO', 'NESTLEIND',
    'WIPRO', 'JSWSTEEL', 'TATASTEEL', 'GRASIM', 'SBILIFE', 'HINDALCO', 'BPCL',
    'EICHERMOT', 'HDFCLIFE', 'TECHM', 'INDUSINDBK', 'BRITANNIA', 'CIPLA', 'DIVISLAB',
    'DRREDDY', 'TATACONSUM', 'HEROMOTOCO', 'APOLLOHOSP','LTIM','SHRIRAMFIN'
]'''


n = NSELive()



target_start_hour, target_start_minute, target_start_second = 23, 59, 45
target_start_time = datetime.now().replace(hour=target_start_hour, minute=target_start_minute, second=target_start_second)




def RSI_14_CALCULATOR(yf_data,event,lock,RSI_2m,RSI_5m,minutes):
    i=1
    close_prices = yf_data['Close'].tolist() 

    if len(close_prices) >= 14:  
        price_diffs = [close_prices[i] - close_prices[i - 1] for i in range(1, len(close_prices))]
    else:
        print("WARNING :- NUMBER OF PRICES ARE LESS THAN 14 DATA POINTS...!!")
    gains = []
    losses = []
    for diff in price_diffs:
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-diff)
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14
    rs = avg_gain / avg_loss
    event.set()
    rsi = (100 - (100 / (1 + rs)))
    with lock:
        if minutes == '2m':
            RSI_2m.append(round(rsi,2))
        if minutes == '5m':
            RSI_5m.append(round(rsi,2))



def DMI_CALCULATOR(high,low,close,period):
    trs = []
    dms_pos = []
    dms_neg = []
    i=1
    
    for i in range(1, len(close)):
        tr = max(high[i] - low[i], abs(high[i] - close[i-1]), abs(low[i] - close[i-1]))
        trs.append(tr)
        dm_pos = max(high[i] - high[i-1], 0)
        dms_pos.append(dm_pos)
        dm_neg = max(low[i-1] - low[i], 0)
        dms_neg.append(dm_neg)
    
    atr = sum(trs[-period:]) / period
    di_pos = sum(dms_pos[-period:]) / atr / period * 100
    di_neg = sum(dms_neg[-period:]) / atr / period * 100
    return di_pos, di_neg




def ADX_14_CALCULATOR(yf_data,lock,ADX_2m,ADX_5m,minutes):
    adx_values = []
    period = 14
    high = yf_data['High'].tolist()
    low = yf_data['Low'].tolist()
    close = yf_data['Close'].tolist()
    
    for i in range(period, len(close)):
        high = close[i-period:i]
        low = close[i-period:i]
        close_values = close[i-period:i]
        di_pos, di_neg = DMI_CALCULATOR(high, low, close_values, period)
        adx = abs(di_pos - di_neg) / (di_pos + di_neg) * 100
        adx_values.append(adx)
    adx = sum(adx_values) / len(adx_values)
    with lock:
        if minutes == '2m':
            ADX_2m.append(round(adx,2))
        if minutes == '5m':
            ADX_5m.append(round(adx,2))






def TOTAL_TRADED_VOLUME(todays_data,event,lock,total_traded_volume):
    Volume = []
    
    for v in todays_data['Volume']:
        Volume.append(v)
    event.set()
    with lock:
        total_traded_volume.append(sum(Volume))


def ERROR_DETECTOR(text,word_to_find):
    pattern = r"\b{}\b".format(word_to_find)
    match = re.search(pattern, text)
    event.set()
    return bool(match)





def APPENDER(yf_data,minutes,time,RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock):
    if minutes == '2m':
        if time == 'before':
            todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]
            TOTAL_TRADED_VOLUME(todays_data,event,lock,total_traded_volume)
            event.wait()
        
        if time == 'after':
            TOTAL_TRADED_VOLUME(yf_data,event,lock,total_traded_volume)
            event.wait()
    
    RSI_14_CALCULATOR(yf_data.iloc[-14:],event,lock,RSI_2m,RSI_5m,minutes) 
    event.wait()
    ADX_14_CALCULATOR(yf_data.iloc[-15:],lock,ADX_2m,ADX_5m,minutes)
    
    event.set()



def DATA_FETCHER(stock,per,shrt_int):
    i=0
    def df_loop(stock,per,shrt_int,i):
        max_retries = 4
        yf_data = yf.download(stock, period=per, interval=shrt_int)
        print(f'fetching the data for {stock} once more, \t\t{i}th timeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.........')
        error_detector = ERROR_DETECTOR(str(yf_data), 'Empty DataFrame')
        event.wait()
        print (error_detector)
        print ('gotaaaaaaaaaaaaaaaaalllllllllllllllllllllllllllllllllllaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print (stock,'\n',yf_data.iloc[-1:])
        while error_detector == True:
            while i < max_retries:
                i+=1
                yf_data = df_loop(stock,per,shrt_int,i)
        return yf_data
    
    
    yf_data = yf.download(stock, period=per, interval=shrt_int)
    
    if ERROR_DETECTOR(str(yf_data), 'Empty DataFrame'):
        print("MISSION ABORTED..!! Its a Failed download, raising a ConnectionError while fetching the data.")
        print(f"Data fetching failed for {stock} Retrying...")
        #time.sleep(5)
        print('\nERROR HAS BEEN DETECTED yf_data ------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n',yf_data.iloc[-5:])
        i+=1
        
        yf_data = df_loop(stock,per,shrt_int,i)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print (yf_data)
        print (f"Executing the same function again.............for the {stock}...........in the WRONG EMPTY DATAFRAME block!!")
    
    event.set()
    print ('kkkkkkaaaaaaaaaaaassssssssaaaaaaaaaaaaaammmmmmmmmmmmmmmmmm seeeeeeeeeeeeeeee beeeeeeeeeeee...!!')
    print ('Bhai saaheb...!! ',stock,'\n',yf_data.iloc[-5:])
    return yf_data



def DATA_MANAGER(start,end,pChange,sector,basicIndustry,Stock,RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock,event):
    current_time = datetime.now()
    short_interval = '2m'
    long_interval ='5m'
    
    for i in range(start, end):
        
        jg_data = n.stock_quote(eqList[i])
        
        '''Data fetching for 2-minute candle'''
        target_change_hour, target_change_minute, target_change_second = 9, 45, 0
        target_change_time_1 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        if current_time <= target_change_time_1:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"2d",short_interval)
            event.wait()
            
            APPENDER(yf_data,short_interval,'before',RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock)
            event.wait()
            with lock:
                Stock.append(eqList[i])
                pChange.append(round(jg_data['priceInfo']['pChange'],2))
                sector.append(jg_data['industryInfo']['sector'])
                basicIndustry.append(jg_data['industryInfo']['basicIndustry'])
                
            #print("Introducing a 2-min delay.......")
            #time.sleep(120)
        else:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"1d",short_interval)
            event.wait()
            
            APPENDER(yf_data,short_interval,'after',RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock)
            event.wait()
            
            with lock:
                Stock.append(eqList[i])
                pChange.append(round(jg_data['priceInfo']['pChange'],2))
                sector.append(jg_data['industryInfo']['sector'])
                basicIndustry.append(jg_data['industryInfo']['basicIndustry'])
                
            #print("Introducing a 2-min delay.......")
            #time.sleep(120)
        
        
        '''Data fetching for 5-minute candle'''
        target_change_hour, target_change_minute, target_change_second = 10, 30, 0
        target_change_time_2 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        if current_time <= target_change_time_2:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"2d",long_interval)
            event.wait()
            APPENDER(yf_data,long_interval,'before',RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock)
            event.wait()
            #print("Introducing a 5-min delay.......")
            #time.sleep(300)
            
        else:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"1d",long_interval)
            event.wait()
            APPENDER(yf_data,long_interval,'after',RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock)
            event.wait()
            #print("Introducing a 5-min delay.......")
            #time.sleep(300)
    event.set()


def SCHEDULE_TASK(start,end,Stock,RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,pChange,sector,basicIndustry,lock):
    while True:
        current_time = target_start_time  #datetime.now()
        if current_time >= target_start_time:
            start_time = time.time()
            DATA_MANAGER(start,end,pChange,sector,basicIndustry,Stock,RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock,event)
            break
        print(current_time,' =======>>> ',target_start_time)
    event.wait()
    end_time = time.time()
    print(f"{process_name}'s Data fetching completed in {end_time - start_time:.2f} seconds extending from FROM = {start_time} TILL = {end_time}.")


@trading_system_server.route('/')
def index():
    sorted_final_output_dataframe = trading_system_server.config['sorted_pd']
    # Render the HTML template with DataFrame passed to it
    return render_template('index.html', tables=[sorted_final_output_dataframe.to_html(classes='data')])


if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    print('the code has started to run.......')
    
    Stock = manager.list()
    RSI_2m = manager.list()
    RSI_5m = manager.list()
    ADX_2m = manager.list()
    ADX_5m = manager.list()
    total_traded_volume = manager.list()
    pChange = manager.list()
    sector = manager.list()
    basicIndustry = manager.list()
    
    lock = manager.Lock()
    
    i=0
    num_processor_cores = multiprocessing.cpu_count()
    chunk_size = len(eqList) // num_processor_cores
    processes = []
    for i in range(num_processor_cores):
        start = i * chunk_size
        end = start + chunk_size if i < num_processor_cores - 1 else len(eqList)
        data_fetching_process = multiprocessing.Process(
            target=SCHEDULE_TASK, 
            args=(start,end,Stock,RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,
                pChange,sector,basicIndustry,lock))
        processes.append(data_fetching_process)
        data_fetching_process.start()

    
    for data_fetching_process in processes:
        data_fetching_process.join()
    
    final_output_dict = {}
    final_output_dict.update({'pChange': list(pChange)})
    final_output_dict.update({'Stock': list(Stock)})
    final_output_dict.update({'ADX(14) 2m': list(ADX_2m)})
    final_output_dict.update({'ADX(14) 5m': list(ADX_5m)})
    final_output_dict.update({'RSI(14) 2m': list(RSI_2m)})
    final_output_dict.update({'RSI(14) 5m': list(RSI_5m)})
    final_output_dict.update({'Total Volume': list(total_traded_volume)})
    final_output_dict.update({'Sector': list(sector)})
    final_output_dict.update({'Industry': list(basicIndustry)})

    print("\n\n\nThe Final dictionary -\n\n")
    for key,value in final_output_dict.items():
        print(f'{key} :- {value}\n')
    
    final_output_dataframe = pd.DataFrame(final_output_dict) #, index = final_output_dict['Stock'])
    print("\n\n\nTHE FINAL OUTPUT IS :-\n\n",final_output_dataframe)
    
    sorted_final_output_dataframe = final_output_dataframe.sort_values(by='RSI(14) 5m', ascending=False)
    print ("\n\n\nThe sorted Stock data :-\n")
    print (sorted_final_output_dataframe)
    # print ('\n\n\nThe FIRST 3 stocks with highest volume are -',sorted_final_output_dataframe.iloc[:3])
    # print ('\n\n\nThe LAST 3 stocks with highest volume are -',sorted_final_output_dataframe.iloc[-3:])
    
    trading_system_server.config['sorted_pd'] = sorted_final_output_dataframe
    trading_system_server.run(debug=True, use_reloader=True)