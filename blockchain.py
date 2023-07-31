from hashlib import sha256

def update_hash(*args):
    hash_text = ""
    h = sha256()
    for arg in args:
        arg = str(arg)
        hash_text += arg

    h.update(hash_text.encode('utf-8'))

    return h.hexdigest()

class Block:
    index = 0
    data = None
    nonce = 0
    hash = None
    previous_hash = "0" * 64

    def __init__(self,data,index=0):
        self.data=data
        self.index=index

    def __hash__(self):
        result = update_hash(self.index,self.data,self.nonce,self.previous_hash)
        self.hash = result
        return result

    def __str__(self):
        return str("Block#: %s\nData: %s\nNonce: %s\nPrevious hash: %s\nHash: %s"
                   %(self.index,self.data,self.nonce,self.previous_hash,self.hash))

class BlockChain:
    difficulty = 4
    chain = []

    def __init__(self, chain=None):
        if chain is None:
            chain = []
        self.chain = chain

    def add(self,block):
        self.chain.append({
            'index':block.index,
            'data':block.data,
            'previous':block.previous_hash,
            'nonce':block.nonce,
            'hash':block.hash})

    def mine(self,block):
        try:
            block.previous_hash = self.chain[-1].get('hash')
        except IndexError:
            pass

        while True:
            if block.__hash__()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

