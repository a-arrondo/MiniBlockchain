
from dataclasses import dataclass, field

from config import Config
from domain import Blockchain, Transaction, Neighbour
from schemas import StatusModel, HistoryModel, TransactionModel, PeersModel, NeighbourModel, BlockModel

@dataclass
class BlockChainHandler:
    cfg: Config = field(default_factory=Config)
    blockchain: Blockchain = field(init=False)

    def __post_init__(self):
        self.blockchain = Blockchain(difficulty=self.cfg.difficulty)

    def get_status(self) -> StatusModel:
        return StatusModel(
            length=len(self.blockchain.chain),
            is_valid=self.blockchain.validate_chain()
        )
    
    def get_history(self) -> HistoryModel:
        hist = [
            BlockModel(
                index=block.index,
                previous_hash=block.previous_hash,
                timestamp=block.timestamp,
                transactions=[
                    TransactionModel(
                        sender=trans.sender,
                        receiver=trans.receiver,
                        amount=trans.amount
                    ) for trans in block.transactions
                ],
                nonce=block.nonce,
                hash=block.hash
            ) for block in self.blockchain.chain
        ]

        return HistoryModel(
            length=len(self.blockchain.chain),
            is_valid=self.blockchain.validate_chain(),
            history=hist
        )

    def add_transaction(
            self,
            transaction: TransactionModel
            ) -> None:
        self.blockchain.add_transaction(
            Transaction(
                sender=transaction.sender,
                receiver=transaction.receiver,
                amount=transaction.amount
            )
        )
        # TODO: remove this code in later versions
        self.blockchain.create_new_block()

    def get_neighbours(self) -> PeersModel:
        peers = [
            NeighbourModel(
                ip=peer.ip,
                port=peer.port
            ) for peer in self.blockchain.peers
        ]
        return PeersModel(
            n_peers=len(self.blockchain.peers),
            peers=peers
        )

    def add_neighbours(
            self,
            neighbours: list[NeighbourModel]
            ) -> None:
        neighs = [
            Neighbour(
                ip=neigh.ip,
                port=neigh.port
            )
            for neigh in neighbours
        ]
        self.blockchain.add_neighbours(
            neighs
        )

    def reset_neighbours(self) -> None:
        self.blockchain.reset_neighbours()

