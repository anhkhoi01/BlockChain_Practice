from hashlib import sha256

def update_hash(*args):
    hash_text = ""
    h = sha256()
    for arg in args:
        arg = str(arg)
        hash_text += arg

    h.update(hash_text.encode('utf-8'))

    return h.hexdigest()

def test():
    database = ["hello", "hi", "how are you", "have a good day"]
    blockChain = BlockChain()

    for data in database:
        blockChain.mine(Block(index=len(blockChain.chain),data=data))

    for block in blockChain.chain:
        print(block)

class Block:
    number = 0
    data = None
    nonce = 0
    hash = None
    previous_hash = "0" * 64

    def __init__(self,index=0,previous="0"*64, data=None, nonce=0, hashin="0"*64):
        self.data=data
        self.number=index
        self.previous_hash = previous
        self.nonce = nonce
        self.hash = hashin

    def __hash__(self):
        result = update_hash(self.number,self.data,self.nonce,self.previous_hash)
        self.hash = result
        return result

    def __str__(self):
        return str("Block#: %s\nData: %s\nNonce: %s\nPrevious hash: %s\nHash: %s"
                   %(self.number,self.data,self.nonce,self.previous_hash,self.hash))

class BlockChain:
    difficulty = 4
    chain = []

    def __init__(self, chain=None):
        if chain is None:
            chain = []
        self.chain = chain

    def add(self,block):
        # self.chain.append({
        #     'index':block.index,
        #     'data':block.data,
        #     'previous':block.previous_hash,
        #     'nonce':block.nonce,
        #     'hash':block.hash})

        self.chain.append(block)

    def remove(self,block):
        self.chain.remove(block)

    def isValid(self):
        if len(self.chain) < 2:
            return True

        for i in range(1,len(self.chain)):
            preHash = self.chain[i].previous_hash
            preBlockHash = self.chain[i-1].hash
            if preHash != preBlockHash:
                return False

        return True
    def mine(self,block):
        try:
            block.previous_hash = self.chain[-1].hash
        except IndexError:
            pass

        while True:
            if block.__hash__()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

