from flask import Flask
from flask import render_template
from flask import request
from collections import defaultdict
from bscscan import BscScan
from datetime import datetime 
from pythonpancakes import PancakeSwapAPI
from transactions import load_transactions



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
    app.run(host='127.0.0.1', port=8081, debug=False)