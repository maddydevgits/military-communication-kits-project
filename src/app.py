#for flask 
from flask import Flask,request,redirect,render_template

#blockchain
from web3 import Web3,HTTPProvider
import json


#for files
from werkzeug.utils import secure_filename
# import ipfsapi


app=Flask(__name__)


def connect_with_network(wallet):
    web3= Web3(HTTPProvider('127.0.0.1:7545'))
    print('ganache connected')
    
    with open('./build/contracts/network.json') as f:
        artificat_network= json.load(f)
        abi=artificat_network['abi']
        address=artificat_network['networks']['5777']['address']
    contract=web3.eth.contract(abi=abi,address=address)
    
    print('contract selected')
        
    if wallet==0:
        web3.eth.defaultAccount=web3.eth._get_accounts
    else:
        web3.eth.defaultAccount=wallet
    
    print('Account selected')
    
    return web3,contract
        
    

def connect_with_communication(wallet):
    web3= Web3(HTTPProvider('127.0.0.1:7545'))
    print('ganache connected')
    
    if wallet==0:
        print('wallet 0')
        web3.eth.defaultAccount=web3.eth._get_accounts
    else:
        web3.eth.defaultAccount=wallet
    
    print('Account selected')
    
    with open('./build/contracts/communication.json') as f:
        artificat_communication= json.load(f)
        abi=artificat_communication['abi']
        address=artificat_communication['networks']['5777']['address']
    contract=web3.eth.contract(abi=abi,address=address)
    
    print('contract selected')
        

    return web3,contract



@app.route('/')
def home():
    return render_template('index.html')

# Routes for network contract
@app.route('/add_commander', methods=['POST'])
def add_command():
    wallet = request.form['wallet']
    name = request.form['name']
    password = request.form['password']

    contract, web3 = connect_with_network(wallet)
    tx_hash = contract.functions.addCommanders(wallet, name, password).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)

    return redirect('/')

#login the account
@app.route('/login', methods=['POST'])
def login_creation():
    wallet = request.form['wallet']
    password = request.form['password']

    contract, web3 = connect_with_network(0)
    is_logged_in = contract.functions.login(wallet, password).call()

    if is_logged_in:
        # Fetch commander details from the blockchain
        _commanders, _commandernames = contract.functions.viewCommanders().call()

        # Check if the provided wallet address is in the list of commanders
        if wallet in _commanders:
            # Get the index of the commander in the list
            index = _commanders.index(wallet)
            
            # Check if the provided password matches the password of the commander
            if password == _commanders.passwords[index]:
                # Login successful
                return render_template('send_message.html')
            else:
                # Password does not match
                return render_template(message="Incorrect password")
        else:
            # Wallet address not found in the list of commanders
            return render_template(message="Wallet address not registered as a commander")

    

# Send messages
@app.route('/send_message', methods=['POST'])
def send_msg():
    from_address = request.form['from']
    to_address = request.form['to']
    message = request.form['message']

    contract, web3 = connect_with_communication(0)
    tx_hash = contract.functions.sendMessage(from_address, to_address, message).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)

    return redirect('/send_message')

#send files
@app.route('/send_files', methods=['POST'])
def send_file():
    wallet = request.form['wallet']
    file_hash = request.form['file_hash']
    to_addresses = request.form.getlist('to')

    contract, web3 = connect_with_communication(wallet)
    tx_hash = contract.functions.sendFiles(wallet, file_hash, to_addresses).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)

    return redirect('/send_files')

#view messges
def view_msg():
    contract, web3 = connect_with_communication(0)
    _messages,from_message,to_message = contract.functions.viewMessages().call()

    return render_template('view_messages.html', _messages=_messages, from_message=from_message, to_message=to_message)

#view files
@app.route('/view_files')
def view_file():
    contract, web3 = connect_with_communication(0)
    from_file,_filehash,_owners = contract.functions.viewFiles().call()

    return render_template('view_files.html', from_file=from_file,_filehash=_filehash,_owners=_owners)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)