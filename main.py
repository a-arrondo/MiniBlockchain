
from pprint import pprint

from schemas import Block

def main():
    genesis = Block(0, "This is the genesis block", None)
    pprint(genesis)

if __name__ == "__main__":
    main()
