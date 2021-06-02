from collections import defaultdict
from bscscan import BscScan
from datetime import datetime 
from pythonpancakes import PancakeSwapAPI
import time
ps = PancakeSwapAPI()

API_KEY = "YOUR_KEY"
ADR = 'YOUR_ADDRESS'


mydict = {k: str(v).encode("utf-8") for k,v in ps.pairs().items()}

all_tokens = {}
for k, v in ps.tokens()['data'].items():

    all_tokens[k.lower()] = v

bsc = BscScan(API_KEY)
balance = bsc.get_bnb_balance(address=ADR)


transfers = bsc.get_bep20_token_transfer_events_by_address(address=ADR,startblock=0,endblock=9999999999999,sort="asc" )
normals = bsc.get_normal_txs_by_address(address=ADR,startblock=0,endblock=9999999999999,sort="asc" )

bnb_values = dict()
for n in normals:
    bnb_values[n['hash']] = n['value']

tokens = defaultdict(list)
for t in transfers:
    tokenName = t['tokenName']
    tokens[tokenName].append(t)

bnb_total_spend = 0
bnb_total_current = 0
print(f"{'Token':50} {'Date':30} {'Count':20} {'BNB buyin':20} {'BNB current':20} {'ROI':20}" )
print("")


for key, value in tokens.items():
    token_count = 0
    bnb_current = 0
    bnb = 0
    for v in value:
        token_count += ( float(v['value']) / ( 10 ** int(v['tokenDecimal']) ) )
        try:
            bnb += float(bnb_values[v['hash']]) / 1000000000000000000
        except:
            pass
    
    
    contract = value[0]['contractAddress']
    try:
        contract_current_values = all_tokens[contract]
        bnb_current = float(contract_current_values['price_BNB']) * token_count
        roi =  (bnb_current * 100.0 / bnb) - 100
    except:
        bnb_current = 0.0
        roi = 0.0

    dt_object = datetime.fromtimestamp(int(value[0]['timeStamp']))    
    bnb_total_spend += bnb
    bnb_total_current += bnb_current
    print(f"{key:50} {dt_object} {token_count:20.2f} {bnb:20.5f} {bnb_current:20.5} {roi:10.1f}" )

print()
print(f"BNB spend:   {bnb_total_spend}")
print(f"BNB current: {bnb_total_current}")