# Trading system v2 - data fetching using python Multiplprocessing library with multiple processes

from nselib import capital_market
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



eqList = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'ICICIBANK', 'BHARTIARTL', 'SBIN', 'INFY', 'ITC',
    'HINDUNILVR', 'LT', 'BAJFINANCE', 'MARUTI', 'HCLTECH', 'SUNPHARMA', 'NTPC', 'ONGC',
    'AXISBANK', 'ADANIENT', 'TATAMOTORS', 'TITAN', 'KOTAKBANK', 'POWERGRID', 'ADANIPORTS',
    'ULTRACEMCO', 'ASIANPAINT', 'COALINDIA', 'M&M', 'BAJAJFINSV', 'BAJAJ-AUTO', 'NESTLEIND',
    'WIPRO', 'JSWSTEEL', 'TATASTEEL', 'GRASIM', 'SBILIFE', 'HINDALCO', 'BPCL',
    'EICHERMOT', 'HDFCLIFE', 'TECHM', 'INDUSINDBK', 'BRITANNIA', 'CIPLA', 'DIVISLAB',
    'DRREDDY', 'TATACONSUM', 'HEROMOTOCO', 'APOLLOHOSP','LTIM','SHRIRAMFIN'
]

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
        max_retries = 10
        yf_data = yf.download(stock, period=per, interval=shrt_int)
        print(f'fetching the data for {stock} once more, \t\t{i}th time')
        error_detector = ERROR_DETECTOR(str(yf_data), 'Empty DataFrame')
        event.wait()
        print (error_detector)
        print (stock,'\n',yf_data.iloc[-2:])
        while error_detector == True:
            while i < max_retries:
                i+=1
                yf_data = df_loop(stock,per,shrt_int,i)
            return yf_data
    
    
    yf_data = yf.download(stock, period=per, interval=shrt_int)
    
    if ERROR_DETECTOR(str(yf_data), 'Empty DataFrame'):
        print("MISSION ABORTED..!! Its a Failed download, raising a ConnectionError while fetching the data.")
        print(f"Data fetching failed for {stock} Retrying...")
        i+=1
        yf_data = df_loop(stock,per,shrt_int,i)
        print (f"Executing the same function again.............for the {stock}...........in the WRONG EMPTY DATAFRAME block!!")
    
    event.set()
    return yf_data



def DATA_MANAGER(start,end,pChange,sector,basicIndustry,Stock,RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock,event):
    current_time = datetime.now()
    short_interval = '2m'
    long_interval ='5m'
    
    for i in range(start, end):
        
        jg_data = n.stock_quote(eqList[i])  #.replace(".NS", ""))
        
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
                Stock.append(eqList[i].replace(".NS", ""))
                pChange.append(round(jg_data['priceInfo']['pChange'],2))
                sector.append(jg_data['industryInfo']['sector'])
                basicIndustry.append(jg_data['industryInfo']['basicIndustry'])
                
        else:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"1d",short_interval)
            event.wait()
            
            APPENDER(yf_data,short_interval,'after',RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock)
            event.wait()
            
            with lock:
                Stock.append(eqList[i].replace(".NS", ""))
                pChange.append(round(jg_data['priceInfo']['pChange'],2))
                sector.append(jg_data['industryInfo']['sector'])
                basicIndustry.append(jg_data['industryInfo']['basicIndustry'])
                
        
        
        '''Data fetching for 5-minute candle'''
        target_change_hour, target_change_minute, target_change_second = 10, 30, 0
        target_change_time_2 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        if current_time <= target_change_time_2:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"2d",long_interval)
            event.wait()
            APPENDER(yf_data,long_interval,'before',RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock)
            event.wait()
        else:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"1d",long_interval)
            event.wait()
            APPENDER(yf_data,long_interval,'after',RSI_2m,RSI_5m,ADX_2m,ADX_5m,total_traded_volume,lock)
            event.wait()
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



if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
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
        print(f'{key} :- {value}\n\n')
        print('\n',len(value))
    
    final_output_dataframe = pd.DataFrame(final_output_dict) 
    print("\n\n\nTHE FINAL OUTPUT IS :-\n\n",final_output_dataframe)
    
    sorted_final_output_dataframe = final_output_dataframe.sort_values(by='RSI(14) 5m', ascending=False)
    print ("\n\n\nThe sorted Stock data :-\n")
    print (sorted_final_output_dataframe)
    print ('\n\n\nThe FIRST 3 stocks with highest volume are -',sorted_final_output_dataframe.iloc[:7])
