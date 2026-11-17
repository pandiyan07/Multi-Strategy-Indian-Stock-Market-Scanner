# Trading system v1 - data fetching & processing using Single process 


from nselib import capital_market
from jugaad_data.nse import NSELive
import pandas as pd
import multiprocessing
import tracemalloc
import time
import sys
from datetime import datetime
import yfinance as yf
import re

tracemalloc.start()
current_process = multiprocessing.current_process()
process_name = current_process.name

Stock = []
RSI_2m = []
RSI_5m = []
ADX_2m = []
ADX_5m = []
total_traded_volume = []
pChange = []
sector = []
basicIndustry = []

final_output_dict = {}
final_output_dataframe = pd.DataFrame(final_output_dict)


eqList = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS','BHARTIARTL.NS', 'SBIN.NS', 'INFY.NS', 'ITC.NS',
    'HINDUNILVR.NS', 'LT.NS', 'BAJFINANCE.NS', 'MARUTI.NS', 'HCLTECH.NS', 'SUNPHARMA.NS', 'NTPC.NS', 'ONGC.NS',
    'AXISBANK.NS', 'ADANIENT.NS', 'TATAMOTORS.NS', 'TITAN.NS', 'KOTAKBANK.NS', 'POWERGRID.NS', 'ADANIPORTS.NS',
    'ULTRACEMCO.NS', 'ASIANPAINT.NS', 'COALINDIA.NS', 'M&M.NS', 'BAJAJFINSV.NS', 'BAJAJ-AUTO.NS', 'NESTLEIND.NS',
    'WIPRO.NS', 'JSWSTEEL.NS', 'TATASTEEL.NS', 'GRASIM.NS', 'SBILIFE.NS', 'HINDALCO.NS', 'BPCL.NS',
    'EICHERMOT.NS', 'HDFCLIFE.NS', 'TECHM.NS', 'INDUSINDBK.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'DIVISLAB.NS',
    'DRREDDY.NS', 'TATACONSUM.NS', 'HEROMOTOCO.NS', 'APOLLOHOSP.NS', 'LTIM.NS', 'SHRIRAMFIN.NS'
]

#["INFY.NS","ITC.NS","WIPRO.NS","TCS.NS","ABB.NS","RELIANCE.NS","ICICIBANK.NS","SBIN.NS"] 
#print ('eqlist ------------------- ',eqList)
# 
n = NSELive()

target_start_hour, target_start_minute, target_start_second = 23, 59, 45
target_start_time = datetime.now().replace(hour=target_start_hour, minute=target_start_minute, second=target_start_second)




def RSI_14_CALCULATOR(yf_data,event3):
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
    #event3.set()
    #print(f"I am {process_name} in RSI\n\n\n")
    rsi = (100 - (100 / (1 + rs)))
    #rsi = rsi:.2f
    return round(rsi,2)



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




def ADX_14_CALCULATOR(yf_data,event4):
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
    #event4.set()
    #print(f"I am {process_name} in ADX\n\n\n")
    adx = sum(adx_values) / len(adx_values)
    return round(adx,2)






def TOTAL_TRADED_VOLUME(todays_data):
    #print('Total traded volume has been calculated :-')
    Volume = []
    for v in todays_data['Volume']:
        Volume.append(v)
    #print (sum(Volume))
    #print(f"I am {process_name} in TOTAL_TRADED_VOLUME\n\n\n")
    return sum(Volume)


def ERROR_DETECTOR(text,word_to_find):
    pattern = r"\b{}\b".format(word_to_find)
    match = re.search(pattern, text)
    #print(f"I am {process_name} in ERROR_DETECTOR\n\n\n")
    return bool(match)


def JUGAAD_DATA_FETCHER(start,end):
    event1 = multiprocessing.Event()
    jugaad_output = {}
    for i in range(start,end):
        q = n.stock_quote(eqList[i].replace(".NS", ""))
        '''jugaad_output.update({'pChange': q['priceInfo']['pChange']})
        jugaad_output.update({'sector': q['industryInfo']['sector']})
        jugaad_output.update({'basicIndustry': q['industryInfo']['basicIndustry']})'''
        #print(f"I am {process_name} in JUGAAD_DATA_FETCHER\n\n\n")
        #event1.set()
        #print (f'The JUGAAD_DATA_FETCHER() OUTPUT is :-\n{jugaad_output}\n\n')
        #event1.wait()
        pChange.append(q['priceInfo']['pChange'])
        sector.append(q['industryInfo']['sector'])
        basicIndustry.append(q['industryInfo']['basicIndustry'])
    return jugaad_output


def YF_DATA_FETCHER(start,end):
    current_time = datetime.now()
    current_process = multiprocessing.current_process()
    
    short_interval = '2m'
    long_interval ='5m'
    
    event2 = multiprocessing.Event()
    event3 = multiprocessing.Event()
    event4 = multiprocessing.Event()
    event5 = multiprocessing.Event()
    
    #op = {}
    yf_output = {}
    #print(f"I am {process_name} in YF_DATA_FETCHER\n\n\n")
    
    for i in range(start, end):
        def appender(yf_data,minutes,time):
            #event2.set()
            if ERROR_DETECTOR(str(yf_data), 'Empty DataFrame'):
                print("MISSION ABORTED..!! Its a Failed download, raising a ConnectionError while fetching the data.")
                #print(f"Data fetching failed for {stock} Retrying...")
                time.sleep(5)
                YF_DATA_FETCHER(start,end)
            else:
                #event2.wait()
                #print("Great..!! The are no ConnectionErrors while fetching the data.")
                if time == 'before':
                    todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]
                    volume = TOTAL_TRADED_VOLUME(todays_data)
                else:
                    volume = TOTAL_TRADED_VOLUME(yf_data)
                
                num_rows = len(yf_data)
                k = [k+1 for k in range(num_rows)]
                yf_data['Index'] = k
                yf_data = yf_data.reset_index(drop=True)
                yf_data = yf_data.set_index('Index')
                
                rsi = RSI_14_CALCULATOR(yf_data.iloc[-14:],event3) 
                adx = ADX_14_CALCULATOR(yf_data.iloc[-15:],event4)
                
                #event3.wait()
                #event4.wait()
                if minutes == short_interval:
                    ADX_2m.append(adx)
                    RSI_2m.append(rsi)
                    total_traded_volume.append(volume)
                    Stock.append(eqList[i].replace(".NS", ""))
                if minutes == long_interval:
                    ADX_5m.append(adx)
                    RSI_5m.append(rsi)
                
                
        
        '''Data fetching for 2-minute candle'''
        target_change_hour, target_change_minute, target_change_second = 9, 45, 0
        target_change_time_1 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        if current_time <= target_change_time_1:
            yf_data = yf.download(eqList[i], period="2d", interval=short_interval)
            #print("Fetching data for :- ",stock)
            #print("ITS BEFORE 9:45AM NOW -")
            #print(f"I am {process_name}\n\n\n")
            appender(yf_data,short_interval,'before')
            #print("Introducing a 2-min delay.......")
            #time.sleep(120)
        else:
            yf_data = yf.download(eqList[i], period="1d", interval=short_interval)
            #print("Fetching data for :- ",stock)
            #print("ITS AFTER 9:45AM NOW -")
            #print(f"I am {process_name}\n\n\n")
            appender(yf_data,short_interval,'after')
            #print("Introducing a 2-min delay.......")
            #time.sleep(120)
        
        
        '''Data fetching for 5-minute candle'''
        target_change_hour, target_change_minute, target_change_second = 10, 30, 0
        target_change_time_2 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        if current_time <= target_change_time_2:
            yf_data = yf.download(eqList[i], period="2d", interval=long_interval)
            #print("Fetching data for :- ",stock)
            #print("ITS BEFORE 10:30AM NOW -")
            #print(f"I am {process_name}\n\n\n")
            appender(yf_data,long_interval,'before')
            #print("Introducing a 5-min delay.......")
            #time.sleep(300)
        else:
            yf_data = yf.download(eqList[i], period="1d", interval=long_interval)
            #print("Fetching data for :- ",stock)
            #print("ITS AFTER 10:30AM NOW -")
            #print(f"I am {process_name} \n\n\n")
            appender(yf_data,long_interval,'after')
            #print("Introducing a 5-min delay.......")
            #time.sleep(300)
    #event5.set()
    #yf_output = op 
    #print("\n\n\n\n\nthe YF_DATA_FETCHER() yf_output issssssssssssssssssssssssssssssssssssss = \n",yf_output,"\n\n\n\n")
    return yf_output,event5



def DATAFRAME_GENERATOR(event6):
    #event6.wait()
    #print ("\n\n\n\nPROCESSING IS OVER")
    #print(f"I am {process_name} in DATAFRAME_GENERATOR\n\n\n")
    
    
    '''
    sorted_final_output_dataframe = final_output_dataframe.sort_values(by='Total Volume', ascending=False)
    print ("\n\n\nThe sorted Stock data :-\n")
    print (sorted_final_output_dataframe)
    print ('\nThe FIRST 3 stocks with highest volume are -',sorted_final_output_dataframe.iloc[:3])
    print ('\nThe LAST 3 stocks with highest volume are -',sorted_final_output_dataframe.iloc[-3:])
    '''

def FINAL_OUTPUT_DATAFRAME(jugaad_output,yf_output,event6):
    #print ("\n\nFINAL_OUTPUT_DATAFRAME() jugaad_output is :-\n",jugaad_output)
    #print ("\n\nFINAL_OUTPUT_DATAFRAME() yf_output is :-\n",yf_output)
    #print(f"I am {process_name} in FINAL_OUTPUT_DATAFRAME\n\n\n")
    
    
    

    for i in range(len(eqList)*2):
        i+=1
        #event6.set()
        if i == len(eqList):
            
            final_output_dict.update({'pChange': pChange})
            final_output_dict.update({'Stock': Stock})
            final_output_dict.update({'ADX(14) 2m': ADX_2m})
            final_output_dict.update({'ADX(14) 5m': ADX_5m})
            final_output_dict.update({'RSI(14) 2m': RSI_2m})
            final_output_dict.update({'RSI(14) 5m': RSI_5m})
            final_output_dict.update({'Total Volume': total_traded_volume})
            final_output_dict.update({'Sector': sector})
            final_output_dict.update({'Industry': basicIndustry})
            #DATAFRAME_GENERATOR(event6)
            
            print("\n\n\nThe Final dictionary -\n\n")
            for key,value in final_output_dict.items():
                print(f'{key} :- {value}\n\n')
            
            final_output_dataframe = pd.DataFrame(final_output_dict) #, index = final_output_dict['Stock'])
            print("\n\n\nTHE FINAL OUTPUT IS :-\n\n",final_output_dataframe.iloc[-3:])
            
            sorted_final_output_dataframe = final_output_dataframe.sort_values(by='RSI(14) 5m', ascending=False)
            print ("\n\n\nThe SORTED STOCK DATA output is :-\n")
            print (sorted_final_output_dataframe.iloc[-10:])






def SCHEDULE_TASK(start,end):
    #print(f"I am {process_name} in SCHEDULE_TASK\n\n\n")
    event6 = multiprocessing.Event()
    print ("THE START IS :-",start)
    print ("THE END IS :-",end)
    while True:
        current_time = target_start_time  #datetime.now()
        if current_time >= target_start_time:
            #print("scheduling the task....")
            start_time = time.time()
            jugaad_output = JUGAAD_DATA_FETCHER(start,end)
            print ("SCHEDULE_TASK() jugaad_output is :-\n",jugaad_output)
            yf_output,event5 = YF_DATA_FETCHER(start,end)
            print ("\n\nSCHEDULE_TASK() yf_output is :-\n",yf_output)
            end_time = time.time()
            
            FINAL_OUTPUT_DATAFRAME(jugaad_output,yf_output,event6)
            break
        print(current_time,' =======>>> ',target_start_time)
        time.sleep(1)
    print(f"Data fetching completed in {end_time - start_time:.2f} seconds.")
    #event5.wait()
    





if __name__ == '__main__':
    multiprocessing.freeze_support()
    print ("\n\nThe server has started running...")
    if target_start_time < datetime.now():
        print (f"Adangomma, the specified time {target_start_time} has already passed daa....!!")
        print ("exiting the program !!")
        sys.exit(1)

    i=0
    num_processor_cores = multiprocessing.cpu_count()
    chunk_size = len(eqList) // num_processor_cores
    processes = []
    
    
    # Delete this entire block of code once the testing with a single stock finishes
    start = 1
    end = len(eqList)
    data_fetching_process = multiprocessing.Process(target=SCHEDULE_TASK, args=(start,end))
    data_fetching_process.start()
    data_fetching_process.join()
    
    current_memory_usage = tracemalloc.get_traced_memory()[0]/(1024*1024)
    peak_memory_usage = tracemalloc.get_traced_memory()[1]/(1024*1024)
    # stopping the tracemalloc library
    tracemalloc.stop()

    print(f"\n\nCurrent Memory usage:- {current_memory_usage:.2f} MB")
    print(f"Peak Memory usage:- {peak_memory_usage:.2f} MB")