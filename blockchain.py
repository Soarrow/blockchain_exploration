import hashlib
import json
from time import time

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
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain(-1))
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
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
        # Hases a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass