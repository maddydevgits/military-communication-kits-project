#for flask 
from flask import Flask,request,redirect,render_template,session
import ipfsapi

#blockchain
from web3 import Web3,HTTPProvider
import json

#for files
from werkzeug.utils import secure_filename
# import ipfsapi

#Quantum
from QuantumCryptoToken import *

app=Flask(__name__)
app.secret_key='1234'


def connect_with_network(wallet):
    web3= Web3(HTTPProvider('http://127.0.0.1:7545'))
    print('ganache connected')
    
    with open('../build/contracts/network.json') as f:
        artificat_network= json.load(f)
        abi=artificat_network['abi']
        address=artificat_network['networks']['5777']['address']
    contract=web3.eth.contract(abi=abi,address=address)
    
    print('contract selected')
        
    if wallet==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=wallet
    
    print('Account selected')
    
    return contract,web3
        
    

def connect_with_communication(wallet):
    web3= Web3(HTTPProvider('http://127.0.0.1:7545'))
    print('ganache connected')
    
    if wallet==0:
        print('wallet 0')
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=wallet
    
    print('Account selected')
    
    with open('../build/contracts/communication.json') as f:
        artificat_communication= json.load(f)
        abi=artificat_communication['abi']
        address=artificat_communication['networks']['5777']['address']
    contract=web3.eth.contract(abi=abi,address=address)
    
    print('contract selected')
    return contract,web3

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signupForm',methods=['post'])
def signupForm():
    walletAddress=request.form['walletAddress']
    commanderName=request.form['commanderName']
    password=int(request.form['password'])
    token=generateToken(10)
    print(walletAddress,commanderName,password,token)
    contract,web3=connect_with_network(0)
    tx_hash=contract.functions.addCommanders(walletAddress,commanderName,password,token).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('signup.html',res='Commander Added')

@app.route('/commanderLoginForm',methods=['post'])
def commanderLoginForm():
    walletAddress=request.form['walletAddress']
    password=request.form['password']
    print(walletAddress,password)
    contract,web3=connect_with_network(0)
    status=contract.functions.login(walletAddress,int(password)).call()
    if(status==True):
        session['username']=walletAddress
        return redirect('/dashboard')
    else:
        return render_template('index.html',err='Login Invalid')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/')

@app.route('/sendFile')
def sendFile():
    return render_template('send_files.html')

@app.route('/viewMessages')
def viewMessages():
    return render_template('authenticatemsg.html')

@app.route('/sendMessageForm',methods=['post'])
def sendMessageForm():
    fromAddress=session['username']
    toAddress=request.form['toAddress']
    message=request.form['message']
    print(fromAddress,toAddress,message)
    contract,web3=connect_with_communication(0)
    tx_hash=contract.functions.sendMessage(fromAddress,toAddress,message).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('dashboard.html',res='message sent')


#send files
@app.route('/sendFileForm', methods=['POST'])
def send_file():
    walletAddress = session['username']
    file_hash = request.form['fileHash']
    to_addresses = request.form['toAddress']

    contract, web3 = connect_with_communication(0)
    tx_hash = contract.functions.sendFiles(walletAddress, file_hash, to_addresses).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('send_files.html',res='Files sent')

@app.route('/viewFiles')
def viewFilesBeforeAuthenticate():
    return render_template('authenticate.html')

@app.route('/authenticateForm',methods=['post'])
def authenticateForm():
    authToken=request.form['authToken']
    walletAddress=session['username']
    print(authToken,walletAddress)
    contract,web3=connect_with_network(0)
    status=contract.functions.verifyToken(walletAddress,authToken).call()
    if status==True:
        return redirect('/viewFilesAfterAuthenticate')
    else:
        return redirect('/viewFiles')

@app.route('/authenticateMsgForm',methods=['post'])
def authenticateMsgForm():
    authToken=request.form['authToken']
    walletAddress=session['username']
    print(authToken,walletAddress)
    contract,web3=connect_with_network(0)
    status=contract.functions.verifyToken(walletAddress,authToken).call()
    if status==True:
        return redirect('/viewMsgAfterAuthenticate')
    else:
        return redirect('/viewMessages')

@app.route('/viewMsgAfterAuthenticate')
def viewMsgs():
    data=[]
    contract,web3=connect_with_communication(0)
    _messages,from_message,to_message=contract.functions.viewMessages().call()
    print(_messages,from_message,to_message)
    contract,web3=connect_with_network(0)
    _commanders,_commandernames,_commanderpasswords,_quantumtokens=contract.functions.viewCommanders().call()

    for i in range(len(_messages)):
        if session['username']==to_message[i]:
            dummy=[]
            dummy.append(from_message[i])
            fromIndex=_commanders.index(from_message[i])
            dummy.append(_commandernames[fromIndex])
            dummy.append(_messages[i])
            data.append(dummy)
            
    return render_template('view_messages.html',l=len(data),dashboard_data=data)

@app.route('/viewFilesAfterAuthenticate')
def viewFiles():
    data=[]
    contract,web3=connect_with_communication(0)
    from_file,_filehash,_owners=contract.functions.viewFiles().call()
    print(from_file,_filehash,_owners)
    contract,web3=connect_with_network(0)
    _commanders,_commandernames,_commanderpasswords,_quantumtokens=contract.functions.viewCommanders().call()

    for i in range(len(_filehash)):
        if session['username']==_owners[i][0]:
            dummy=[]
            dummy.append(from_file[i])
            fromIndex=_commanders.index(from_file[i])
            dummy.append(_commandernames[fromIndex])
            dummy.append(_filehash[i])
            data.append(dummy)
            
    return render_template('view_files.html',l=len(data),dashboard_data=data)

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