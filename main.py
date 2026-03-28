
from fastapi import status, FastAPI, HTTPException

from config import Config
from domain import Blockchain
from schemas import StatusModel, HistoryModel, TransactionModel, NeighbourModel, PeersModel

cfg = Config()
app = FastAPI()
blockchain = Blockchain(difficulty=cfg.difficulty)

# TODO create pydantic schemas

@app.get("/blockchain/status", response_model=StatusModel)
async def get_blockchain_length():
    try:
        result = {
            "length": len(blockchain.chain),
            "is_valid": blockchain.validate_chain()
        }
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/blockchain/history", response_model=HistoryModel)
async def get_blockchain_history():
    try:
        result = {
            "length": len(blockchain.chain),
            "is_valid": blockchain.validate_chain(),
            "history": blockchain.chain
        }
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/blockchain/append", status_code=status.HTTP_204_NO_CONTENT)
async def add_transaction(
        transaction: TransactionModel
        ):
    try:
        blockchain.add_transaction(
            sender=transaction.sender,
            receiver=transaction.receiver,
            amount=transaction.amount
        )
        blockchain.create_new_block() # TODO: should be removed later
        
        return transaction
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/blockchain/neighbours", status_code=status.HTTP_204_NO_CONTENT)
async def add_neighbours(
        neighbours: list[NeighbourModel]
        ):
    try:
        blockchain.peers.update(neighbours)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/blockchain/neighbours", response_model=PeersModel)
async def get_neighbours():
    return {
        "n_peers": len(blockchain.peers),
        "peers": blockchain.peers
    }

@app.delete("/blockchain/neighbours", status_code=status.HTTP_204_NO_CONTENT)
async def reset_neighbours():
    try:
        blockchain.peers.clear()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
