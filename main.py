
from pprint import pprint

from schemas import Blockchain, Transaction

def main():
    transactions_log = [
        {
            "sender": "Alice",
            "receiver": "Bob",
            "amount": 10.0
        },
        {
            "sender": "Bob",
            "receiver": "Alice",
            "amount": 5.0
        },
        {
            "sender": "Bob",
            "receiver": "Alice",
            "amount": 2.3
        },
        {
            "sender": "Bob",
            "receiver": "Alice",
            "amount": 2.7
        }
    ]

    blockchain = Blockchain()
    print(f"Validation: {blockchain.validate_chain()}\n")
    for i, transaction in enumerate(transactions_log):
        print(f"# Transaction {i}")
        blockchain.add_transaction(
            transaction["sender"],
            transaction["receiver"],
            transaction["amount"]
        )
        blockchain.create_new_block()
        pprint(blockchain)
        print(f"Validation: {blockchain.validate_chain()}\n")
        

if __name__ == "__main__":
    main()
