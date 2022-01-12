import hashlib
import json

from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
    # Responsible for managing the chain
    # Will store transactions and have helper methods for adding new blocks to the chain

    def __init__(self):
        # used to store our blockchain
        self.chain = []

        # used to store transactions
        self.current_transactions = []

        #create the genesis block (first block of the chain)
        self.new_block(previous_hash = 1 , proof = 100)

    def new_block(self, proof, previous_hash = None):
        # Creates a new Block and adds it too the chain
        # :param proof: <int> The proof gien by the Proof of Work algorithm
        # :param previous_hash: (Optional) <str> Hash of previous Block
        # :return: <dict> New Block

        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        # Creating transaction for the next Block
        # Adds a new transaction to the list of transcations
        # Way of adding transactions to a Block
        # Creates a new transaction to go into the next mined Block
        # :param sender: <str> Address of the Sender
        # :param recipient: <str> Address of the recipient
        # :param amount: <int> Amount
        # :return: <int> the index of theo Block that will hold this transaction

        self.current_transactions.append({
            'sender' : sender,
            'recipient' : recipient,
            'amount' : amount,
        })

        # returns the index the block which the transactions will be added to (the next one to be mined)
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a Block
        # Creates a SHA-256 hash of a Block
        # :param block: <dict> Block
        # :return: <str>

        # must ensure that the dictionary is ordered, or we'll have inconsistent hashes
        # block_string = json.dumps(block, sort_keys = True).encode()
        # return hashlib.sha256(block_string).hexdigest()

        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        # Proof of Work Algo
        # Find a number p where hash(pp') contains 4 leadin 0s
        # p is the previous proof, and p' is the new p
        # :param last_proof: <int>
        # :return: <int>

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        # Validates the Proof: Does hash(last_proof, proof) contain 4 leading 0s?
        # :param last_proof: <int> Previous Proof
        # :return: <bool> True if correct, False if not.

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# ===============================
# PART 2: Blockchain as an API
# Using flask we can talk to our blockchain ovver the web using HTTP requests
# Create three methods
#   /transactions/new -> create a new transaction to a block
#   /mine -> tell the server to mine a new block
#   /chain to return the full Blockchain

# The server will form a single node in the blockchian network

# Instantiate our Node
app = Flask(__name__)

# Create a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')  #creates a random name for our node

# Instantiate the blockchain (instantiate the blockchain class)
blockchain = Blockchain()

# create the /mine endpoint (get request)
@app.route('/mine', methods=['GET'])
def mine():
    return "We'll make a new Block"

# create the /transactions/new endpoint (post request ... sending data to it)
@app.route('/transactions/new', methods=['POST'])
def new_transactions():
    values = request.get_json()

    # Check that the required fields are in the POSTed data
    required = ['sender', 'recipient', 'amount']

    if not all (k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

# create the /chain endpoint (returns the full blockchain)
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)

    # ===========================================
    # PERSONAL NOTES
    # - Proof of Work : how new blocks are created/mined on the blockchain
    #       - We want to find a number that solves a problem
    #       - The number should be hard to find but easy to verify by anyone on the network
    #       - Example: hash of two factors must end in a 0 (fix x = 0) ... 
    #       - In BC PoW algo is known as Hashcash ... algo that miners race to solve in order to create a new block
    #         Miners are rewarded for their solution by receiving a coin - in a transaction