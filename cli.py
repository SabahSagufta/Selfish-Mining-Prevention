from blockchain import *
from transaction import *
from wallet import *
import time


def cli_help():
    print("Orders:")
    print("-- transaction   - Send a transaction to another wallet")
    print("-- add   - Add a block with the previous transactions to the blockchain")
    print("-- wallet   - Create a new wallet")
    print("-- quit   - Close script")
    print("--------------------------------------------------")


def cli_wallet(ws: Wallets, wallet_alias: dict):
    alias = input("User alias: ")

    # Initiate user wallet and add to network
    newWallet = InitWallet(ws)
    wallet_alias[alias] = newWallet.getAdress()
    ws.addWallet(newWallet)

    # Save private key locally
    f = open(f"{alias}_pk.txt", "w+")
    f.write(newWallet.PrivateKey.hex())
    f.close()

    print(f"Your adress is: {newWallet.getAdress()}")
    print(f"Private Key stored in {alias}_pk.txt")

    return newWallet.getAdress()


def cli_transaction(ws: Wallets, wallet_alias: dict, Transaction_list: list):
    fromAlias = input("User alias: ")

    # Check if wallet exists
    try:
        fromAdress = wallet_alias[fromAlias]
    except:
        print("Alias not found")
        if (input("create new wallet? (yes / no) ") == "yes"):
            cli_wallet(ws, wallet_alias)
        return 0

    toAdress = input("Destiny adress: ")

    # Check if private key is correct
    try:
        fileKeys = input("Key file path: ")
        f = open(fileKeys, "r")
        input_pk = f.read()
    except:
        print("file not found")
        return 0

    # Store transaction
    if (ws.wallets[fromAdress].PrivateKey.hex() == input_pk):
        print("----- Correct key -----")
        value = input("Value to transfer: ")

        Tx = Transaction("", TxInput("", fromAdress, ""), TxOutput(value, toAdress))
        Transaction_list.append(Tx)
        print("----- Transaction introduced to ledger, add block to execute -----")


    else:
        print("----- Incorrect key -----")
        return 0


def cli_add(blockchain: BlockChain, Transaction_list: list, ws: Wallets, wallet_alias: dict):
    alias = input("User alias: ")
    adress = wallet_alias[alias]

    # Check if wallet exists
    try:
        fileKeys = input("Key file path: ")
        f = open(fileKeys, "r")
        input_pk = f.read()
    except:
        print("file not found")
        return 0

    # Check if private key is correct
    if (ws.wallets[adress].PrivateKey.hex() == input_pk):
        print("----- Correct key -----")
        Transaction_list.append(CoinbaseTx(adress, ""))
        blockchain.addBlock(Transaction_list)
        return True
    return False


def cli_start(ws, wallet_alias):
    print("Creating user wallet to Init BlockChain ...")
    w = cli_wallet(ws, wallet_alias)
    print("--------------------------------------------------")

    print("Retrieving last block or generating genesis block")
    blockchain = InitBlockChain(w)
    print("--------------------------------------------------")

    return blockchain


def main():
    end_script = False
    ws = Wallets()
    wallet_alias = {}
    Transaction_list = []

    cli_help()

    blockchain = cli_start(ws, wallet_alias)

    while (not end_script):
        order = input(" Input new order: ")

        if (order == "wallet"): cli_wallet(ws, wallet_alias)

        if (order == "transaction"): cli_transaction(ws, wallet_alias, Transaction_list)

        if (order == "add"):
            start_time = time.time()
            f = open("startime.txt", "w")
            f.write(f"{start_time}\n")
            f.close()

            if (cli_add(blockchain, Transaction_list, ws, wallet_alias)):
                Transaction_list = []
            print(start_time)

        if (order == "help"): cli_help()

        if (order == "quit"): end_script = True


if __name__ == "__main__":
    main()
