from flask import Flask
from flask import render_template
from flask import request
from collections import defaultdict
from bscscan import BscScan
from datetime import datetime 
from pythonpancakes import PancakeSwapAPI
import configparser
import sys




def load_transactions(ADR):

    ADR = ADR.lower()
    token_balance = dict()

    cfg = configparser.ConfigParser()
    cfg.read('config.cfg')

    API_KEY = cfg.get('CONFIG', 'api_key', raw='')
    try:
        with BscScan(API_KEY, asynchronous=False) as bsc:
            balance = bsc.get_bnb_balance(address=ADR)

        ps = PancakeSwapAPI()
        mydict = {k: str(v).encode("utf-8") for k,v in ps.pairs().items()}

        all_tokens = {}
        for k, v in ps.tokens()['data'].items():

            all_tokens[k.lower()] = v


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


        for key, value in tokens.items():
            token_count = 0
            bnb_current = 0
            bnb = 0
            for v in value:
                # If the address has sold any tokens, they have to be subtracted from the amount. The following lines should take care of that.
                # However, the amount sold should also be reflected in the bnb buy amount. This is still missing 
                #assert (v['from'] == ADR) or (v['to'] == ADR) # just to be sure
                if v['to'] == ADR:
                    token_count += (float(v['value']) / (10 ** int(v['tokenDecimal'])))
                elif v['from'] == ADR:
                    token_count -= (float(v['value']) / (10 ** int(v['tokenDecimal'])))

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

            token_balance[key] = [dt_object, token_count, bnb, bnb_current, roi ]

        return bnb_total_spend, bnb_total_current, token_balance
    except:
        return 0, 0, token_balance

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def root(): 
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        results = []
        
        address = request.form.get('address')
        fieldnames = [ 'Token', 'Date', 'Count', 'BNB buyin', 'BNB current', 'ROI [%]']
        bnb_total_spend, bnb_total_current, results = load_transactions(address)

        return render_template('home.html', address=address, bnb_spent=bnb_total_spend, bnb_value=bnb_total_current, results=results, fieldnames=fieldnames, len=len)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)