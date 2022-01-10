class Blockchain(object):
    # Responsible for managing the chain
    # Will store transactions and have helper methods for adding new blocks to the chain

    def __init__(self):
        # used to store our blockchain
        self.chain = []

        # used to store transactions
        self.current_transactions = []

    def new_block(self):
        # Creates a new Block and adds it too the chain
        pass
    
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