import hashlib

import base58 #encoding scheme

import ecdsa

from config import checksum_length, version


class Wallet():
    def __init__(self):
        self.PrivateKey = ""
        self.PublicKey = ""

    def getAdress(self):
        publicKeyHash = PublicKeyHash(self.PublicKey)

        versionedHash = publicKeyHash
        versionedHash.extend(version) #list

        checksum = CheckSum(versionedHash)

        finalHash = versionedHash
        finalHash.extend(checksum)

        adress = base58.b58encode(finalHash).decode("utf-8")

        return adress

class Wallets():
    def __init__(self):
        self.wallets = {}
        self.balances = {}
    def addWallet(self, w: Wallet):
        adress = w.getAdress()
        self.wallets[adress] = w
        self.balances[adress] = 0
    def getBalance(self, adress):
        return self.balances[adress]
    def setBalance(self, adress, balance):
        self.balances[adress] = balance


def NewKeyPair():
    # SECP256k1 is the Bitcoin elliptic curve
    privateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    publicKey = privateKey.get_verifying_key()
    return privateKey.to_string(), publicKey.to_string()

def PublicKeyHash(publicKey):
    hashedPublicKey = hashlib.new('sha256', publicKey).digest()
    publicRipeMd = hashlib.new('ripemd160', hashedPublicKey).digest()
    return bytearray(publicRipeMd)

def CheckSum(versionedHash):
    firstHash = hashlib.new('sha256', versionedHash).digest()
    secondHash = hashlib.new('sha256', firstHash).digest()
    return secondHash[:checksum_length]

def InitWallet(ws: Wallets):
    w = Wallet()
    w.PrivateKey, w.PublicKey =  NewKeyPair()

    ws.addWallet(w)
    return w

ws = Wallets()
