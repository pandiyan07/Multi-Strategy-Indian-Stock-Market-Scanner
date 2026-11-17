#python "d:/Trading/Python/Code/Trading system v4.py"

'''
Trading system v4 - 
we are going to download all the stock's data at once in a single request to the server
for every 2 minutes in a forever loop
.
we will use multiprocessing library to run multiple processes running simultaneously on each core of the prcessor
for processing data simultaneuosly
.
We have introduced 2 set of threads, 1 set is for fetching data and
another set is for calculating using the same fetched data
'''

from nselib import capital_market
from jugaad_data.nse import NSELive
import pandas as pd
import multiprocessing
import time
import sys
from datetime import datetime
import yfinance as yf

current_process = multiprocessing.current_process()
process_name = current_process.name
event = multiprocessing.Event()
try:
    n = NSELive()
except:
    print ('There is NO INTERNET CONNECTION dude...!!')
    sys.exit(1)



# RUN THIS CODE FROM THE START OF THE MARKET AT - 9:16am


#eqList = ["INFY.NS","ITC.NS","WIPRO.NS","TCS.NS", 'HDFCBANK.NS', 'ICICIBANK.NS','BHARTIARTL.NS', 'SBIN.NS', "AUBANK.NS", "HEROMOTOCO.NS"]



eqList = ["ABB.NS", "ACC.NS","APLAPOLLO.NS", "AUBANK.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "MCDOWELL-N.NS",
"ADANIPOWER.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", 
"ASIANPAINT.NS", "ASTRAL.NS", "AUROPHARMA.NS", "DMART.NS", "AXISBANK.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", 
"BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "MAHABANK.NS", "BERGEPAINT.NS", "BDL.NS",  
"BHARATFORG.NS", "BHEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BRITANNIA.NS", "CGPOWER.NS", "CANBK.NS", "CHOLAFIN.NS", 
"CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "CUMMINSIND.NS", "DLF.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", 
"DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS", "LALPATHLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "NYKAA.NS", "FEDERALBNK.NS", 
"FACT.NS", "FORTIS.NS", "GAIL.NS", "GMRINFRA.NS", "GLAND.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRASIM.NS", "GUJGASLTD.NS", "HCLTECH.NS", 
"HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HAVELLS.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HAL.NS", "HINDPETRO.NS", "HINDUNILVR.NS", 
"ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDBI.NS", "IDFCFIRSTB.NS", "ITC.NS", "INDIANB.NS", "INDHOTEL.NS", "IOC.NS", "SIEMENS.NS",
"IRFC.NS", "IGL.NS", "INDUSTOWER.NS", "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS", "INDIGO.NS", "IPCALAB.NS","JSWENERGY.NS", "JSWINFRA.NS",
"JSWSTEEL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "KPITTECH.NS", "KALYANKJIL.NS","BEL.NS","IRCTC.NS","PNB.NS","M&MFIN.NS",
"KOTAKBANK.NS", "LTF.NS", "LTTS.NS", "LICHSGFIN.NS", "LTIM.NS", "LT.NS", "LAURUSLABS.NS", "LICI.NS", "LUPIN.NS", "MRF.NS", "LODHA.NS", 
"M&M.NS", "MANKIND.NS", "MARICO.NS", "MARUTI.NS", "MFSL.NS", "MAXHEALTH.NS", "MAZDOCK.NS", "MPHASIS.NS", "NHPC.NS", "NMDC.NS", "NTPC.NS",
"NESTLEIND.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "PAYTM.NS", "OFSS.NS", "POLICYBZR.NS", "PIIND.NS", "PAGEIND.NS", "PATANJALI.NS",
"PERSISTENT.NS", "PETRONET.NS", "PIDILITIND.NS", "PEL.NS", "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", "POWERGRID.NS", "PRESTIGE.NS", 
"RECLTD.NS", "RVNL.NS", "RELIANCE.NS", "SBICARD.NS", "SBILIFE.NS", "SJVN.NS", "SRF.NS", "MOTHERSON.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", 
"SONACOMS.NS", "SBIN.NS", "SAIL.NS", "SUNPHARMA.NS", "SUNTV.NS", "SUPREMEIND.NS", "SUZLON.NS", "SYNGENE.NS", "TVSMOTOR.NS", "TATACHEM.NS",
"TATACOMM.NS", "TCS.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAMTRDVR.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS",
"TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TIINDIA.NS", "UPL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "ZYDUSLIFE.NS",
"VBL.NS", "VEDL.NS", "IDEA.NS", "VOLTAS.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS"]



target_start_hour, target_start_minute, target_start_second = 23, 59, 45  # CHANGE THIS TO 9:16 AM
target_start_time = datetime.now().replace(hour=target_start_hour, minute=target_start_minute, second=target_start_second)


def RSI_14_CALCULATOR(yf_cp_list,event):
    i=1
    if len(yf_cp_list) >= 14:  
        price_diffs = [yf_cp_list[i] - yf_cp_list[i - 1] for i in range(1, len(yf_cp_list))]
    else:
        print("WARNING :- NUMBER OF PRICES ARE LESS THAN 14 DATA POINTS...!!\n")
        print('The length of close price list is = \n',len(yf_cp_list))
        print ('\n\n\n\n\n\n So thats why exiting the programe................. \n\n\n\n\n\n')
        sys.exit(1)
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
        
    event.set() #3
    return rsi


def TOTAL_TRADED_VOLUME(todays_data,event):
    Volume = []
    for v in todays_data['Volume']:
        Volume.append(v)
    event.set() #4
    return sum(Volume)





def APPENDER(start, end, yfd_dict, vol_cal, RSI_2m, RSI_5m, RSI_1d, RSI_1wk, RSI_1mo, Stock,
            total_traded_volume, pChange,sector, basicIndustry, lock):
    for i in range(start, end): 
        yf_all_stocks_data = yfd_dict['2m']
        yf_data = yf_all_stocks_data[(eqList[i])]
        
        jg_data = n.stock_quote(eqList[i].replace(".NS", ""))
        
        if vol_cal == 'before': 
            todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]
            volume = TOTAL_TRADED_VOLUME(todays_data,event)
        
        if vol_cal == 'after': 
            volume = TOTAL_TRADED_VOLUME(yf_data,event)
        event.wait()    #4
        
        with lock:
            total_traded_volume.append(volume)
            Stock.append(jg_data['info']['symbol'])
            pChange.append(round(jg_data['priceInfo']['pChange'],2))
            sector.append(jg_data['industryInfo']['sector'])
            basicIndustry.append(jg_data['industryInfo']['basicIndustry'])
        
        
        
        for key,value in yfd_dict.items():
            v = list(value.columns.levels)
            yf_all_stocks_data = value
            yf_data = yf_all_stocks_data.iloc[-14:]
            yf_cp_list = yf_data[(eqList[i], 'Close')].tolist()
            
            rsi = RSI_14_CALCULATOR(yf_cp_list, event)
            event.wait()    #3
            
            with lock:
                if key == '2m':
                    RSI_2m.append(rsi)
                if key == '5m':
                    RSI_5m.append(rsi)
                if key == '1d':
                    RSI_1d.append(rsi)
                if key == '1wk':
                    RSI_1wk.append(rsi)
                if key == '1mo':
                    RSI_1mo.append(rsi)



def DATA_FETCHER(per,inte):
    yf_all_stocks_data = yf.download(eqList, group_by='Ticker', period=per, interval=inte)
    event.set() #1
    return yf_all_stocks_data



def SCHEDULE_TASK(y,yfd_dict,lock,vol_cal):
    if y < 6 :
        if vol_cal == 'before': 
            period_interval = {
                1 : ["2d",'2m'],
                2 : ["2d",'5m'],
                3 : ["15d",'1d'],
                4 : ["15wk",'1wk'],
                5 : ["15mo",'1mo']
            }
        if vol_cal == 'after': 
            period_interval = {
                1 : ["1d",'2m'],
                2 : ["1d",'5m'],
                3 : ["15d",'1d'],
                4 : ["15wk",'1wk'],
                5 : ["15mo",'1mo']
            }
        pi = period_interval[y]
        while True:
            current_time = target_start_time  #datetime.now()
            if current_time >= target_start_time:
                yf_all_stocks_data = DATA_FETCHER(pi[0],pi[1])
                
                with lock:
                    yfd_dict.update({pi[1]:yf_all_stocks_data})
                    event.wait()    #1
                break
            print(current_time,' =======>>> ',target_start_time)
            time.sleep(5)



if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    print('the code has started to run.......')
    if target_start_time < datetime.now():
        print (f"Adangomma, the specified time {target_start_time} has already passed daa....!!")
        print ("exiting the program !!")
        sys.exit(1)
    
    Stock = manager.list()
    pChange = manager.list()
    sector = manager.list()
    basicIndustry = manager.list()
    total_traded_volume = manager.list()
    RSI_2m = manager.list()
    RSI_5m = manager.list()
    RSI_1d = manager.list()
    RSI_1wk = manager.list()
    RSI_1mo = manager.list()
    yfd_dict = manager.dict()
    
    
    lock = manager.Lock()
    
    processes = []
    final_output_dict = {}
    j=0
    
    
    
    while True:
        
        # use this start_time for automating the server to run from 9:16
        start_time = datetime.now()
        #start_time = start_time.replace(hour=9, minute=16, second=0, microsecond=0)
        
        target_change_hour, target_change_minute, target_change_second = 10, 30, 0
        target_change_time_1 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        current_time = datetime.now()
        if current_time <= target_change_time_1:
            vol_cal = 'before'
        else:
            vol_cal = 'after'
        
        i=0
        y=0
        
        for i in range(0,5):
            y+=1
            data_fetching_process = multiprocessing.Process(
                target=SCHEDULE_TASK, 
                args=(y,yfd_dict,lock,vol_cal))
            processes.append(data_fetching_process)
            data_fetching_process.start()
        for process in processes:
            process.join()
        
        
        current_time = datetime.now()
        # Calculate the time difference between now and the start time
        time_difference = current_time - start_time
        print (f'\n\nIt took {time_difference} seconds to run & FETCH THE YF DATA FOR ALL THE ABOVE MENTIONED 4 INTERVALS \n\n')
        
        
        i=0
        
        num_processor_cores = multiprocessing.cpu_count()
        chunk_size = len(eqList) // num_processor_cores
        
        for i in range(num_processor_cores):
            start = i * chunk_size
            end = start + chunk_size if i < num_processor_cores - 1 else len(eqList)
            
            data_fetching_process = multiprocessing.Process(
                target=APPENDER, 
                args=(start,end,yfd_dict,vol_cal,RSI_2m, RSI_5m, RSI_1d, RSI_1wk, RSI_1mo,Stock,
                    total_traded_volume, pChange,sector, basicIndustry, lock))
            processes.append(data_fetching_process)
            data_fetching_process.start()
        
        for process in processes:
            process.join()
        
        nifty200 = n.live_index("NIFTY 200")
        
        final_output_dict.update({'pChange': list(pChange)})
        final_output_dict.update({'RSI(14) 2m': list(RSI_2m)})
        final_output_dict.update({'Stock': list(Stock)})
        final_output_dict.update({'RSI(14) 5m': list(RSI_5m)})
        final_output_dict.update({'RSI(14) 1d': list(RSI_1d)})
        final_output_dict.update({'RSI(14) 1wk': list(RSI_1wk)})
        final_output_dict.update({'RSI(14) 1mo': list(RSI_1mo)})
        final_output_dict.update({'Total Volume': list(total_traded_volume)})
        #final_output_dict.update({'Sector': list(sector)})
        #final_output_dict.update({'Industry': list(basicIndustry)})
        
        
        current_time = datetime.now()
        time_difference = current_time - start_time
        print (f'\n\n IT TOOK {time_difference} SECONDS TO CREATE THE FINAL OUTPUT DICTIONARY \n\n')
        
        pp = 0
        pm = 0
        for perc in pChange :
            if perc > 1:
                pp+=1
            if perc < -1:
                pm+=1
        
        advances = int(nifty200['advance']['advances'])
        declines = int(nifty200['advance']['declines'])
        unchanged = int(nifty200['advance']['unchanged'])
        
        final_output_dataframe = pd.DataFrame(final_output_dict) #, index = final_output_dict['Stock'])
        
        if advances >= declines:
            ''' TOP 10 RSI STOCKS '''
            sorted_final_output_dataframe = final_output_dataframe.sort_values(by='RSI(14) 5m', ascending=False)
        else:
            ''' BOTTOM 10 RSI STOCKS '''
            sorted_final_output_dataframe = final_output_dataframe.sort_values(by='RSI(14) 5m', ascending=True)
        
        num_rows = len(sorted_final_output_dataframe)
        k = [k+1 for k in range(num_rows)]
        sorted_final_output_dataframe['Index'] = k
        sorted_final_output_dataframe = sorted_final_output_dataframe.reset_index(drop=True)
        sorted_final_output_dataframe = sorted_final_output_dataframe.set_index('Index')
        
        j+=1
        if j > 0:
            print ('\n\n\nIteration number - ',j)
        
        print ('CURRENT TIME = ',current_time.strftime("%H:%M:%S"))
        
        print ('pp = ',pp)
        print ('pm = ',pm)
        print (pp+pm,'stocks are PROMISING STOCKS')
        
        print(f"\nNIFTY 200 current status -\nAdvances :- {advances}\nDeclines :- {declines}\nUnchanged :- {unchanged}\n")
        if advances >= declines:
            print ("\nThe TOP 10 RSI STOCKS are :-\n")
            print (sorted_final_output_dataframe.iloc[:10])
        else:
            print ("\nThe BOTTOM 10 RSI STOCKS are :-\n")
            print (sorted_final_output_dataframe.iloc[:10])
        
        
        Stock = manager.list()
        pChange = manager.list()
        sector = manager.list()
        basicIndustry = manager.list()
        total_traded_volume = manager.list()
        RSI_2m = manager.list()
        RSI_5m = manager.list()
        RSI_1d = manager.list()
        RSI_1wk = manager.list()
        RSI_1mo = manager.list()
        
        processes = []
        final_output_dict = {}


        current_time = datetime.now()
        # Calculate the time difference between now and the start time
        time_difference = current_time - start_time
        time_left = 120 - time_difference.total_seconds()
        print (f'\n\nIt took {time_difference} seconds to run & complete this program')
        print (f'sleeeping for {time_left} seconds.....\n\n\n\n')
        time.sleep(time_left) 