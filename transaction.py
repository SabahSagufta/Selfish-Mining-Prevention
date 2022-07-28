import hashlib
import json
import pickle

from config import reward

class Transaction():
    def __init__(self, ID=None, TxIn=None, TxOut=None):
        self.ID = ID
        self.Input = TxIn
        self.Output = TxOut

    def setID(self):
        encoded_data = pickle.dumps(self)
        self.ID = hashlib.sha256(encoded_data).hexdigest()

    def canUnlock(self, data):
        return (self.Input.Signature == data)

    def canBeUnlocked(self, data):
        return (self.Output.PubKey == data)

    def isCoinbase(self):
        return (((self.Input.fromAdress) == -1) & (self.Output.Value == reward))

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def executeTransaction(self): #??
        self.setID()

        print(f"---- Executing transaction ---- {self.ID}")
        if(self.isCoinbase()): print("Coinbase transaction")
        else: print(f"From adress: {self.Input.fromAdress}")
        print(f"To adress: {self.Output.toAdress}")
        print(f"Value: {self.Output.Value}")
        print("--------------------------------------------------")


class TxInput():
    def __init__(self, ID="", fromAdress="", Signature=""):
        self.ID = ID
        self.fromAdress = fromAdress
        self.Signature = Signature
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class TxOutput():
    def __init__(self, Value=None, toAdress=None):
        self.Value = Value # valor monetari
        self.toAdress = toAdress


def CoinbaseTx(toAdress, data):
    if(data == ""): data = f"Coins to {toAdress}"

    txIn = TxInput("", -1, data)
    txOut = TxOutput(reward, toAdress)
    tx = Transaction(None, txIn, txOut)

    return tx
