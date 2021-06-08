from collections import defaultdict
from bscscan import BscScan
from datetime import datetime 
from pythonpancakes import PancakeSwapAPI
import configparser
from tokens import load

def load_transactions(ADR):

    ADR = ADR.lower()

    token_balance = dict()

    cfg = configparser.ConfigParser()
    cfg.read('config.cfg')

    API_KEY = cfg.get('CONFIG', 'api_key', raw='')
    try:
        with BscScan(API_KEY, asynchronous=False) as bsc:
            balance = bsc.get_bnb_balance(address=ADR)
            bep20_transfers = bsc.get_bep20_token_transfer_events_by_address(address=ADR,startblock=0,endblock=9999999999999,sort="asc" )
            normal_transfers = bsc.get_normal_txs_by_address(address=ADR,startblock=0,endblock=9999999999999,sort="asc" )
            bnb_values = dict()
            for n in normal_transfers:
                bnb_values[n['hash']] = n['value']

            tokens = defaultdict(list)
            for t in bep20_transfers:
                tokens[t['contractAddress']].append(t)

            # lookup dict for live prices
            tokens_live_values = dict()
            contracts = ["0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"]   # add
            for key in list(tokens): 
                contracts.append( key )
            tokens_live_list = load(contracts)

            for t in tokens_live_list:
                if t != None:
                    tokens_live_values[t['id'][:-4]] = t['priceUSD'] # remove -bsc suffix
            
            # get current WBNB Token price                    
            bnb_live = tokens_live_values['0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c']#['priceUSD']
            bnb_total_spend = 0
            bnb_total_current = 0.0

            for key, value in tokens.items():
                token_count = 0
                bnb_current = 0
                bnb = 0
                for v in value:
                    try:
                        trans_value = float(bnb_values[v['hash']]) / 1000000000000000000
                    except:
                        trans_value = 0

                    if v['to'] == ADR:
                        bnb += trans_value
                        token_count += (float(v['value']) / (10 ** int(v['tokenDecimal'])))
                    elif v['from'] == ADR:
                        bnb -= trans_value
                        token_count -= (float(v['value']) / (10 ** int(v['tokenDecimal'])))
                
                try:
                    bnb_current = float(tokens_live_values[key]) / bnb_live  * token_count
                    roi =  (bnb_current * 100.0 / bnb) - 100
                except:
                    bnb_current = 0.0
                    roi = 0.0

                dt_object = datetime.fromtimestamp(int(value[0]['timeStamp']))    
                bnb_total_spend += bnb
                bnb_total_current += bnb_current

                token_balance[key] = [v['tokenName'], dt_object, token_count, bnb, bnb_current, roi ]

            return bnb_total_spend, bnb_total_current, token_balance
    except:
        return 0, 0, token_balance



if __name__ == '__main__':
    bnb_total_spend, bnb_total_current, token_balance = load_transactions('0x123456')
    
    for key, t in token_balance.items():
        print(f"{t[0]:50} {t[1]} {t[2]:20.2f} {t[3]:20.5f} {t[4]:20.5} {t[5]:10.1f}" )

    print()
    print(f"BNB spend:   {bnb_total_spend}")
    print(f"BNB current: {bnb_total_current}")