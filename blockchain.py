import hashlib
import pickledb
import time


from transaction import *
from wallet import *
from config import difficulty, max_nonce

file = open("startime.txt", "r")
value = file.read()
startTime = float(value)
file.close()

secret_block = []
Max_Time = 600.00

class Block():
    def __init__(self):
        self.Hash: str
        self.Data: str
        self.PrevHash: str
        self.Nonce: int
        self.Transactions = []
        self.Time: float


class BlockChain():
    def __init__(self):
        self.blocks = []
        self.lastHash = None
        self.database = "blockchain.db"

    def __len__(self):
        return len(self.blocks)

    # New Block with PoW and validation
    def createBlock(self, txs: list, PrevHash: str):
        newBlock = Block()

        ## !!!! chapuza maxima
        for tx in txs:
            if (type(tx) != str): tx.executeTransaction()
        ## !!!!

        # Chapuza per convertir cada transacció a JSON
        for tx in txs:
            if ((type(tx) != str) & (type(tx) != list)):
                newBlock.Transactions.append(tx.toJson())
            else:
                newBlock.Transactions.append(tx)

        newBlock.PrevHash = PrevHash

        PoW = NewProofOfWork(newBlock)
        newBlock.Hash, newBlock.Nonce = PoW.run()

        # Validation
        if (PoW.validate(newBlock.Nonce)):
            return (newBlock)
        else:
            print("error")

    # Add a new block for a set of transactions to the blockchain
    def addBlock(self, txs: list):

        prevBlock = self.blocks[len(self) - 1]
        newBlock = self.createBlock(txs, prevBlock.Hash)


        if (input("broadcast the generated block? (yes / no) ") == "yes"):
            end_T1 = time.time()
            print("Time T1=", end_T1 - InitBlockChain.start_T1)

            if ((end_T1 - InitBlockChain.start_T1) < Max_Time):
                # pendent de canviz
                end_time = time.time()
                newBlock.Time = end_time - startTime
                print("block generation time:", newBlock.Time)

                self.blocks.append(newBlock)  # append directe?

                # update database
                self.lastHash = newBlock.Hash
                self.database.set("lh", newBlock.Hash)
                self.database.set(newBlock.Hash, serializeBlock(newBlock))
                self.database.dump()
            else:
                self.secret_block = secret_block.append(newBlock)
                # return secret_block

        else:
            dummyBlock = self.createBlock([], prevBlock.Hash)
            self.blocks.append(dummyBlock)

    def adding_selfish_block(self):
        SB = secret_block[0]
        CB = self.blocks[-1]
        if (SB.addBlock.prevBlock == CB.addBlock.prevBlock):
            self.blocks.append(secret_block)

        else:
            print("The selfish block is rejected")


    def Genesis(self, coinbaseTx: Transaction):
        return self.createBlock([coinbaseTx], "")

    def uploadFromDatabase(numBlocks: int):
        pass

    def findUTXO(self):
        return self.database.get(self.lastHash)


# Serialization tools for database saving
def serializeBlock(block: Block):
    return {"Hash": block.Hash,
            "PrevHash": block.PrevHash,
            "Nonce": block.Nonce,
            "Transactions": block.Transactions,
            "Time": block.Time
            }


def deserializeBlock(serialized: dict):
    newBlock = Block()
    newBlock.Hash = serialized["Hash"]
    newBlock.PrevHash = serialized["PrevHash"]
    newBlock.Nonce = serialized["Nonce"]
    newBlock.Transactions = serialized["Transactions"]
    newBlock.Time = serialized["Time"]

    return newBlock


def InitBlockChain(adress: str):
    newBlockChain = BlockChain()

    # connect database
    newBlockChain.database = pickledb.load("blockchain.db", False)

    # Retrieve last block from database or create genesis block
    lastHash = newBlockChain.database.get("lh")
    if (lastHash != False):
        firstBlock = deserializeBlock(newBlockChain.database.get(lastHash))
        newBlockChain.blocks.append(newBlockChain.createBlock(firstBlock.Transactions, firstBlock.PrevHash))
        printBlock(firstBlock)
    else:
        newBlockChain.blocks.append(newBlockChain.Genesis(CoinbaseTx(adress, "")))

    InitBlockChain.start_T1 = time.time()

    return newBlockChain


def printBlock(block: Block):
    print(f"First Block PrevHash: {block.PrevHash}")
    # print(f"First Block Data: {block.Transactions}")
    print(f"First Block Hash: {block.Hash}")


################################################################################
################################################################################


class ProofOfWork():
    def __init__(self, block, verbose=False):
        self.Block = block
        self.Target = 2 ** (256 - difficulty)
        self.verbose = verbose

    # Unify hashable data
    def createHeader(self, nonce: int):
        data = (str(self.Block.PrevHash) + str(self.Block.Transactions) + str(nonce)).encode('utf-8')
        return data

    def run(self):
        for nonce in range(max_nonce):
            data = self.createHeader(nonce)
            hash_result = hashlib.sha256(data).hexdigest()

            if int(hash_result, base=16) < self.Target:
                if (self.verbose):
                    print("Success with nonce ", nonce)
                    print("Hash is ", hash_result)
                return (hash_result, nonce)

        if (self.verbose): print(f"Failed after {nonce}(max_nonce) tries")  # ?
        return nonce

    def validate(self, nonce):
        data = self.createHeader(nonce)
        hash_result = hashlib.sha256(data).hexdigest()

        if (int(hash_result, base=16) < self.Target): return True
        return False


# cal?
def NewProofOfWork(block: Block):
    return ProofOfWork(block)
