#python "d:/Trading/Python/Code/Trading system v5.py"

'''
Trading system v5 - 
-- created THE_MAIN() & OUTPUT_PRINTER() functions
-- created price breakout detector & volume breakout tracker
'''


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
except Exception as e:
    print ('\n\n\n\n\n\n',repr(e))
    print ('There is NO INTERNET CONNECTION dude...!!\n\n\n\n\n\n')
    sys.exit(1)



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



# RUN THIS CODE FROM THE START OF THE MARKET AT - 9:16:30 am
target_start_hour, target_start_minute, target_start_second = 23, 59, 45  # CHANGE THIS TO 9:16:30 AM
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
        rsi = round(rsi,1)
    else:
        rsi = 100
    event.set() #3
    return rsi




def THREE_CANDLE_PRICE_BREAKOUT(yf_all_stocks_data,bull_BO,bear_BO,i,lock,event):
    BO_status = '0'
    percentage = 0
    yf_cp_list = yf_all_stocks_data[(eqList[i], 'Close')].tolist()       # A stock's CP data
    yf_op_list = yf_all_stocks_data[(eqList[i], 'Open')].tolist()
    zero_candle_cp = yf_cp_list[2] 
    last_candle_cp = yf_cp_list[1] 
    second_last_candle_cp = yf_cp_list[0] 
    
    zero_candle_op = yf_op_list[2]
    last_candle_op = yf_op_list[1]
    second_last_candle_op = yf_op_list[0]
    
    '''    BULLISH BREAKOUT     '''
    if zero_candle_cp > last_candle_cp > second_last_candle_cp:                  # this condition checks for a bullish breakout
        with lock:
            bull_BO.append(eqList[i].replace(".NS", ""))
        
        if second_last_candle_op < last_candle_op:                                        # this IF statement checks if the last_candle_op is more than the second_last_candle mid point
            if last_candle_op < zero_candle_op:                                 # this IF statement checks if the zero_candle_op is more than the last_candle mid point
                percentage = 100 - ((second_last_candle_op/zero_candle_cp)*100)
                BO_status = '+'

    '''    BEARISH BREAKOUT     '''
    if zero_candle_cp < last_candle_cp < second_last_candle_cp:           # this condition checks for a bearish breakout
        with lock:
            bear_BO.append(eqList[i].replace(".NS", ""))
            
        if second_last_candle_op > last_candle_op:                                        # this IF statement checks if the last_candle_op is less than the second_last_candle mid point
            if last_candle_op > zero_candle_op:                                 # this IF statement checks if the zero_candle_op is less than the last_candle mid point
                percentage = 100 - ((zero_candle_cp/second_last_candle_op)*100)
                BO_status = 'BEARISH'
    event.set()    #5
    return BO_status,percentage


def THREE_CANDLE_VOLUME_BREAKOUT(yfd_dict,i,event,vol_cal,BO_status):
    yf_all_stocks_data = yfd_dict['5m']
    yf_data = yf_all_stocks_data[(eqList[i])]
    
    '''
    This below block of code will find the total volume of this particular stock
    '''
    
    if vol_cal == 'before': 
        todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]  
        ttv = sum(todays_data['Volume'])
        
    if vol_cal == 'after': 
        ttv = sum(yf_data['Volume'])
    
    ttv = f'{ttv:,}'
    
    
    yf_all_stocks_data = yfd_dict['5m'].iloc[-4:]
    yf_vol_list = yf_all_stocks_data[(eqList[i], 'Volume')].tolist()
    a = 3
    b = ['fvd','svd','tvd']
    volume_change = {}
    
    '''
    This below block of code will find the DIFFERENCE IN VOLUME only when
    the last 3 CLOSING PRICES of that same stock is in a BULLISH or BEARISH trend
    '''
    
    if BO_status in ('+', 'BEARISH'):
        for v in range(0,3):
            curr_vol = yf_vol_list[a]
            prev_vol = yf_vol_list[a-1] 
            if curr_vol == 0:
                curr_vol = 1
            perc = ((curr_vol-prev_vol)/curr_vol)*100
            volume_change.update({b[v]:round(perc,1)})
            a-=1
    else:
        for v in range(0,3):
            volume_change.update({b[v]:0})
    
    event.set()    #7
    return volume_change,ttv


def APPENDER(start, end, yfd_dict, vol_cal,RSI_2m, RSI_5m, Stock,
    total_traded_volume, pChange, lock, breakout, bopp, bull_BO, bear_BO,last_three_volume):
    for i in range(start, end): 
        yf_all_stocks_data = yfd_dict['2m']
        yf_data = yf_all_stocks_data[(eqList[i])]        # A stock's data
            
        try:
            jg_data = n.stock_quote(eqList[i].replace(".NS", ""))
        except Exception as e:
            print ('\n\n\n\n\n\n',repr(e))
            print ('\n\n\n\n\n\nERROR = Couldnt reach the NSE server for the STOCK QUOTE, so try again sometime later..!!\n\n\n\n\n\n')
        
        '''    RSI COLUMN   '''
        for key,value in yfd_dict.items():
            #v = list(value.columns.levels)
            yf_all_stocks_data = value
            yf_data = yf_all_stocks_data.iloc[-14:]
            yf_cp_list = yf_data[(eqList[i], 'Close')].tolist()
            rsi = RSI_14_CALCULATOR(yf_cp_list,event)
            event.wait()    #3
            with lock:
                if key == '2m':
                    RSI_2m.append(rsi)
                if key == '5m':
                    RSI_5m.append(rsi)
        
        '''    PRICE BREAKOUT COLUMN    '''
        yf_all_stocks_data = yfd_dict['5m'].iloc[-3:]
        BO_status,percentage = THREE_CANDLE_PRICE_BREAKOUT(yf_all_stocks_data,bull_BO,bear_BO,i,lock,event)
        event.wait()    #5
        
        '''    VOLUME COLUMN    '''
        volume_change,ttv = THREE_CANDLE_VOLUME_BREAKOUT(yfd_dict,i,event,vol_cal,BO_status)
        event.set()    #7
        v = f'{volume_change['tvd']}% -> {volume_change['svd']}% -> {volume_change['fvd']}%'
        percentage = f'{round(percentage,1)} %'
        with lock:
            Stock.append(jg_data['info']['symbol'])
            pChange.append(round(jg_data['priceInfo']['pChange'],1))
            breakout.append(BO_status)
            bopp.append(percentage)
            total_traded_volume.append(ttv)
            last_three_volume.append(v)


def DATA_FETCHER(per,inte):
    yf_all_stocks_data = yf.download(eqList, group_by='Ticker', period=per, interval=inte)
    event.set() #1
    return yf_all_stocks_data


def SCHEDULE_TASK(y,yfd_dict,lock,vol_cal):
    if vol_cal == 'before': 
        period_interval = {
            1 : ["2d",'2m'],
            2 : ["2d",'5m'],
        }
    if vol_cal == 'after': 
        period_interval = {
            1 : ["1d",'2m'],
            2 : ["1d",'5m'],
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


def COMMON_STOCKS(sorted_FO_BO_df,sorted_FO_RSI_df):
    sorted_BO_eqList = sorted_FO_BO_df['Stock'].tolist()
    sorted_RSI_eqList = sorted_FO_RSI_df['Stock'].tolist()
    commn_eq = []
    for eq in sorted_BO_eqList:
        for st in sorted_RSI_eqList:
            if eq == st:
                commn_eq.append(eq)
    
    
    
    if len(commn_eq) != 0:
        print ('THESE ARE THE STOCKS WHICH ARE COMMON IN BOTH THE TABLES = \n',commn_eq) 
    else:
        print ('NO STOCKS COMMON IN BOTH THE TABLES')



def OUTPUT_PRINTER(j,pp,pm,current_time,advances,declines,unchanged,sorted_final_output_rsi_dataframe,sorted_final_output_breakout_dataframe):
    
    if j > 0:
        print ('\nIteration number - ',j)

    print ('CURRENT TIME = ',current_time.strftime("%H:%M:%S"))
    
    print ('pp = ',pp)
    print ('pm = ',pm)
    print (pp+pm,'stocks are PROMISING STOCKS')
    
    print(f"\nNIFTY 200 current status -\nAdvances :- {advances}\nDeclines :- {declines}\nUnchanged :- {unchanged}\n")
    print (f'In total there were {len(bull_BO)} BULLISH BREAKOUT STOCKS \n& \n{len(bear_BO)} BEARISH BREAKOUT STOCKS\n')
    
    if advances >= declines:
        print ("\n\nThe TOP 10 RSI STOCKS are :-\n")
        print (sorted_final_output_rsi_dataframe.iloc[:10])
    else:
        print ("\nThe BOTTOM 10 RSI STOCKS are :-\n")
        print (sorted_final_output_rsi_dataframe.iloc[:10])
    
    print ('\n\n')
    print ("The BREAKOUT STOCKS are :-\n")
    print (sorted_final_output_breakout_dataframe.iloc[:20])
    print ('\n')
    
    COMMON_STOCKS(sorted_final_output_breakout_dataframe.iloc[:10],sorted_final_output_rsi_dataframe.iloc[:10])
    



def THE_MAIN(Stock,pChange,total_traded_volume,last_three_volume,RSI_2m,RSI_5m,breakout,bopp,bull_BO,bear_BO,yfd_dict,lock,processes,final_rsi_output_dict,final_output_breakout_dict):
    j = 0
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
        
        
        for i in range(0,2):
            y+=1
            data_fetching_process = multiprocessing.Process(
                target=SCHEDULE_TASK, 
                args=(y,yfd_dict,lock,vol_cal))
            processes.append(data_fetching_process)
            data_fetching_process.start()
        for process in processes:
            process.join()

        i=0
        num_processor_cores = multiprocessing.cpu_count()
        chunk_size = len(eqList) // num_processor_cores
        
        for i in range(num_processor_cores):
            start = i * chunk_size
            end = start + chunk_size if i < num_processor_cores - 1 else len(eqList)
            
            data_fetching_process = multiprocessing.Process(
                target=APPENDER, 
                args=(start,end,yfd_dict,vol_cal,RSI_2m, RSI_5m, Stock,
                total_traded_volume, pChange, lock, breakout, bopp, bull_BO, bear_BO,last_three_volume))
            processes.append(data_fetching_process)
            data_fetching_process.start()

        for process in processes:
            process.join()

        try:
            nifty200 = n.live_index("NIFTY 200")
        except Exception as e:
            print ('\n\n\n\n\n\n',repr(e))
            print ('\n\n\n\n\n\nERROR = Couldnt reach the NSE server for the LIVE INDEX data, so try again sometime later\n\n\n\n\n\n')
        
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
        
        
        '''    RSI     '''
        final_rsi_output_dict.update({'pChange': list(pChange)})
        #final_rsi_output_dict.update({'RSI(14) 2m': list(RSI_2m)})
        final_rsi_output_dict.update({'RSI(14) 5m': list(RSI_5m)})
        final_rsi_output_dict.update({'Stock': list(Stock)})
        final_rsi_output_dict.update({'BO price %': list(bopp)})
        final_rsi_output_dict.update({'Last 3 Vol chg': list(last_three_volume)})
        final_rsi_output_dict.update({'Total Volume': list(total_traded_volume)})
        
        
        try:
            final_output_rsi_dataframe = pd.DataFrame(final_rsi_output_dict)
        except Exception as e:
            print ('\n\n\n\n\n\n',repr(e))
            print ('\n\n\n\n\n\nValueError: All arrays must be of the same length..!!\n\n\n\n\n\n')    
        
        if advances >= declines:
            '''TOP 10 RSI STOCKS'''    
            sorted_final_output_rsi_dataframe = final_output_rsi_dataframe.sort_values(by='RSI(14) 5m', ascending=False)
        else:
            '''BOTTOM 10 RSI STOCKS'''
            sorted_final_output_rsi_dataframe = final_output_rsi_dataframe.sort_values(by='RSI(14) 5m', ascending=True)
        
        sorted_final_output_rsi_dataframe = sorted_final_output_rsi_dataframe.reset_index(drop=True)
        sorted_final_output_rsi_dataframe = sorted_final_output_rsi_dataframe.set_index('pChange')
        
        
        '''    BREAKOUT    '''
        final_output_breakout_dict.update({'pChange': list(pChange)})
        final_output_breakout_dict.update({'RSI(14) 5m': list(RSI_5m)})
        final_output_breakout_dict.update({'Stock': list(Stock)})
        final_output_breakout_dict.update({'BO price %': list(bopp)})
        final_output_breakout_dict.update({'BO trend': list(breakout)})
        final_output_breakout_dict.update({'Last 3 Vol chg': list(last_three_volume)})
        final_output_breakout_dict.update({'Total Volume': list(total_traded_volume)})
        
        try:
            final_output_breakout_dataframe = pd.DataFrame(final_output_breakout_dict)
        except Exception as e:
            print ('\n\n\n\n\n\n',repr(e))
            print ('\n\n\n\n\n\nValueError: All arrays must be of the same length..!!\n\n\n\n\n\n')
        
        
        c = final_output_breakout_dataframe[(final_output_breakout_dataframe["BO trend"] == '+') | (final_output_breakout_dataframe["BO trend"] == 'BEARISH')]
        sorted_final_output_breakout_dataframe = c.sort_values(by='BO price %', ascending=False)
        
        
        sorted_final_output_breakout_dataframe = sorted_final_output_breakout_dataframe.reset_index(drop=True)
        sorted_final_output_breakout_dataframe = sorted_final_output_breakout_dataframe.set_index('pChange')
        


        

        '''    PRINTING THE FINAL OUTPUT    '''
        j += 1
        OUTPUT_PRINTER(j,pp,pm,current_time,advances,declines,unchanged,
            sorted_final_output_rsi_dataframe,sorted_final_output_breakout_dataframe)
        
        Stock = manager.list()
        pChange = manager.list()
        total_traded_volume = manager.list()
        last_three_volume = manager.list()
        RSI_2m = manager.list()
        RSI_5m = manager.list()
        
        breakout = manager.list()
        bopp = manager.list()
        bull_BO = manager.list()
        bear_BO = manager.list()
        yfd_dict = manager.dict()
        
        processes = []
        final_rsi_output_dict = {}
        final_output_breakout_dict = {}

        current_time = datetime.now()
        # Calculate the time difference between now and the start time
        
        time_difference = current_time - start_time
        time_difference = time_difference.total_seconds()
        
        if 120 > time_difference:
            time_left = 120 - time_difference
            print (f'\nIt took {time_difference} seconds to run & complete this program\n')
        else:
            time_left = 5
            print (f'\nIt took {time_difference} seconds to run & complete this program\nAs it has crossed 2 minutes, so rerunning this program just after the next {time_left} seconds............\n')
        
        time.sleep(time_left)
        #sys.exit(1)



if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    print ('\n\nthe code has started to run.......')
    
    if target_start_time < datetime.now():
        print (f"Adangomma, the specified time {target_start_time} has already passed daa....!!")
        print ("exiting the program !!")
        sys.exit(1)

    Stock = manager.list()
    pChange = manager.list()
    total_traded_volume = manager.list()
    last_three_volume = manager.list()
    RSI_2m = manager.list()
    RSI_5m = manager.list()
    
    breakout = manager.list()
    bopp = manager.list()
    bull_BO = manager.list()
    bear_BO = manager.list()
    yfd_dict = manager.dict()
    
    
    lock = manager.Lock()
    
    processes = []
    final_rsi_output_dict = {}
    final_output_breakout_dict = {}

    THE_MAIN(Stock,pChange,total_traded_volume,last_three_volume,
        RSI_2m,RSI_5m,breakout,bopp,bull_BO,bear_BO,yfd_dict,lock,
        processes,final_rsi_output_dict,final_output_breakout_dict)