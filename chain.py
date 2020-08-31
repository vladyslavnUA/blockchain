import hashlib
import json
from textwrap import dedent
from typing import List, Any
from uuid import uuid4
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # miner reward  //  0 - new coin mined
    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1,
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'Mining a new block  ( ͡° ͜ʖ ͡°)╭∩╮  \n New block forged  \(“▔□▔)/\(“▔□▔)/  \n',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing parameters, ヽ༼ಥ_ಥ༽ﾉ \n Required: Sender, Recipient, Amount', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Processing new transaction  [̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅ )̲̅$̲̅] \n Transaction is scheduled to be added to Block No. {index}'}
    return jsonify(response), 201 


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200

class Blockchain(object):

   def __init__(self):

       self.chain = []

       self.current_transactions = []

       self.new_block(previous_hash=1, proof=100)

 

   def proof_of_work(self, last_proof):

       proof = 0

       while self.valid_proof(last_proof, proof) is False:

           proof +=1

       return proof

   @staticmethod

   def valid_proof(last_proof, proof):

       guess = f'{last_proof}{proof}'.encode()

       guess_hash = hashlib.sha256(guess).hexdigest()

       return guess_hash[:4] == "0000"

   def new_block(self, proof, previous_hash=None):

       now = datetime.now()
       block = {

           'index': len(self.chain) + 1,
            
           'timestamp': datetime.timestamp(now),

           'proof': proof,

           'previous_hash': previous_hash or self.hash(self.chain[-1]),

       }

       self.current_transactions=[]

       self.chain.append(block)

       return block

   def new_transaction(self):

       self.current_transactions.append(

           {

               'sender': sender,

               'recipient': recipient,

               'amount': amount,

           }

       )

       return self.last_block['index'] + 1

   @staticmethod

   def hash(block):
       block_string = json.dumps(block, sort_keys=True).encode()
       return hashlib.sha256(block_string).hexdigest()

   @property

   def last_block(self):
       return self.chain[-1]



node_identifier = str(uuid4()).replace('-',"")

# initialize blockchain

blockchain = Blockchain()

if __name__ == '__main__':

   app.run(host="0.0.0.0", port=5000)


# ARTICLE BY: NITISH SINGH
# ARTICLE URL: https://101blockchains.com/build-a-blockchain-in-python/