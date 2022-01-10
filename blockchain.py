class Blockchain(object):
    def __init__(self):
        # used to store our blockchain
        self.contain = []

        # used to store transactions
        self.current_transactions = []

    def new_block(self):
        # Creates a new Block and adds it too the chain
        pass
    
    def new_transaction(self):
        # Adds a new transaction to the list of transcations
        pass

    @staticmethod
    def hash(block):
        # Hases a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass