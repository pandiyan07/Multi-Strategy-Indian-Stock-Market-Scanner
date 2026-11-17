# Trading system v3 - data fetching for every 2 minutes in a loop using the python Multiplprocessing library
# with the help of multiple processes running simultaneously on each core of the prcessor requesting one stock name at a time
# Run the code from 9:16am

# Removed the ADX caluculation completely

#python "d:/Trading/Python/Code/Trading system v3.py"

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

try:
    n = NSELive()
except:
    print ('There is NO INTERNET CONNECTION dude...!!')
    sys.exit(1)



# RUN THIS CODE FROM - 9:16am


eqList = ["ABB", "ACC", "APLAPOLLO", "AUBANK", "ADANIENSOL", "ADANIENT", "ADANIGREEN", "ADANIPORTS", 
"ADANIPOWER", "ATGL", "ABCAPITAL", "ABFRL", "ALKEM", "AMBUJACEM", "APOLLOHOSP", "APOLLOTYRE", "ASHOKLEY", 
"ASIANPAINT", "ASTRAL", "AUROPHARMA", "DMART", "AXISBANK", "BSE", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", 
"BAJAJHLDNG", "BALKRISIND", "BANDHANBNK", "BANKBARODA", "BANKINDIA", "MAHABANK", "BERGEPAINT", "BDL", "BEL", 
"BHARATFORG", "BHEL", "BPCL", "BHARTIARTL", "BIOCON", "BOSCHLTD", "BRITANNIA", "CGPOWER", "CANBK", "CHOLAFIN", 
"CIPLA", "COALINDIA", "COFORGE", "COLPAL", "CONCOR", "CUMMINSIND", "DLF", "DABUR", "DALBHARAT", "DEEPAKNTR", 
"DELHIVERY", "DIVISLAB", "DIXON", "LALPATHLAB", "DRREDDY", "EICHERMOT", "ESCORTS", "NYKAA", "FEDERALBNK", 
"FACT", "FORTIS", "GAIL", "GMRINFRA", "GLAND", "GODREJCP", "GODREJPROP", "GRASIM", "GUJGASLTD", "HCLTECH", 
"HDFCAMC", "HDFCBANK", "HDFCLIFE", "HAVELLS", "HEROMOTOCO", "HINDALCO", "HAL", "HINDPETRO", "HINDUNILVR", 
"ICICIBANK", "ICICIGI", "ICICIPRULI", "IDBI", "IDFCFIRSTB", "ITC", "INDIANB", "INDHOTEL", "IOC", "IRCTC", 
"IRFC", "IGL", "INDUSTOWER", "INDUSINDBK", "NAUKRI", "INFY", "INDIGO", "IPCALAB","JSWENERGY", "JSWINFRA",
"JSWSTEEL", "JINDALSTEL", "JIOFIN", "JUBLFOOD", "KPITTECH", "KALYANKJIL",
"KOTAKBANK", "LTF", "LTTS", "LICHSGFIN", "LTIM", "LT", "LAURUSLABS", "LICI", "LUPIN", "MRF", "LODHA", "M&MFIN",
"M&M", "MANKIND", "MARICO", "MARUTI", "MFSL", "MAXHEALTH", "MAZDOCK", "MPHASIS", "NHPC", "NMDC", "NTPC",
"NESTLEIND", "OBEROIRLTY", "ONGC", "OIL", "PAYTM", "OFSS", "POLICYBZR", "PIIND", "PAGEIND", "PATANJALI",
"PERSISTENT", "PETRONET", "PIDILITIND", "PEL", "POLYCAB", "POONAWALLA", "PFC", "POWERGRID", "PRESTIGE", "PNB",
"RECLTD", "RVNL", "RELIANCE", "SBICARD", "SBILIFE", "SJVN", "SRF", "MOTHERSON", "SHREECEM", "SHRIRAMFIN", "SIEMENS",
"SONACOMS", "SBIN", "SAIL", "SUNPHARMA", "SUNTV", "SUPREMEIND", "SUZLON", "SYNGENE", "TVSMOTOR", "TATACHEM",
"TATACOMM", "TCS", "TATACONSUM", "TATAELXSI", "TATAMTRDVR", "TATAMOTORS", "TATAPOWER", "TATASTEEL", "TATATECH",
"TECHM", "TITAN", "TORNTPHARM", "TORNTPOWER", "TRENT", "TIINDIA", "UPL", "ULTRACEMCO", "UNIONBANK", "MCDOWELL-N",
"VBL", "VEDL", "IDEA", "VOLTAS", "WIPRO", "YESBANK", "ZEEL", "ZOMATO", "ZYDUSLIFE"]




target_start_hour, target_start_minute, target_start_second = 23, 59, 45  # CHANGE THIS TO 9:15 AM
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
    if avg_loss != 0:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi = round(rsi,2)
    else:
        rsi = 100
    event.set()
    
    with lock:
        if minutes == '2m':
            RSI_2m.append(round(rsi,2))
        if minutes == '5m':
            RSI_5m.append(round(rsi,2))





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





def APPENDER(yf_data,minutes,time,RSI_2m,RSI_5m,total_traded_volume,lock):
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
    
    event.set()



def DATA_FETCHER(stock,per,shrt_int):
    i=0
    def df_loop(stock,per,shrt_int,i):
        max_retries = 4
        yf_data = yf.download(stock, period=per, interval=shrt_int)
        error_detector = ERROR_DETECTOR(str(yf_data), 'Empty DataFrame')
        event.wait()
        while error_detector == True:
            while i < max_retries:
                i+=1
                yf_data = df_loop(stock,per,shrt_int,i)
                print ('fetched the data once again successfully...!!')
        return yf_data
    
    yf_data = yf.download(stock, period=per, interval=shrt_int)
    
    if ERROR_DETECTOR(str(yf_data), 'Empty DataFrame'):
        print("MISSION ABORTED..!! Its a Failed download, raising a ConnectionError while fetching the data.")
        i+=1
        yf_data = df_loop(stock,per,shrt_int,i)
    
    event.set()
    return yf_data



def DATA_MANAGER(start,end,pChange,sector,basicIndustry,Stock,RSI_2m,RSI_5m,total_traded_volume,lock,event,promising_stock):
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
            
            APPENDER(yf_data,short_interval,'before',RSI_2m,RSI_5m,total_traded_volume,lock)
            event.wait()
            
        else:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"1d",short_interval)
            event.wait()
            
            APPENDER(yf_data,short_interval,'after',RSI_2m,RSI_5m,total_traded_volume,lock)
            event.wait()
            
        with lock:
            Stock.append(eqList[i])
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
            
            APPENDER(yf_data,long_interval,'before',RSI_2m,RSI_5m,total_traded_volume,lock)
            event.wait()
            
        else:
            with lock:
                yf_data = DATA_FETCHER(eqList[i]+'.NS',"1d",long_interval)
            event.wait()
            
            APPENDER(yf_data,long_interval,'after',RSI_2m,RSI_5m,total_traded_volume,lock)
            event.wait()
    event.set()


def SCHEDULE_TASK(start,end,Stock,RSI_2m,RSI_5m,total_traded_volume,pChange,sector,basicIndustry,lock,promising_stock):
    while True:
        current_time = target_start_time  #datetime.now()
        if current_time >= target_start_time:
            start_time = time.time()
            DATA_MANAGER(start,end,pChange,sector,basicIndustry,Stock,RSI_2m,RSI_5m,total_traded_volume,lock,event,promising_stock)
            break
        print(current_time,' =======>>> ',target_start_time)
    event.wait()
    end_time = time.time()
    with lock:
        print(f"{process_name}'s Data fetching completed in {end_time - start_time:.2f} seconds extending from FROM = {start_time} TILL = {end_time}.")





if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    print('the code has started to run.......')
    print (len(eqList))
    
    Stock = manager.list()
    RSI_2m = manager.list()
    RSI_5m = manager.list()
    total_traded_volume = manager.list()
    pChange = manager.list()
    sector = manager.list()
    basicIndustry = manager.list()
    promising_stock = manager.list()
    
    lock = manager.Lock()
    
    processes = []
    final_output_dict = {}
    j=0
    
    
    while True:
        start_time = datetime.now()
        #start_time = start_time.replace(hour=9, minute=16, second=0, microsecond=0)       
        i=0
        num_processor_cores = multiprocessing.cpu_count()
        chunk_size = len(eqList) // num_processor_cores
        
        for i in range(num_processor_cores):
            start = i * chunk_size
            end = start + chunk_size if i < num_processor_cores - 1 else len(eqList)
            data_fetching_process = multiprocessing.Process(
                target=SCHEDULE_TASK, 
                args=(start,end,Stock,RSI_2m,RSI_5m,total_traded_volume,
                    pChange,sector,basicIndustry,lock,promising_stock))
            processes.append(data_fetching_process)
            data_fetching_process.start()
        
        for process in processes:
            process.join()
        
        nifty200 = n.live_index("NIFTY 200")
        
        final_output_dict.update({'pChange': list(pChange)})
        final_output_dict.update({'RSI(14) 2m': list(RSI_2m)})
        final_output_dict.update({'Stock': list(Stock)})        
        final_output_dict.update({'RSI(14) 5m': list(RSI_5m)})
        final_output_dict.update({'Total Volume': list(total_traded_volume)})
        final_output_dict.update({'Sector': list(sector)})
        final_output_dict.update({'Industry': list(basicIndustry)})


        pp = 0      # percentage positive
        pm = 0      # percentage positive
        for perc in pChange :
            if perc > 1:
                pp+=1
            if perc < -1:
                pm+=1
        
        
        final_output_dataframe = pd.DataFrame(final_output_dict) #, index = final_output_dict['Stock'])
        
        ''' TOP 10 RSI STOCKS '''
        top_sorted_final_output_dataframe = final_output_dataframe.sort_values(by='RSI(14) 5m', ascending=False)
        num_rows = len(top_sorted_final_output_dataframe)
        k = [k+1 for k in range(num_rows)]
        top_sorted_final_output_dataframe['Index'] = k
        top_sorted_final_output_dataframe = top_sorted_final_output_dataframe.reset_index(drop=True)
        top_sorted_final_output_dataframe = top_sorted_final_output_dataframe.set_index('Index')
        
        ''' BOTTOM 10 RSI STOCKS '''
        bottom_sorted_final_output_dataframe = final_output_dataframe.sort_values(by='RSI(14) 5m', ascending=True)
        num_rows = len(bottom_sorted_final_output_dataframe)
        k = [k+1 for k in range(num_rows)]
        bottom_sorted_final_output_dataframe['Index'] = k
        bottom_sorted_final_output_dataframe = bottom_sorted_final_output_dataframe.reset_index(drop=True)
        bottom_sorted_final_output_dataframe = bottom_sorted_final_output_dataframe.set_index('Index')
        
        advances = nifty200['advance']['advances']
        declines = nifty200['advance']['declines']
        unchanged = nifty200['advance']['unchanged']
        
        j+=1
        if j > 0:
            print ('\n\n\n\n\n\n\nIteration number - ',j)
        current_time = datetime.now()
        print ('CURRENT TIME = ',current_time.strftime("%H:%M:%S"))
        print ('pp = ',pp)
        print ('pm = ',pm)
        print (pp+pm,'stocks are PROMISING STOCKS')
        print(f"\nNIFTY 200 current status -\nAdvances :- {advances}\nDeclines :- {declines}\nUnchanged :- {unchanged}\n")
        print ("\nThe TOP 10 RSI STOCKS are :-\n")
        print (top_sorted_final_output_dataframe.iloc[:10])
        #print ('\n\n')
        print ("\n\nThe BOTTOM 10 RSI STOCKS are :-\n")
        print (bottom_sorted_final_output_dataframe.iloc[:10])
        
        
        Stock = manager.list()
        RSI_2m = manager.list()
        RSI_5m = manager.list()
        total_traded_volume = manager.list()
        pChange = manager.list()
        sector = manager.list()
        basicIndustry = manager.list()
        #promising_stock = manager.list()
        
        processes = []
        final_output_dict = {}

        
        # Calculate the time difference between now and the start time
        time_difference = current_time - start_time
        #time_left = 10 + time_difference.total_seconds()
        print (f'\n\nIt took {time_difference} seconds to run & complete this program')
        #print (f'sleeeping for {time_left} seconds.....')
        print (f'sleeeping for 10 seconds.....')
        time.sleep(10) 